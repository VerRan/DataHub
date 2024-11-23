from typing import Dict, Any, List
from datetime import datetime
from ..core.data_source import DataSource, DataSourceConfig
import requests

class FacebookAdsSource(DataSource):
    """Facebook Ads data source implementation"""
    
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.base_url = "https://graph.facebook.com/v12.0"
        self.token = None
    
    def connect(self) -> bool:
        """Establish connection to Facebook Ads API"""
        try:
            self.token = self.config.credentials.get('access_token')
            return self.validate_credentials()
        except Exception as e:
            print(f"Failed to connect to Facebook Ads API: {str(e)}")
            return False
    
    def validate_credentials(self) -> bool:
        """Validate the authentication credentials"""
        if not self.token:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            response = requests.get(
                f"{self.base_url}/me",
                headers=headers
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def fetch_data(self,
                   start_date: datetime,
                   end_date: datetime,
                   metrics: List[str],
                   dimensions: List[str]) -> List[Dict[str, Any]]:
        """Fetch data from Facebook Ads API"""
        if not self.token:
            raise ValueError("Not connected to Facebook Ads API")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            
            account_id = self.config.credentials.get('ad_account_id')
            
            params = {
                'time_range': {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                },
                'fields': ','.join(metrics + dimensions),
                'level': 'ad'  # Default to ad level, can be configured
            }
            
            url = f"{self.base_url}/{account_id}/insights"
            
            all_results = []
            next_page = url
            
            while next_page:
                response = requests.get(next_page, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                all_results.extend(self._process_response(data))
                
                # Handle pagination
                paging = data.get('paging', {})
                next_page = paging.get('next')
                # Clear params for subsequent requests as they're included in the next URL
                params = None
            
            return all_results
        except Exception as e:
            print(f"Failed to fetch data from Facebook Ads API: {str(e)}")
            return []
    
    def _process_response(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process the API response and convert it to standard format"""
        return response_data.get('data', [])

# Register the source with the factory
from ..core.data_source import DataSourceFactory
DataSourceFactory.register('facebook_ads', FacebookAdsSource)
