#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

accessKeyId = 'LTAI4FjD96JZjWRfQ6Gjzwf4'
accessSecret = 'oqqh0KMfE4IQChNPxViIWoVZj1aCoH'

client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

def send_sms(phone_numbers,code):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone_numbers)
    request.add_query_param('SignName', "xfz网站验证")
    request.add_query_param('TemplateCode', "SMS_183150221")
    template_param = {"code":code}
    request.add_query_param('TemplateParam', json.dumps(template_param))

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding = 'utf-8'))