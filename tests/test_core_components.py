import unittest
from unittest.mock import Mock, patch
import os
import json
from datetime import datetime
from datahub.core.data_source import DataSource, DataSourceConfig, DataSourceFactory
from datahub.core.token_manager import TokenManager
from datahub.core.config_manager import ConfigManager

class TestDataSourceConfig(unittest.TestCase):
    def setUp(self):
        self.credentials = {
            'access_token': 'test_token',
            'client_id': 'test_client'
        }
        self.settings = {
            'api_version': 'v1',
            'timeout': 30
        }
        self.config = DataSourceConfig(self.credentials, self.settings)

    def test_config_initialization(self):
        self.assertEqual(self.config.credentials, self.credentials)
        self.assertEqual(self.config.settings, self.settings)

    def test_config_validation(self):
        self.assertTrue(self.config.validate())

class TestTokenManager(unittest.TestCase):
    def setUp(self):
        self.test_storage_path = os.path.join(os.path.dirname(__file__), 'test_tokens.json')
        self.token_manager = TokenManager(self.test_storage_path)

    def tearDown(self):
        if os.path.exists(self.test_storage_path):
            os.remove(self.test_storage_path)

    def test_store_and_get_token(self):
        test_token = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        self.token_manager.store_token('test_source', test_token)
        retrieved_token = self.token_manager.get_token('test_source')
        self.assertEqual(retrieved_token['access_token'], test_token['access_token'])

    def test_remove_token(self):
        test_token = {'access_token': 'test_token'}
        self.token_manager.store_token('test_source', test_token)
        self.token_manager.remove_token('test_source')
        self.assertIsNone(self.token_manager.get_token('test_source'))

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        self.config_manager = ConfigManager(self.test_config_path)

    def tearDown(self):
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_add_and_get_data_source_config(self):
        source_id = 'test_source'
        source_type = 'test_type'
        credentials = {'access_token': 'test_token'}
        settings = {'api_version': 'v1'}

        self.config_manager.add_data_source(
            source_id, source_type, credentials, settings
        )

        config = self.config_manager.get_source_config(source_id)
        self.assertEqual(config['type'], source_type)
        self.assertEqual(config['credentials'], credentials)
        self.assertEqual(config['settings'], settings)

    def test_remove_data_source(self):
        source_id = 'test_source'
        self.config_manager.add_data_source(
            source_id, 'test_type',
            {'access_token': 'test_token'},
            {'api_version': 'v1'}
        )
        self.config_manager.remove_data_source(source_id)
        self.assertIsNone(self.config_manager.get_source_config(source_id))

class MockDataSource(DataSource):
    def __init__(self, config):
        super().__init__(config)

    def connect(self) -> bool:
        return True

    def fetch_data(self, start_date, end_date, metrics, dimensions):
        return [{'metric1': 100, 'dimension1': 'test'}]

    def validate_credentials(self) -> bool:
        return True

class TestDataSourceFactory(unittest.TestCase):
    def setUp(self):
        DataSourceFactory._sources = {}
        self.config = DataSourceConfig(
            credentials={'access_token': 'test_token'},
            settings={'api_version': 'v1'}
        )

    def test_register_and_create_source(self):
        DataSourceFactory.register('mock_source', MockDataSource)
        source = DataSourceFactory.create('mock_source', self.config)
        self.assertIsInstance(source, MockDataSource)

    def test_create_unknown_source(self):
        with self.assertRaises(ValueError):
            DataSourceFactory.create('unknown_source', self.config)

if __name__ == '__main__':
    unittest.main()
