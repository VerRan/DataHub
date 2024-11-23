from datetime import datetime, timedelta
from datahub.core.config_manager import ConfigManager
import json
import os

def main():
    # Initialize configuration manager
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    os.makedirs(config_dir, exist_ok=True)
    config_manager = ConfigManager(os.path.join(config_dir, 'config.json'))

    # Example: Configure Google Ads data source
    google_ads_config = {
        'credentials': {
            'customer_id': 'your-customer-id',
            'access_token': 'your-access-token'
        },
        'settings': {
            'api_version': 'v9'
        }
    }
    config_manager.add_data_source(
        source_id='google_ads_main',
        source_type='google_ads',
        credentials=google_ads_config['credentials'],
        settings=google_ads_config['settings']
    )

    # Example: Configure Facebook Ads data source
    facebook_ads_config = {
        'credentials': {
            'ad_account_id': 'your-ad-account-id',
            'access_token': 'your-access-token'
        },
        'settings': {
            'api_version': 'v12.0'
        }
    }
    config_manager.add_data_source(
        source_id='facebook_ads_main',
        source_type='facebook_ads',
        credentials=facebook_ads_config['credentials'],
        settings=facebook_ads_config['settings']
    )

    # Example: Fetch data from Google Ads
    try:
        google_ads = config_manager.get_data_source('google_ads', 'google_ads_main')
        if google_ads and google_ads.connect():
            # Fetch last 30 days of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            metrics = ['metrics.impressions', 'metrics.clicks', 'metrics.cost_micros']
            dimensions = ['campaign.name', 'ad_group.name']
            
            results = google_ads.fetch_data(
                start_date=start_date,
                end_date=end_date,
                metrics=metrics,
                dimensions=dimensions
            )
            
            print("Google Ads Data:")
            print(json.dumps(results[:2], indent=2))  # Print first 2 results
        else:
            print("Failed to connect to Google Ads")
    except Exception as e:
        print(f"Error fetching Google Ads data: {str(e)}")

    # Example: Fetch data from Facebook Ads
    try:
        facebook_ads = config_manager.get_data_source('facebook_ads', 'facebook_ads_main')
        if facebook_ads and facebook_ads.connect():
            # Fetch last 30 days of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            metrics = ['impressions', 'clicks', 'spend']
            dimensions = ['campaign_name', 'adset_name', 'ad_name']
            
            results = facebook_ads.fetch_data(
                start_date=start_date,
                end_date=end_date,
                metrics=metrics,
                dimensions=dimensions
            )
            
            print("\nFacebook Ads Data:")
            print(json.dumps(results[:2], indent=2))  # Print first 2 results
        else:
            print("Failed to connect to Facebook Ads")
    except Exception as e:
        print(f"Error fetching Facebook Ads data: {str(e)}")

if __name__ == "__main__":
    main()
