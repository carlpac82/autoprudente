"""
WhatsApp API Endpoints
Endpoints FastAPI para integração WhatsApp
"""

import os
import json
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, Query, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import asyncpg

from whatsapp_client import whatsapp_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

# Configurações
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "meu_token_secreto_123")
DATABASE_URL = os.getenv("DATABASE_URL", "")


# ================== MODELS ==================

class SendMessageRequest(BaseModel):
    phone_number: str
    message: str
    
class SendTemplateRequest(BaseModel):
    phone_number: str
    template_name: str
    variables: Optional[Dict[str, str]] = None
    
class SendImageRequest(BaseModel):
    phone_number: str
    image_url: str
    caption: Optional[str] = ""

class QuickReplyCreate(BaseModel):
    shortcut: str
    title: str
    message_text: str
    category: Optional[str] = None


# ================== WEBHOOK ==================

@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge")
):
    """
    Webhook verification endpoint
    WhatsApp vai chamar isto para verificar o webhook
    """
    logger.info(f"🔐 Webhook verification request: mode={mode}, token={token}")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("✅ Webhook verified successfully")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        logger.warning("❌ Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/webhook")
async def webhook_handler(request: Request):
    """
    Webhook para receber eventos do WhatsApp
    (mensagens recebidas, status de envio, etc)
    """
    try:
        payload = await request.json()
        logger.info(f"📥 Webhook event received: {json.dumps(payload, indent=2)}")
        
        # Guardar evento no log
        await log_webhook_event(payload)
        
        # Processar entrada (mensagem recebida, status, etc)
        entry = payload.get("entry", [])
        if not entry:
            return JSONResponse({"status": "no_entry"})
        
        for item in entry:
            changes = item.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                
                # Processar mensagens recebidas
                if "messages" in value:
                    await process_incoming_messages(value["messages"], value.get("contacts", []))
                
                # Processar atualizações de status
                if "statuses" in value:
                    await process_status_updates(value["statuses"])
        
        return JSONResponse({"status": "ok"})
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {str(e)}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


async def process_incoming_messages(messages: List[Dict], contacts: List[Dict]):
    """Processa mensagens recebidas"""
    for message in messages:
        try:
            from_number = message.get("from")
            message_id = message.get("id")
            timestamp = message.get("timestamp")
            message_type = message.get("type")
            
            # Extrair conteúdo
            content = ""
            media_url = None
            
            if message_type == "text":
                content = message.get("text", {}).get("body", "")
            elif message_type == "image":
                media_url = message.get("image", {}).get("id")
                content = message.get("image", {}).get("caption", "")
            elif message_type == "document":
                media_url = message.get("document", {}).get("id")
                content = message.get("document", {}).get("filename", "")
            elif message_type == "button":
                content = message.get("button", {}).get("text", "")
            elif message_type == "interactive":
                button_reply = message.get("interactive", {}).get("button_reply", {})
                content = button_reply.get("title", "")
            
            logger.info(f"📨 Message from {from_number}: {content}")
            
            # Guardar mensagem na database
            await save_incoming_message(
                phone_number=from_number,
                whatsapp_message_id=message_id,
                message_type=message_type,
                content=content,
                media_url=media_url,
                timestamp=datetime.fromtimestamp(int(timestamp))
            )
            
            # Marcar como lida
            whatsapp_client.mark_as_read(message_id)
            
            # Auto-responder (se ativado)
            # await check_auto_reply(from_number, content)
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {str(e)}")


async def process_status_updates(statuses: List[Dict]):
    """Processa atualizações de status (delivered, read, failed)"""
    for status in statuses:
        try:
            message_id = status.get("id")
            recipient = status.get("recipient_id")
            status_value = status.get("status")  # sent, delivered, read, failed
            timestamp = status.get("timestamp")
            
            logger.info(f"📬 Status update for {message_id}: {status_value}")
            
            # Atualizar status na database
            await update_message_status(message_id, status_value)
            
        except Exception as e:
            logger.error(f"❌ Error processing status: {str(e)}")


# ================== SEND MESSAGES ==================

@router.post("/send-message")
async def send_message(req: SendMessageRequest):
    """Envia mensagem de texto"""
    try:
        result = whatsapp_client.send_text_message(req.phone_number, req.message)
        
        # Guardar mensagem enviada na database
        message_id = result.get("messages", [{}])[0].get("id")
        await save_outgoing_message(
            phone_number=req.phone_number,
            whatsapp_message_id=message_id,
            content=req.message,
            message_type="text"
        )
        
        return JSONResponse({"success": True, "message_id": message_id})
    except Exception as e:
        logger.error(f"❌ Send message error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-template")
async def send_template(req: SendTemplateRequest):
    """Envia mensagem usando template"""
    try:
        # Construir componentes do template
        components = []
        if req.variables:
            parameters = [{"type": "text", "text": val} for val in req.variables.values()]
            components.append({
                "type": "body",
                "parameters": parameters
            })
        
        result = whatsapp_client.send_template_message(
            to=req.phone_number,
            template_name=req.template_name,
            components=components if components else None
        )
        
        message_id = result.get("messages", [{}])[0].get("id")
        await save_outgoing_message(
            phone_number=req.phone_number,
            whatsapp_message_id=message_id,
            content=f"Template: {req.template_name}",
            message_type="template"
        )
        
        return JSONResponse({"success": True, "message_id": message_id})
    except Exception as e:
        logger.error(f"❌ Send template error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-image")
async def send_image(req: SendImageRequest):
    """Envia imagem"""
    try:
        result = whatsapp_client.send_image(req.phone_number, req.image_url, req.caption)
        message_id = result.get("messages", [{}])[0].get("id")
        
        await save_outgoing_message(
            phone_number=req.phone_number,
            whatsapp_message_id=message_id,
            content=req.caption,
            message_type="image",
            media_url=req.image_url
        )
        
        return JSONResponse({"success": True, "message_id": message_id})
    except Exception as e:
        logger.error(f"❌ Send image error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ================== CONVERSATIONS ==================

@router.get("/conversations")
async def get_conversations(status: Optional[str] = None, limit: int = 50):
    """Lista conversas"""
    try:
        conversations = await fetch_conversations(status=status, limit=limit)
        return JSONResponse({"success": True, "conversations": conversations})
    except Exception as e:
        logger.error(f"❌ Get conversations error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: int, limit: int = 100):
    """Obt'em mensagens de uma conversa"""
    try:
        messages = await fetch_conversation_messages(conversation_id, limit=limit)
        return JSONResponse({"success": True, "messages": messages})
    except Exception as e:
        logger.error(f"❌ Get messages error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ================== QUICK REPLIES ==================

@router.get("/quick-replies")
async def get_quick_replies():
    """Lista respostas rápidas"""
    try:
        quick_replies = await fetch_quick_replies()
        return JSONResponse({"success": True, "quick_replies": quick_replies})
    except Exception as e:
        logger.error(f"❌ Get quick replies error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick-replies")
async def create_quick_reply(req: QuickReplyCreate):
    """Cria resposta rápida"""
    try:
        quick_reply_id = await insert_quick_reply(
            shortcut=req.shortcut,
            title=req.title,
            message_text=req.message_text,
            category=req.category
        )
        return JSONResponse({"success": True, "id": quick_reply_id})
    except Exception as e:
        logger.error(f"❌ Create quick reply error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ================== DATABASE HELPERS ==================

async def get_db_connection():
    """Obtém conexão com database"""
    return await asyncpg.connect(DATABASE_URL)


async def log_webhook_event(payload: Dict):
    """Guarda evento do webhook nos logs"""
    conn = await get_db_connection()
    try:
        await conn.execute("""
            INSERT INTO whatsapp_webhook_logs (event_type, payload, processed)
            VALUES ($1, $2, $3)
        """, "message", json.dumps(payload), False)
    finally:
        await conn.close()


async def save_incoming_message(phone_number: str, whatsapp_message_id: str,
                               message_type: str, content: str, media_url: str = None,
                               timestamp: datetime = None):
    """Guarda mensagem recebida"""
    conn = await get_db_connection()
    try:
        # Garantir que contacto existe
        contact_id = await conn.fetchval("""
            INSERT INTO whatsapp_contacts (phone_number, last_message_date)
            VALUES ($1, NOW())
            ON CONFLICT (phone_number) DO UPDATE
            SET last_message_date = NOW(), total_messages = whatsapp_contacts.total_messages + 1
            RETURNING id
        """, phone_number)
        
        # Garantir que conversa existe
        conversation_id = await conn.fetchval("""
            INSERT INTO whatsapp_conversations (contact_id, last_message_at, last_message_preview, unread_count)
            VALUES ($1, NOW(), $2, 1)
            ON CONFLICT (contact_id) DO UPDATE
            SET last_message_at = NOW(), last_message_preview = $2, unread_count = whatsapp_conversations.unread_count + 1
            RETURNING id
        """, contact_id, content[:100])
        
        # Guardar mensagem
        await conn.execute("""
            INSERT INTO whatsapp_messages 
            (conversation_id, contact_id, whatsapp_message_id, direction, message_type, content, media_url, timestamp)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """, conversation_id, contact_id, whatsapp_message_id, "inbound", message_type, content, media_url, timestamp or datetime.now())
        
    finally:
        await conn.close()


async def save_outgoing_message(phone_number: str, whatsapp_message_id: str,
                               content: str, message_type: str, media_url: str = None):
    """Guarda mensagem enviada"""
    conn = await get_db_connection()
    try:
        contact_id = await conn.fetchval("""
            INSERT INTO whatsapp_contacts (phone_number, last_message_date)
            VALUES ($1, NOW())
            ON CONFLICT (phone_number) DO UPDATE
            SET last_message_date = NOW(), total_messages = whatsapp_contacts.total_messages + 1
            RETURNING id
        """, phone_number)
        
        conversation_id = await conn.fetchval("""
            INSERT INTO whatsapp_conversations (contact_id, last_message_at, last_message_preview)
            VALUES ($1, NOW(), $2)
            ON CONFLICT (contact_id) DO UPDATE
            SET last_message_at = NOW(), last_message_preview = $2
            RETURNING id
        """, contact_id, content[:100])
        
        await conn.execute("""
            INSERT INTO whatsapp_messages 
            (conversation_id, contact_id, whatsapp_message_id, direction, message_type, content, media_url, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """, conversation_id, contact_id, whatsapp_message_id, "outbound", message_type, content, media_url, "sent")
        
    finally:
        await conn.close()


async def update_message_status(whatsapp_message_id: str, status: str):
    """Atualiza status de mensagem"""
    conn = await get_db_connection()
    try:
        await conn.execute("""
            UPDATE whatsapp_messages
            SET status = $1
            WHERE whatsapp_message_id = $2
        """, status, whatsapp_message_id)
    finally:
        await conn.close()


async def fetch_conversations(status: str = None, limit: int = 50):
    """Busca conversas"""
    conn = await get_db_connection()
    try:
        if status:
            rows = await conn.fetch("""
                SELECT c.id, c.status, c.assigned_to, c.last_message_at, c.last_message_preview, c.unread_count,
                       co.phone_number, co.name
                FROM whatsapp_conversations c
                JOIN whatsapp_contacts co ON c.contact_id = co.id
                WHERE c.status = $1
                ORDER BY c.last_message_at DESC
                LIMIT $2
            """, status, limit)
        else:
            rows = await conn.fetch("""
                SELECT c.id, c.status, c.assigned_to, c.last_message_at, c.last_message_preview, c.unread_count,
                       co.phone_number, co.name
                FROM whatsapp_conversations c
                JOIN whatsapp_contacts co ON c.contact_id = co.id
                ORDER BY c.last_message_at DESC
                LIMIT $1
            """, limit)
        
        return [dict(row) for row in rows]
    finally:
        await conn.close()


async def fetch_conversation_messages(conversation_id: int, limit: int = 100):
    """Busca mensagens de uma conversa"""
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("""
            SELECT id, direction, message_type, content, media_url, status, timestamp, sent_by
            FROM whatsapp_messages
            WHERE conversation_id = $1
            ORDER BY timestamp DESC
            LIMIT $2
        """, conversation_id, limit)
        
        return [dict(row) for row in rows]
    finally:
        await conn.close()


async def fetch_quick_replies():
    """Busca respostas rápidas"""
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("""
            SELECT id, shortcut, title, message_text, category, usage_count
            FROM whatsapp_quick_replies
            WHERE is_active = TRUE
            ORDER BY usage_count DESC
        """)
        
        return [dict(row) for row in rows]
    finally:
        await conn.close()


async def insert_quick_reply(shortcut: str, title: str, message_text: str, category: str = None):
    """Insere resposta rápida"""
    conn = await get_db_connection()
    try:
        quick_reply_id = await conn.fetchval("""
            INSERT INTO whatsapp_quick_replies (shortcut, title, message_text, category)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """, shortcut, title, message_text, category)
        
        return quick_reply_id
    finally:
        await conn.close()
