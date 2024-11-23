from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

class DataSource(ABC):
    """Abstract base class for all data sources"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the data source"""
        pass
    
    @abstractmethod
    def fetch_data(self, 
                   start_date: datetime, 
                   end_date: datetime, 
                   metrics: List[str],
                   dimensions: List[str]) -> List[Dict[str, Any]]:
        """Fetch data from the data source"""
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validate the authentication credentials"""
        pass

class DataSourceConfig:
    """Configuration class for data sources"""
    
    def __init__(self, credentials: Dict[str, Any], settings: Dict[str, Any]):
        self.credentials = credentials
        self.settings = settings
    
    def validate(self) -> bool:
        """Validate the configuration"""
        return True

class DataSourceFactory:
    """Factory class for creating data source instances"""
    
    _sources: Dict[str, type] = {}
    
    @classmethod
    def register(cls, source_type: str, source_class: type):
        """Register a new data source type"""
        cls._sources[source_type] = source_class
    
    @classmethod
    def create(cls, source_type: str, config: DataSourceConfig) -> DataSource:
        """Create a new data source instance"""
        if source_type not in cls._sources:
            raise ValueError(f"Unknown data source type: {source_type}")
        
        return cls._sources[source_type](config)
