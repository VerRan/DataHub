import unittest
import sys
import os
import pytest

def run_tests():
    """运行所有单元测试"""
    # 添加src目录到Python路径
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    
    # 使用unittest发现并运行测试
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 使用pytest运行测试并生成覆盖率报告
    pytest.main(['tests', '--cov=src/datahub', '--cov-report=html'])
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
