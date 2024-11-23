from typing import Dict, Any, Optional
from datetime import datetime
import json
import os

class TokenManager:
    """Manages authentication tokens for different data sources"""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.tokens: Dict[str, Dict[str, Any]] = {}
        self._load_tokens()
    
    def _load_tokens(self):
        """Load tokens from storage"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self.tokens = json.load(f)
    
    def _save_tokens(self):
        """Save tokens to storage"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.tokens, f)
    
    def get_token(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get token for a specific data source"""
        return self.tokens.get(source_id)
    
    def store_token(self, source_id: str, token_data: Dict[str, Any]):
        """Store token for a specific data source"""
        token_data['updated_at'] = datetime.now().isoformat()
        self.tokens[source_id] = token_data
        self._save_tokens()
    
    def remove_token(self, source_id: str):
        """Remove token for a specific data source"""
        if source_id in self.tokens:
            del self.tokens[source_id]
            self._save_tokens()
