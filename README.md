# DataHub - Automated Data Integration Platform

DataHub是一个自动化数据集成平台，支持从多个数据源（如Google Ads、Facebook Ads等）自动拉取数据，用于BI分析。

## 特性

- 支持多数据源集成
- 统一的数据源抽象接口
- 灵活的配置管理系统
- 永久性Token管理
- 可扩展的架构设计

## 项目结构

```
src/
├── datahub/
│   ├── core/
│   │   ├── data_source.py     # 数据源抽象基类
│   │   ├── token_manager.py   # Token管理器
│   │   └── config_manager.py  # 配置管理器
│   └── sources/
│       ├── google_ads.py      # Google Ads数据源实现
│       └── facebook_ads.py    # Facebook Ads数据源实现
├── examples/
│   └── data_fetch_example.py  # 使用示例
└── tests/
    ├── test_core_components.py    # 核心组件测试
    ├── test_data_sources.py       # 数据源实现测试
    └── test_config.json           # 测试配置文件
```

## 安装

1. 克隆项目：
```bash
git clone <repository-url>
cd datahub
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 创建配置目录：
```bash
mkdir -p src/config
```

2. 配置数据源：

示例配置文件 (src/config/config.json):
```json
{
  "sources": {
    "google_ads_main": {
      "type": "google_ads",
      "credentials": {
        "customer_id": "your-customer-id",
        "access_token": "your-access-token"
      },
      "settings": {
        "api_version": "v9"
      }
    },
    "facebook_ads_main": {
      "type": "facebook_ads",
      "credentials": {
        "ad_account_id": "your-ad-account-id",
        "access_token": "your-access-token"
      },
      "settings": {
        "api_version": "v12.0"
      }
    }
  }
}
```

## 使用示例

```python
from datahub.core.config_manager import ConfigManager
from datetime import datetime, timedelta

# 初始化配置管理器
config_manager = ConfigManager('src/config/config.json')

# 获取Google Ads数据源实例
google_ads = config_manager.get_data_source('google_ads', 'google_ads_main')

# 连接到Google Ads API
if google_ads.connect():
    # 设置时间范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # 设置指标和维度
    metrics = ['metrics.impressions', 'metrics.clicks', 'metrics.cost_micros']
    dimensions = ['campaign.name', 'ad_group.name']
    
    # 获取数据
    results = google_ads.fetch_data(
        start_date=start_date,
        end_date=end_date,
        metrics=metrics,
        dimensions=dimensions
    )
    
    print(results)
```

## 运行测试

项目包含完整的单元测试套件，使用unittest和pytest框架。测试覆盖了核心组件和数据源实现。

1. 运行所有测试：
```bash
python run_tests.py
```

2. 仅运行特定测试：
```bash
# 运行核心组件测试
python -m unittest tests/test_core_components.py

# 运行数据源测试
python -m unittest tests/test_data_sources.py
```

3. 生成测试覆盖率报告：
```bash
pytest tests --cov=src/datahub --cov-report=html
```

覆盖率报告将生成在 `htmlcov` 目录中，可以在浏览器中打开 `htmlcov/index.html` 查看详细的覆盖率信息。

## 添加新的数据源

1. 在 `src/datahub/sources` 目录下创建新的数据源实现类
2. 继承 `DataSource` 基类并实现所需方法
3. 使用 `DataSourceFactory.register()` 注册新的数据源
4. 在 `tests/test_data_sources.py` 中添加相应的单元测试

示例：
```python
from datahub.core.data_source import DataSource, DataSourceFactory

class NewDataSource(DataSource):
    def __init__(self, config):
        self.config = config
        
    def connect(self):
        # 实现连接逻辑
        pass
        
    def fetch_data(self, start_date, end_date, metrics, dimensions):
        # 实现数据获取逻辑
        pass
        
    def validate_credentials(self):
        # 实现认证验证逻辑
        pass

# 注册新数据源
DataSourceFactory.register('new_source', NewDataSource)
```

## 错误处理

该框架包含完整的错误处理机制：

- 连接错误处理
- 认证错误处理
- 数据获取错误处理
- 配置错误处理

所有错误都会被适当捕获并记录，确保系统的稳定运行。

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 编写测试用例
4. 实现新功能
5. 确保所有测试通过
6. 提交更改
7. 推送到分支
8. 创建 Pull Request

## 许可证

MIT License
