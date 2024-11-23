import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from datahub.core.data_source import DataSourceConfig
from datahub.sources.google_ads import GoogleAdsSource
from datahub.sources.facebook_ads import FacebookAdsSource

class TestGoogleAdsSource(unittest.TestCase):
    def setUp(self):
        self.config = DataSourceConfig(
            credentials={
                'customer_id': 'test_customer',
                'access_token': 'test_token'
            },
            settings={
                'api_version': 'v9'
            }
        )
        self.source = GoogleAdsSource(self.config)

    @patch('requests.get')
    def test_validate_credentials(self, mock_get):
        # 模拟成功的API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.assertTrue(self.source.validate_credentials())

        # 验证API调用
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('Authorization', kwargs['headers'])
        self.assertEqual(
            kwargs['headers']['Authorization'],
            'Bearer test_token'
        )

    @patch('requests.get')
    def test_fetch_data(self, mock_get):
        # 模拟API响应数据
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {
                    'campaign': {'name': 'Test Campaign'},
                    'metrics': {
                        'clicks': 100,
                        'impressions': 1000
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        # 执行数据获取
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 31)
        metrics = ['metrics.clicks', 'metrics.impressions']
        dimensions = ['campaign.name']

        results = self.source.fetch_data(
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            dimensions=dimensions
        )

        # 验证结果
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]['campaign.name'],
            'Test Campaign'
        )
        self.assertEqual(results[0]['metrics.clicks'], 100)
        self.assertEqual(results[0]['metrics.impressions'], 1000)

class TestFacebookAdsSource(unittest.TestCase):
    def setUp(self):
        self.config = DataSourceConfig(
            credentials={
                'ad_account_id': 'test_account',
                'access_token': 'test_token'
            },
            settings={
                'api_version': 'v12.0'
            }
        )
        self.source = FacebookAdsSource(self.config)

    @patch('requests.get')
    def test_validate_credentials(self, mock_get):
        # 模拟成功的API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.assertTrue(self.source.validate_credentials())

        # 验证API调用
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('Authorization', kwargs['headers'])
        self.assertEqual(
            kwargs['headers']['Authorization'],
            'Bearer test_token'
        )

    @patch('requests.get')
    def test_fetch_data(self, mock_get):
        # 模拟API响应数据
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'campaign_name': 'Test Campaign',
                    'adset_name': 'Test AdSet',
                    'impressions': 1000,
                    'clicks': 100
                }
            ],
            'paging': {
                'next': None
            }
        }
        mock_get.return_value = mock_response

        # 执行数据获取
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 31)
        metrics = ['impressions', 'clicks']
        dimensions = ['campaign_name', 'adset_name']

        results = self.source.fetch_data(
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            dimensions=dimensions
        )

        # 验证结果
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]['campaign_name'],
            'Test Campaign'
        )
        self.assertEqual(results[0]['impressions'], 1000)
        self.assertEqual(results[0]['clicks'], 100)

    @patch('requests.get')
    def test_fetch_data_with_pagination(self, mock_get):
        # 模拟带分页的API响应
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = {
            'data': [{'campaign_name': 'Campaign 1'}],
            'paging': {
                'next': 'https://next.page.url'
            }
        }

        second_response = Mock()
        second_response.status_code = 200
        second_response.json.return_value = {
            'data': [{'campaign_name': 'Campaign 2'}],
            'paging': {
                'next': None
            }
        }

        mock_get.side_effect = [first_response, second_response]

        results = self.source.fetch_data(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 31),
            metrics=['impressions'],
            dimensions=['campaign_name']
        )

        # 验证结果
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['campaign_name'], 'Campaign 1')
        self.assertEqual(results[1]['campaign_name'], 'Campaign 2')

if __name__ == '__main__':
    unittest.main()
