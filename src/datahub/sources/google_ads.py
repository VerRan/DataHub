from typing import Dict, Any, List
from datetime import datetime
from ..core.data_source import DataSource, DataSourceConfig
import requests

class GoogleAdsSource(DataSource):
    """Google Ads data source implementation"""
    
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.base_url = "https://googleads.googleapis.com/v9"
        self.token = None
    
    def connect(self) -> bool:
        """Establish connection to Google Ads API"""
        try:
            self.token = self.config.credentials.get('access_token')
            return self.validate_credentials()
        except Exception as e:
            print(f"Failed to connect to Google Ads API: {str(e)}")
            return False
    
    def validate_credentials(self) -> bool:
        """Validate the authentication credentials"""
        if not self.token:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            customer_id = self.config.credentials.get('customer_id')
            url = f"{self.base_url}/customers/{customer_id}"
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def fetch_data(self,
                   start_date: datetime,
                   end_date: datetime,
                   metrics: List[str],
                   dimensions: List[str]) -> List[Dict[str, Any]]:
        """Fetch data from Google Ads API"""
        if not self.token:
            raise ValueError("Not connected to Google Ads API")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            customer_id = self.config.credentials.get('customer_id')
            
            # Construct GAQL query
            select_fields = ', '.join(dimensions + metrics)
            date_range = f"segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"
            query = f"SELECT {select_fields} FROM campaign WHERE {date_range}"
            
            url = f"{self.base_url}/customers/{customer_id}/googleAds:search"
            params = {'query': query}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._process_response(data)
        except Exception as e:
            print(f"Failed to fetch data from Google Ads API: {str(e)}")
            return []
    
    def _process_response(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process the API response and convert it to standard format"""
        results = []
        for row in response_data.get('results', []):
            processed_row = {}
            # Flatten the nested structure
            for key, value in row.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        processed_row[f"{key}.{sub_key}"] = sub_value
                else:
                    processed_row[key] = value
            results.append(processed_row)
        return results

# Register the source with the factory
from ..core.data_source import DataSourceFactory
DataSourceFactory.register('google_ads', GoogleAdsSource)
