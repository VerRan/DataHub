好的,根据Google广告效果数据拉取接口,我为您生成了一份接口文档,如下所示:

# Google Ads Data Fetch API

## 接口概述

该接口用于拉取Google广告效果数据,支持按照指定的时间范围和维度进行数据查询。

## 接口地址

```
GET https://googleads.googleapis.com/v9/customers/{customerId}/googleAds:search
```

## 请求参数

| 参数名称 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- |
| customerId | string | 是 | Google Ads客户ID |
| pageSize | integer | 否 | 每页返回的结果数量,默认为1000 |
| pageToken | string | 否 | 分页标记,用于获取下一页数据 |
| query | string | 是 | 查询语句,支持Google Ads查询语法 |

## 请求示例

```
GET https://googleads.googleapis.com/v9/customers/123456789/googleAds:search?query=SELECT campaign.name, metrics.clicks, metrics.impressions FROM campaign WHERE segments.date BETWEEN '2023-04-01' AND '2023-04-30'
```

## 响应参数

| 参数名称 | 类型 | 描述 |
| --- | --- | --- |
| results | array | 查询结果集 |
| - campaign.name | string | 广告活动名称 |
| - metrics.clicks | integer | 点击数 |
| - metrics.impressions | integer | 展示数 |
| nextPageToken | string | 下一页数据的分页标记 |

## 响应示例

```json
{
  "results": [
    {
      "campaign": {
        "name": "Spring Sale Campaign"
      },
      "metrics": {
        "clicks": 1234,
        "impressions": 10000
      }
    },
    {
      "campaign": {
        "name": "Summer Promotion"
      },
      "metrics": {
        "clicks": 567,
        "impressions": 5000
      }
    }
  ],
  "nextPageToken": "abcdefghijk"
}
```

## 错误码

| 错误码 | 描述 |
| --- | --- |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |