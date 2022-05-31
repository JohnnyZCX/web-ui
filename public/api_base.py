# -*- coding: utf-8 -*-
# @File: api_base.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/17  10:42


import json

import requests
from urllib3 import encode_multipart_formdata

from config.setting import API_URL, TIMEOUT, HEADERS
from public.common import ErrorExcep, logger, is_assertion_results
from public.reda_data import GetCaseYmal, replace_py_yaml


class ApiBase:

    def __init__(self):
        self.url = API_URL
        self.headers = HEADERS
        self.timeout = TIMEOUT

    def gourl(self, urlpath):
        """
        判断url
        :param urlpath:  url路径
        :return:
        """
        if urlpath is not None:
            if ('http' or 'https') in urlpath:
                return urlpath
            else:
                return self.url + urlpath

    def post(self, urlpath, params, filePath=None, filename=None, verify=False, header=None, upheader=None, code=None,
             assertion=None, assertype=None, isassert=True):
        """
        post 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param filePath:  上传文件路径
        :param filename:  上传文件名称
        :param verify:  https 请求时忽略证书
        :param header:  请求头
        :param upheader: 更新请求参数
        :param code: 状态码
        :param assertion: 预期参数
        :param assertype: 断言类型
        :param isassert: 是否开启模板断言默认是开启
        :return:
        """

        url = self.gourl(urlpath)
        logger.info(f'当前请求接口: {url} ,请求类型: POST')

        if header is None:  # 如果yaml 里面没有 headers就使用默认配置的
            header = self.headers

        if upheader is not None:  # upheader不为空就追加 upheader
            header.update(upheader)

        if self.headers is not None:
            try:
                if params is not None and filePath is not None:
                    # 处理文件上传
                    params['file'] = (filename, open(filePath, 'rb').read())
                    encode_data = encode_multipart_formdata(params)
                    params = encode_data[0]
                    header['Content-Type'] = encode_data[1]

                    with requests.post(url, data=params, headers=header, timeout=self.timeout,
                                       verify=verify) as rep:

                        if isassert and (assertion, assertype) is not None:  # 判断开启默认断言

                            assert rep.status_code == code if code is not None else 200
                            is_assertion_results(rep.json(), assertion, assertype)
                            return rep
                        else:
                            return rep
                with requests.post(url, data=params, headers=header, timeout=self.timeout, verify=verify) as rep:
                    if isassert and (assertion, assertype) is not None:  # 判断开启默认断言
                        assert rep.status_code == code if code is not None else 200
                        is_assertion_results(rep.json(), assertion, assertype)
                        return rep
                    else:
                        return rep
            except Exception as e:
                logger.error(f'请求异常，异常原因:{e}')
                raise ErrorExcep(e)
        else:
            logger.error('headers is not null ！！')
            raise ('headers is not null ！！')

    def get(self, urlpath, params=None, verify=False, header=None, upheader=None, code=None, assertion=None,
            assertype=None, isassert=True):
        """
        get 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:  https 请求时忽略证书
        :param header: 请求头
        :param upheader: 更新请求头参数
        :return:
        """

        url = self.gourl(urlpath)

        logger.info(f'当前请求接口: {url} ,请求类型: GET')

        if header is None:  # 如果yaml 里面没有 headers就使用默认配置的
            header = self.headers

        if upheader is not None:  # upheader不为空就追加 upheader
            header.update(upheader)

        if self.headers is not None:
            try:
                if params is not None:
                    with requests.get(url, params=params, headers=header, timeout=self.timeout,
                                      verify=verify) as rep:
                        if isassert and (assertion, assertype) is not None:  # 判断开启默认断言
                            assert rep.status_code == code if code is not None else 200
                            is_assertion_results(rep.json(), assertion, assertype)
                            return rep
                        else:
                            return rep
                with requests.get(url, headers=header, timeout=self.timeout, verify=verify) as rep:
                    if isassert and (assertion, assertype) is not None:  # 判断开启默认断言
                        assert rep.status_code == code if code is not None else 200
                        is_assertion_results(rep.json(), assertion, assertype)
                        return rep
                    else:
                        return rep
            except Exception as e:
                logger.error(f'请求异常，异常原因:{e}')
                raise ErrorExcep(e)

        else:
            logger.error('headers is not null ！！')
            raise ('headers is not null ！！')

    def put(self, urlpath, params=None, verify=False, header=None, upheader=None):
        """
        put 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:   https 请求时忽略证书
        :param header: 请求头
        :param upheader: 更新请求头参数
        :return:
        """
        url = self.gourl(urlpath)
        logger.info(f'当前请求接口{url} ,请求类型: PUT')

        if header is None:  # 如果yaml 里面没有 headers就使用默认配置的
            header = self.headers

        if upheader is not None:  # upheader不为空就追加 upheader
            header.update(upheader)

        if self.headers is not None:
            try:
                if params is not None:
                    with requests.put(url, data=json.dumps(params), headers=header, timeout=self.timeout,
                                      verify=verify) as rep:
                        return rep
                else:
                    logger.warning('put方法必须传递参数！！')

            except Exception as e:
                logger.error(f'请求异常，异常原因:{e}')
        else:
            logger.error('headers is not null ！！')
            raise ('headers is not null ！！')

    def delete(self, urlpath, verify=False, header=None, upheader=None):
        """
        delete 请求
        :param urlpath:  url 路径
        :param verify:   https 请求时忽略证书
        :param header: 请求头
        :param upheader: 更新请求头参数
        :return:
        """
        url = self.gourl(urlpath)
        logger.info(f'当前请求接口: {url} ,请求类型: DELETE')

        if header is None:  # 如果yaml 里面没有 headers就使用默认配置的
            header = self.headers

        if upheader is not None:  # upheader不为空就追加 upheader
            header.update(upheader)

        if self.headers is not None:
            try:
                with requests.delete(url, headers=header, timeout=self.timeout, verify=verify) as rep:
                    return rep
            except Exception as e:
                logger.error(f'请求出错，出错原因:{e}')
        else:
            logger.error('headers is not null ！！')
            raise ('headers is not null ！！')


def apiexe(yamlfile, case, params=None, verify=True, upheader=None, code=None, assertion=None, assertype=None,
           isassert=True):
    """
    api 请求执行函数
    :param yamlfile:  yaml 文件
    :param case:     yaml:  用例
    :param params:   请求参数
    :param verify:   忽略https
    :param upheader:  更新请求头参数
    :return:
    """

    api = ApiBase()
    yaml = replace_py_yaml(yamlfile)
    yaml_data = GetCaseYmal(yaml_name=yaml, case_name=case)
    requests_type = yaml_data.reqtype.upper()  # 请求类型
    requests_url = yaml_data.urlpath  # url地址
    requests_header = yaml_data.header  # 请求头

    filename = None
    filepath = None
    code = None
    assertion = None
    assertype = None

    # 删除多余参数
    if params is not None:
        try:
            assertion = params.pop('assertion')
            code = params.pop('code')
            assertype = params.pop('assertype')
            filename = params.pop('filename')
            filepath = params.pop('filepath')
        except Exception:
            pass

    # 判断请求类型是否支持
    if requests_type not in ('POST', 'GET', 'PUT', 'DELETE'):
        raise ErrorExcep('请求类型不支持！！！')

    if requests_type == 'POST':
        return api.post(requests_url, params, filePath=filepath, filename=filename, verify=verify,
                        header=requests_header, upheader=upheader, code=code, assertion=assertion, assertype=assertype,
                        isassert=isassert)

    elif requests_type == 'GET':
        return api.get(requests_url, params, verify=verify, header=requests_header, upheader=upheader, code=code,
                       assertion=assertion, assertype=assertype, isassert=isassert)

    elif requests_type == 'PUT':
        return api.put(requests_url, params, verify=verify, header=requests_header, upheader=upheader)

    elif requests_type == 'DELETE':
        return api.delete(requests_url, verify=verify, header=requests_header, upheader=upheader)
    else:
        raise ErrorExcep(f'暂时不支持请求类型{requests_type}！！！')

#
# if __name__ == '__main__':
#     a = ApiBase()
#     d = {
#         "username": "root1",
#         "password": "root",
#         "finame":"nm",
#     }
#
#     ss = apiexe(r'C:\Users\hanwe\Desktop\reda-ui-auto\database\caseYAML\test_api.yaml', 'test_login', params=d)
#     print(ss.json())
