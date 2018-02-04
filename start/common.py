import telnetlib
# 检查代理是否可用
def isUseIp(ip):
    try:
        testIps = ip.split(":")
        port = testIps[1]
        telnetlib.Telnet(testIps[0], port=port, timeout=1)
    except:
        return False
    return True




#自定义异常
class BusinessException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)