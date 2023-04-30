# -*- coding:utf-8 -*-
import json

import requests

import re


def handler(event, context):
    """
    基于华为云的bilibili反向代理

    :param event: see <https://support.huaweicloud.com/devg-functiongraph/functiongraph_02_0420.html>
    :param context: see <https://support.huaweicloud.com/devg-functiongraph/functiongraph_02_0420.html>
    :return:
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(result),
        "headers": {
            "Content-Type": "application/json"
        }
    """

    result = {}

    params = event['queryStringParameters']
    headers = event['headers']
    path = re.sub('/bilihub', '', event['path'])

    match = False
    if 'bilihost' in event['headers'].keys():
        bili_host = event['headers']['bilihost']
        match = re.match(".*.bilibili.com", bili_host)
    else:
        bili_host = 'api.bilibili.com'

    if match:
        bili_headers = {}

        def set_header(key):
            if key in headers.keys():
                bili_headers[key] = headers[key]

        url = f'https://{bili_host}{path}'
        set_header('cookie')
        set_header('origin')
        set_header('referer')
        set_header('user-agent')

        response = requests.request(method='GET', url=url, params=params, headers=bili_headers)

        result['code'] = response.status_code
        if response.status_code == 200:
            result['data'] = json.loads(response.text)
        else:
            result['data'] = 'error'

    else:
        result['code'] = 500
        result['msg'] = 'Host Error.'

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(result),
        "headers": {
            "Content-Type": "application/json"
        }
    }
