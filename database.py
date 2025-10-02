import psycopg2
from sqlalchemy import create_engine, text
import streamlit as st
from datetime import datetime

class DatabaseManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = None
        
    def connect(self):
        try:
            # PostgreSQL connection string'i SQLAlchemy formatına çevir
            conn_parts = self.connection_string.split(';')
            host = conn_parts[0].split('=')[1]
            port = conn_parts[1].split('=')[1]
            database = conn_parts[2].split('=')[1]
            username = conn_parts[3].split('=')[1]
            password = conn_parts[4].split('=')[1]
            
            sqlalchemy_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            self.engine = create_engine(sqlalchemy_url)
            return True
        except Exception as e:
            st.error(f"Veritabanı bağlantı hatası: {e}")
            return False
    
    def create_tables(self):
        """Veritabanı tablolarını oluştur"""
        try:
            with self.engine.connect() as conn:
                # Messages tablosu
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id BIGSERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        created_by TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        input_tokens INTEGER DEFAULT 0
                    )
                """))
                
                # Knowledge tablosu
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS knowledge (
                        id BIGSERIAL PRIMARY KEY,
                        message_id BIGINT REFERENCES messages(id),
                        knowledge_text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Tablo oluşturma hatası: {e}")
            return False
    
    def save_message(self, content, created_by, input_tokens=0):
        """Mesaj kaydet"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO messages (content, created_by, input_tokens)
                    VALUES (:content, :created_by, :input_tokens)
                    RETURNING id
                """), {
                    'content': content,
                    'created_by': created_by,
                    'input_tokens': input_tokens
                })
                message_id = result.fetchone()[0]
                conn.commit()
                return message_id
        except Exception as e:
            st.error(f"Mesaj kaydetme hatası: {e}")
            return None
    
    def save_knowledge(self, message_id, knowledge_text):
        """Bilgi kaydet"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO knowledge (message_id, knowledge_text)
                    VALUES (:message_id, :knowledge_text)
                """), {
                    'message_id': message_id,
                    'knowledge_text': knowledge_text
                })
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Bilgi kaydetme hatası: {e}")
            return False
    
    def get_chat_history(self, limit=50):
        """Chat geçmişini getir"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT m.content, m.created_by, m.created_at, k.knowledge_text
                    FROM messages m
                    LEFT JOIN knowledge k ON m.id = k.message_id
                    ORDER BY m.created_at DESC
                    LIMIT :limit
                """), {'limit': limit})
                return result.fetchall()
        except Exception as e:
            st.error(f"Geçmiş getirme hatası: {e}")
            return []