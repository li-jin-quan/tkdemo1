import urllib.parse
import urllib.request

baseUrl="http://47.106.71.60:9180/service.asmx/"
class MyUrl(object):
    def __init__(self):
        self.url = ""

    # 执行请求
    def getResponse(self, url, data):
        params = urllib.parse.urlencode(data)
        url = url % params
        with urllib.request.urlopen(url, timeout=100) as response:
            return response.read()

    # 获取token
    def getToken(self, uname, pwd):
        data = {
            "name": uname,
            "psw": pwd
        }
        url = baseUrl+"UserLoginStr?%s"
        return self.getResponse(url, data)

    # 获取手机号
    def getTelNum(self, token):
        data = {
            "token": token,
            "xmid": 200,
            "sl": 1,
            "lx": 1,
            "a1": "",
            "a2": "",
            "pk": "",
            "ks": 0,
            "rj": 0
        }
        url = baseUrl+"GetHM2Str?%s"
        return self.getResponse(url, data)

    # 获取验证码
    def getVerificationCode(self, token, telNumber):
        url = baseUrl+"GetYzm2Str?%s"

        data = {
            "token": token,
            "hm": telNumber[3:13],
            "xmid": 200,
            "sf": 0
        }
        return self.getResponse(url, data)

    #释放号码
    def releaseNum(self,token,num):
        url = baseUrl+"sfHmStr?%s"
        data = {
            "token": token,
            "hm":num
        }
        return self.getResponse(url, data)
