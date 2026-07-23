import hashlib
import secrets
from typing import Optional
import logging
import base64

logger = logging.getLogger(__name__)

class Security:
    """Security utilities - Simplified version without cryptography"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        salt = secrets.token_hex(16)
        return f"{salt}:{hashlib.sha256((salt + password).encode()).hexdigest()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        try:
            salt, hash_value = hashed.split(':')
            return hash_value == hashlib.sha256((salt + password).encode()).hexdigest()
        except:
            return False
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """Encrypt data using base64"""
        try:
            encoded = base64.b64encode(data.encode()).decode()
            return encoded
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return None
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: bytes) -> Optional[str]:
        """Decrypt data from base64"""
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            return decoded
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return None
    
    @staticmethod
    def generate_encryption_key() -> bytes:
        """Generate a new encryption key"""
        return secrets.token_bytes(32)