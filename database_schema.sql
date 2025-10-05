-- AI Chat Kod Editörü Veritabanı Şeması

-- Messages tablosu - Kullanıcı mesajları
CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_tokens INTEGER DEFAULT 0
);

-- Knowledge tablosu - AI yanıtları
CREATE TABLE IF NOT EXISTS knowledge (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT REFERENCES messages(id) ON DELETE CASCADE,
    knowledge_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_created_by ON messages(created_by);
CREATE INDEX IF NOT EXISTS idx_knowledge_message_id ON knowledge(message_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_created_at ON knowledge(created_at);

-- Örnek veri
INSERT INTO messages (content, created_by, input_tokens) VALUES 
('Python ile web scraper nasıl yazılır?', 'user', 8),
('React ile todo app oluşturmak istiyorum', 'user', 7);