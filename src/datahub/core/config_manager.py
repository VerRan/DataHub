from typing import Dict, Any, Optional
import json
import os
from .token_manager import TokenManager
from .data_source import DataSourceConfig, DataSourceFactory

class ConfigManager:
    """Manages system-wide configuration and data source settings"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.token_manager = TokenManager(os.path.join(os.path.dirname(config_path), 'tokens.json'))
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
    
    def _save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_data_source(self, source_type: str, source_id: str) -> Optional[Any]:
        """Get a configured data source instance"""
        source_config = self.config.get('sources', {}).get(source_id)
        if not source_config:
            return None
        
        # Get token from token manager
        token_data = self.token_manager.get_token(source_id)
        if token_data:
            source_config['credentials'].update(token_data)
        
        config = DataSourceConfig(
            credentials=source_config.get('credentials', {}),
            settings=source_config.get('settings', {})
        )
        
        return DataSourceFactory.create(source_type, config)
    
    def add_data_source(self, source_id: str, source_type: str, 
                       credentials: Dict[str, Any], settings: Dict[str, Any]):
        """Add or update a data source configuration"""
        if 'sources' not in self.config:
            self.config['sources'] = {}
        
        self.config['sources'][source_id] = {
            'type': source_type,
            'credentials': credentials,
            'settings': settings
        }
        self._save_config()
    
    def remove_data_source(self, source_id: str):
        """Remove a data source configuration"""
        if source_id in self.config.get('sources', {}):
            del self.config['sources'][source_id]
            self._save_config()
            self.token_manager.remove_token(source_id)
    
    def update_source_credentials(self, source_id: str, credentials: Dict[str, Any]):
        """Update credentials for a data source"""
        if source_id in self.config.get('sources', {}):
            self.config['sources'][source_id]['credentials'].update(credentials)
            self._save_config()
            
            # Update token if present in credentials
            if 'access_token' in credentials:
                self.token_manager.store_token(source_id, {
                    'access_token': credentials['access_token']
                })
    
    def get_source_config(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific data source"""
        return self.config.get('sources', {}).get(source_id)
