"""
WhatsApp Cloud API Client
Cliente para integração com WhatsApp Business Cloud API
"""

import os
import requests
import json
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")


class WhatsAppClient:
    """Cliente para WhatsApp Business Cloud API"""
    
    def __init__(self, access_token: str = None, phone_number_id: str = None):
        self.access_token = access_token or ACCESS_TOKEN
        self.phone_number_id = phone_number_id or PHONE_NUMBER_ID
        self.api_url = f"{WHATSAPP_API_URL}/{self.phone_number_id}"
        
        if not self.access_token or not self.phone_number_id:
            logger.warning("WhatsApp credentials not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers para requisições à API"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Envia mensagem de texto
        
        Args:
            to: Número do destinatário (formato: 351912345678)
            message: Texto da mensagem
            
        Returns:
            Response da API com message_id
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": message
            }
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"✅ Message sent to {to}: {result.get('messages', [{}])[0].get('id')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send message to {to}: {str(e)}")
            raise
    
    def send_template_message(self, to: str, template_name: str, 
                            language: str = "pt", 
                            components: List[Dict] = None) -> Dict[str, Any]:
        """
        Envia mensagem usando template aprovado
        
        Args:
            to: Número do destinatário
            template_name: Nome do template aprovado
            language: Código do idioma (pt, en, etc)
            components: Componentes do template (variáveis, botões)
            
        Returns:
            Response da API
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"✅ Template '{template_name}' sent to {to}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send template to {to}: {str(e)}")
            raise
    
    def send_image(self, to: str, image_url: str, caption: str = "") -> Dict[str, Any]:
        """
        Envia imagem
        
        Args:
            to: Número do destinatário
            image_url: URL da imagem (deve ser acessível publicamente)
            caption: Legenda opcional
            
        Returns:
            Response da API
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {
                "link": image_url
            }
        }
        
        if caption:
            payload["image"]["caption"] = caption
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"✅ Image sent to {to}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send image to {to}: {str(e)}")
            raise
    
    def send_document(self, to: str, document_url: str, filename: str = "", 
                     caption: str = "") -> Dict[str, Any]:
        """
        Envia documento (PDF, etc)
        
        Args:
            to: Número do destinatário
            document_url: URL do documento
            filename: Nome do ficheiro
            caption: Legenda opcional
            
        Returns:
            Response da API
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "document",
            "document": {
                "link": document_url
            }
        }
        
        if filename:
            payload["document"]["filename"] = filename
        if caption:
            payload["document"]["caption"] = caption
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"✅ Document sent to {to}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send document to {to}: {str(e)}")
            raise
    
    def send_location(self, to: str, latitude: float, longitude: float, 
                     name: str = "", address: str = "") -> Dict[str, Any]:
        """
        Envia localização
        
        Args:
            to: Número do destinatário
            latitude: Latitude
            longitude: Longitude
            name: Nome do local
            address: Endereço
            
        Returns:
            Response da API
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            }
        }
        
        if name:
            payload["location"]["name"] = name
        if address:
            payload["location"]["address"] = address
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"✅ Location sent to {to}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send location to {to}: {str(e)}")
            raise
    
    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """
        Marca mensagem como lida
        
        Args:
            message_id: ID da mensagem WhatsApp
            
        Returns:
            Response da API
        """
        url = f"{self.api_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"✅ Message {message_id} marked as read")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to mark message as read: {str(e)}")
            raise
    
    def get_media_url(self, media_id: str) -> str:
        """
        Obtém URL de mídia enviada pelo cliente
        
        Args:
            media_id: ID da mídia
            
        Returns:
            URL da mídia
        """
        url = f"{WHATSAPP_API_URL}/{media_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            return result.get("url", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to get media URL: {str(e)}")
            raise
    
    def download_media(self, media_url: str, save_path: str) -> str:
        """
        Download de mídia
        
        Args:
            media_url: URL da mídia
            save_path: Caminho para salvar o ficheiro
            
        Returns:
            Caminho do ficheiro salvo
        """
        try:
            response = requests.get(media_url, headers=self._get_headers(), stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"✅ Media downloaded to {save_path}")
            return save_path
        except Exception as e:
            logger.error(f"❌ Failed to download media: {str(e)}")
            raise


# Singleton instance
whatsapp_client = WhatsAppClient()
