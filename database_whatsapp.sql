-- WhatsApp Integration Database Schema for Auto Prudente
-- Execute este script na tua database PostgreSQL

-- Tabela de Contactos WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_contacts (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    customer_type VARCHAR(50) DEFAULT 'lead', -- 'lead', 'customer', 'vip'
    notes TEXT,
    tags TEXT[], -- Array de tags: ['booking', 'vip', 'support']
    first_contact_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_date TIMESTAMP,
    total_messages INTEGER DEFAULT 0,
    profile_pic_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Conversas WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_conversations (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES whatsapp_contacts(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'closed', 'pending', 'archived'
    assigned_to VARCHAR(100), -- Utilizador responsável (email ou nome)
    priority VARCHAR(20) DEFAULT 'normal', -- 'low', 'normal', 'high', 'urgent'
    last_message_at TIMESTAMP,
    last_message_preview TEXT, -- Prévia da última mensagem
    unread_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Mensagens WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES whatsapp_conversations(id) ON DELETE CASCADE,
    contact_id INTEGER REFERENCES whatsapp_contacts(id) ON DELETE CASCADE,
    whatsapp_message_id VARCHAR(255) UNIQUE, -- ID da mensagem no WhatsApp
    direction VARCHAR(10) NOT NULL, -- 'inbound' (recebida) ou 'outbound' (enviada)
    message_type VARCHAR(50) DEFAULT 'text', -- 'text', 'image', 'document', 'template', 'location', 'button_reply'
    content TEXT, -- Texto da mensagem
    media_url TEXT, -- URL da mídia (imagem, documento)
    media_type VARCHAR(50), -- 'image/jpeg', 'application/pdf', etc
    template_name VARCHAR(100), -- Nome do template (se aplicável)
    status VARCHAR(50) DEFAULT 'sent', -- 'sent', 'delivered', 'read', 'failed'
    error_message TEXT, -- Mensagem de erro se falhou
    sent_by VARCHAR(100), -- Utilizador que enviou (se outbound)
    metadata JSONB, -- Dados adicionais (botões, localização, etc)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Templates de Mensagens (aprovados no WhatsApp)
CREATE TABLE IF NOT EXISTS whatsapp_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'MARKETING', 'UTILITY', 'AUTHENTICATION'
    language VARCHAR(10) DEFAULT 'pt',
    status VARCHAR(50) DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REJECTED'
    whatsapp_template_id VARCHAR(255), -- ID do template aprovado no WhatsApp
    
    -- Estrutura do template
    header_type VARCHAR(20), -- 'TEXT', 'IMAGE', 'DOCUMENT', 'VIDEO', NULL
    header_content TEXT, -- Conteúdo do header (texto ou URL)
    body_content TEXT NOT NULL, -- Corpo da mensagem com {{1}}, {{2}} para variáveis
    footer_content TEXT, -- Rodapé (opcional)
    
    -- Botões (opcional)
    buttons JSONB, -- Array de botões: [{"type": "QUICK_REPLY", "text": "Confirmar"}]
    
    -- Variáveis
    variables JSONB, -- Descrição das variáveis: {"1": "nome_cliente", "2": "data_pickup"}
    
    -- Uso
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Respostas Rápidas (Quick Replies)
CREATE TABLE IF NOT EXISTS whatsapp_quick_replies (
    id SERIAL PRIMARY KEY,
    shortcut VARCHAR(50) UNIQUE NOT NULL, -- Ex: '/ola', '/preco', '/disponibilidade'
    title VARCHAR(100) NOT NULL, -- Título descritivo
    message_text TEXT NOT NULL, -- Texto da mensagem
    category VARCHAR(50), -- 'greeting', 'pricing', 'availability', 'support'
    attachments JSONB, -- Links para imagens/documentos: [{"type": "image", "url": "..."}]
    created_by VARCHAR(100),
    usage_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Configurações WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Logs/Webhook Events
CREATE TABLE IF NOT EXISTS whatsapp_webhook_logs (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50), -- 'message', 'status', 'error'
    payload JSONB, -- Payload completo do webhook
    processed BOOLEAN DEFAULT FALSE,
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_contacts_phone ON whatsapp_contacts(phone_number);
CREATE INDEX IF NOT EXISTS idx_contacts_updated ON whatsapp_contacts(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON whatsapp_conversations(status);
CREATE INDEX IF NOT EXISTS idx_conversations_assigned ON whatsapp_conversations(assigned_to);
CREATE INDEX IF NOT EXISTS idx_conversations_updated ON whatsapp_conversations(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON whatsapp_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_contact ON whatsapp_messages(contact_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON whatsapp_messages(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_messages_direction ON whatsapp_messages(direction);
CREATE INDEX IF NOT EXISTS idx_templates_status ON whatsapp_templates(status);
CREATE INDEX IF NOT EXISTS idx_quick_replies_active ON whatsapp_quick_replies(is_active);

-- Triggers para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_whatsapp_contacts_updated_at 
    BEFORE UPDATE ON whatsapp_contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_whatsapp_conversations_updated_at 
    BEFORE UPDATE ON whatsapp_conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_whatsapp_templates_updated_at 
    BEFORE UPDATE ON whatsapp_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_whatsapp_quick_replies_updated_at 
    BEFORE UPDATE ON whatsapp_quick_replies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Inserir configurações iniciais
INSERT INTO whatsapp_config (config_key, config_value, description) VALUES
    ('access_token', '', 'WhatsApp Cloud API Access Token'),
    ('phone_number_id', '', 'WhatsApp Phone Number ID'),
    ('business_account_id', '', 'WhatsApp Business Account ID'),
    ('webhook_verify_token', '', 'Token para verificação do webhook'),
    ('auto_reply_enabled', 'false', 'Ativar respostas automáticas'),
    ('business_hours', '{"start": "09:00", "end": "18:00"}', 'Horário de atendimento')
ON CONFLICT (config_key) DO NOTHING;

-- Inserir quick replies de exemplo
INSERT INTO whatsapp_quick_replies (shortcut, title, message_text, category) VALUES
    ('/ola', 'Saudação', 'Olá! Bem-vindo à Auto Prudente. Como posso ajudar?', 'greeting'),
    ('/preco', 'Consultar Preços', 'Para consultar preços, por favor indique:\n- Datas de levantamento e devolução\n- Tipo de veículo pretendido\n- Local de levantamento', 'pricing'),
    ('/obrigado', 'Agradecimento', 'Obrigado pelo seu contacto! Estamos sempre disponíveis para ajudar. 🚗', 'greeting')
ON CONFLICT (shortcut) DO NOTHING;

-- Comentários nas tabelas
COMMENT ON TABLE whatsapp_contacts IS 'Contactos/Clientes que interagem via WhatsApp';
COMMENT ON TABLE whatsapp_conversations IS 'Conversas ativas com clientes';
COMMENT ON TABLE whatsapp_messages IS 'Histórico completo de mensagens enviadas e recebidas';
COMMENT ON TABLE whatsapp_templates IS 'Templates de mensagens aprovados pelo WhatsApp';
COMMENT ON TABLE whatsapp_quick_replies IS 'Respostas rápidas para agilizar atendimento';
COMMENT ON TABLE whatsapp_config IS 'Configurações do sistema WhatsApp';
COMMENT ON TABLE whatsapp_webhook_logs IS 'Logs de eventos recebidos do WhatsApp webhook';
