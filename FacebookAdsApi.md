好的,根据Facebook广告效果数据拉取接口,我为您生成了一份接口文档,如下所示:

# Facebook Ads Data Fetch API

## 接口概述

该接口用于拉取Facebook广告效果数据,支持按照指定的时间范围和维度进行数据查询。

## 接口地址

```
GET https://graph.facebook.com/v12.0/{ad_account_id}/insights
```

## 请求参数

| 参数名称 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- |
| ad_account_id | string | 是 | Facebook广告账户ID |
| time_range | object | 是 | 时间范围,包含start_date和end_date字段 |
| fields | string | 是 | 需要返回的数据字段,多个字段用逗号分隔 |
| level | string | 否 | 数据聚合级别,可选值:ad、adset、campaign |
| limit | integer | 否 | 每页返回的结果数量,默认为100 |
| after | string | 否 | 分页标记,用于获取下一页数据 |

## 请求示例

```
GET https://graph.facebook.com/v12.0/987654321/insights?time_range={"start_date":"2023-04-01","end_date":"2023-04-30"}&fields=campaign_name,adset_name,ad_name,impressions,clicks&level=ad&limit=50
```

## 响应参数

| 参数名称 | 类型 | 描述 |
| --- | --- | --- |
| data | array | 查询结果集 |
| - campaign_name | string | 广告活动名称 |
| - adset_name | string | 广告组名称 |
| - ad_name | string | 广告名称 |
| - impressions | integer | 展示数 |
| - clicks | integer | 点击数 |
| paging | object | 分页信息 |
| - next | string | 下一页数据的URL |

## 响应示例

```json
{
  "data": [
    {
      "campaign_name": "Spring Sale Campaign",
      "adset_name": "Audience A",
      "ad_name": "Ad 1",
      "impressions": 10000,
      "clicks": 1234
    },
    {
      "campaign_name": "Summer Promotion",
      "adset_name": "Audience B",
      "ad_name": "Ad 2",
      "impressions": 5000,
      "clicks": 567
    }
  ],
  "paging": {
    "next": "https://graph.facebook.com/v12.0/987654321/insights?time_range=%7B%22start_date%22%3A%222023-04-01%22%2C%22end_date%22%3A%222023-04-30%22%7D&fields=campaign_name%2Cadset_name%2Cad_name%2Cimpressions%2Cclicks&level=ad&limit=50&after=abcdefghijk"
  }
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