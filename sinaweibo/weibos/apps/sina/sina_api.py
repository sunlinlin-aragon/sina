#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from weibos.apps.sina.models import SinaApiData
from weibos.utils.log_utils import get_file_logger

reload(sys)
sys.setdefaultencoding("utf8")

from weibo import APIClient
import re, json
import urllib, urllib2, urllib3, cookielib
import base64, rsa, binascii
from django.conf import settings


sina_log = get_file_logger('sina_api_log')

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    """
    # 参考：风行影者/Blog：http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html
    """
    def http_error_301(cls, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(cls, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(cls, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(cls, req, fp, code, msg, headers)
        result.status = code
        return result


def get_cookie():
    cookies = cookielib.CookieJar()
    return urllib2.HTTPCookieProcessor(cookies)

def get_opener(proxy=False):
    rv = urllib2.build_opener(get_cookie(), SmartRedirectHandler())
    rv.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]
    return rv


class SinaAPI():
    """
    # get_code_NS()方法为风行影者所写。/Blog：http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html
    # get_code_NS()明文传输密码，不安全。所以作者@The_Third_Wave 用模拟登陆的方法获取重要参数'ticket'。保证传输过程中不明文传输密码。保证安全。
    # get_code_Security()方法为作者@The_Third_Wave所写安全自动获取code的方法。
    # 有疑问的请Blog：http://blog.csdn.net/zhanh1218/article/details/26383469留言或者sina微博关注作者@The_Third_Wave。
    """

    def __init__(self, CALLBACK_URL, APP_KEY, REDIRECT_URL, USER_ID, USER_PSWD):
        self.CALLBACK_URL = CALLBACK_URL
        self.APP_KEY = APP_KEY
        self.REDIRECT_URL = REDIRECT_URL
        self.USER_ID = USER_ID
        self.USER_PSWD = USER_PSWD
        self.http = urllib3.PoolManager()

    def get_username(self, USER_ID):
        USER_ID_ = urllib.quote(USER_ID)
        su = base64.encodestring(USER_ID_)[:-1]
        return su

    def get_password_rsa(self, USER_PSWD, PUBKEY, servertime, nonce):
        # 密码加密运算sina我已知有两种，这是其中一种。
        # rsa Encrypt :  #when pwencode = "rsa2"
        rsaPubkey = int(PUBKEY, 16)
        key_1 = int('10001', 16)
        key = rsa.PublicKey(rsaPubkey, key_1)
        message = str(servertime) + "\t" + str(nonce) + "\n" + str(USER_PSWD)
        passwd = rsa.encrypt(message, key)
        passwd = binascii.b2a_hex(passwd)
        return passwd

    def get_parameter(self):
        su = self.get_username(self.USER_ID)
        # su = get_username(USER_ID)‎‎
        url = "https://login.sina.com.cn/sso/prelogin.php?entry=openapi&callback=sinaSSOController.preloginCallBack\
&su=" + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)"
        r = self.http.request('GET', url)
        p = re.compile('\((.*)\)')
        json_data = p.search(r.data).group(1)
        data = json.loads(json_data)
        PUBKEY = data['pubkey']
        pcid = data['pcid']
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = str(data['rsakv'])
        sp = self.get_password_rsa(self.USER_PSWD, PUBKEY, servertime, nonce)
        return pcid, servertime, nonce, rsakv, sp, su

    def get_ticket(self):
        pcid, servertime, nonce, rsakv, sp, su = self.get_parameter()
        fields = urllib.urlencode({
            'entry': 'openapi',
            'gateway': '1',
            'from': '',
            'savestate': '0',
            'useticket': '1',
            'pagerefer': '',
            'pcid': pcid,
            'ct': '1800',
            's': '1',
            'vsnf': '1',
            'vsnval': '',
            'door': '',
            'appkey': 'kxR5R',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1680*1050',
            'encoding': 'UTF-8',
            'cdult': '2',
            'domain': 'weibo.com',
            'prelt': '0',
            'returntype': 'TEXT',
        })
        headers = {
            # "请求": "POST /sso/login.php?client=ssologin.js(v1.4.15)&_=1400652171542 HTTP/1.1",
            # "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Referer": self.CALLBACK_URL,
            # "Accept-Language": "zh-CN",
            # "Origin": "https://api.weibo.com",
            # "Accept-Encoding": "gzip, deflate",
            # "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ZHCNMSE; rv:11.0) like Gecko",
            # "Host": "login.sina.com.cn",
            # "Connection": "Keep-Alive",
            # "Cache-Control": "no-cache",
        }
        url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
        req = urllib2.Request(url, fields, headers)
        f = urllib2.urlopen(req)
        data = json.loads(f.read())
        return data["ticket"]

    def get_code_Security(self):
        ticket = self.get_ticket()
        fields = urllib.urlencode({
            'action': 'submit',
            'display': 'default',
            'withOfficalFlag': '0',
            'quick_auth': 'null',
            'withOfficalAccount': '',
            'scope': '',
            'ticket': ticket,
            'isLoginSina': '',
            'response_type': 'code',
            'regCallback': 'https://api.weibo.com/2/oauth2/authorize?client_id=' + self.APP_KEY + '\
&response_type=code&display=default&redirect_uri=' + self.REDIRECT_URL + '&from=&with_cookie=',
            'redirect_uri': self.REDIRECT_URL,
            'client_id': self.APP_KEY,
            'appkey62': 'kxR5R',
            'state': '',
            'verifyToken': 'null',
            'from': '',
            'userId': "",
            'passwd': "",
        })
        LOGIN_URL = 'https://api.weibo.com/oauth2/authorize'
        headers = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ZHCNMSE; rv:11.0) like Gecko",
                   "Referer": self.CALLBACK_URL,
                   "Content-Type": "application/x-www-form-urlencoded",
                   }
        req = urllib2.Request(LOGIN_URL, fields, headers)
        req_ = urllib2.urlopen(req)
        return_redirect_uri = req_.geturl()
        code = re.findall(r"(?<=code%3D).{32}|(?<=code=).{32}", return_redirect_uri)  # url中=用%3D表示或者=直接表示
        return code

    def get_code_NS(self):
        fields = urllib.urlencode({
            'action': 'submit',
            'display': 'default',
            'withOfficalFlag': '0',
            'quick_auth': 'null',
            'withOfficalAccount': '',
            'scope': '',
            'ticket': '',
            'isLoginSina': '',
            'response_type': 'code',
            'regCallback': '',
            'redirect_uri': self.REDIRECT_URL,
            'client_id': self.APP_KEY,
            'appkey62': 'kxR5R',
            'state': '',
            'verifyToken': 'null',
            'from': '',
            'userId': self.USER_ID,
            'passwd': self.USER_PSWD,
        })
        LOGIN_URL = 'https://api.weibo.com/oauth2/authorize'
        headers = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ZHCNMSE; rv:11.0) like Gecko",
                   "Referer": self.CALLBACK_URL,
                   "Content-Type": "application/x-www-form-urlencoded",
                   }
        r = urllib2.Request(LOGIN_URL, fields, headers)
        opener = get_opener(False)
        urllib2.install_opener(opener)
        try:
            f = opener.open(r)
            return_redirect_uri = f.url
            sina_log.info("NS1: %s" % return_redirect_uri)
        except urllib2.HTTPError, e:
            return_redirect_uri = e.geturl()
            sina_log.info("NS2: %s" % return_redirect_uri)

        code = re.findall(r"(?<=code%3D).{32}|(?<=code=).{32}", return_redirect_uri)
        return code


def get_sina_weibo_access_token():
    client = APIClient(app_key=settings.APP_KEY, app_secret=settings.APP_SECRET, redirect_uri=settings.REDIRECT_URL)
    CALLBACK_URL = client.get_authorize_url()
    API = SinaAPI(CALLBACK_URL, settings.APP_KEY, settings.REDIRECT_URL, settings.USER_NAME, settings.PASSWORD)
    code = API.get_code_Security()
    sina_log.info('sina code %s' % code)
    requests = client.request_access_token(code[0])
    access_token = requests.access_token
    sina_log.info('access_token: %s' % access_token)
    SinaApiData.objects.get_or_create(code=code, token=access_token)
    return access_token