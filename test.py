import re


def go_split(s, symbol):
    # 拼接正则表达式
    symbol = "[" + symbol + "]+"
    # 一次性分割字符串
    result = re.split(symbol, s)
    # 去除空字符
    return [x for x in result if x]
def _C():
    print('cccccccccccc')

if __name__ == "__main__":

    a={0:lambda x,y,z:'00'+str(x*y*z),1:10}
    print(a[0](10,20,30))
    print(10 in a)
    a='123'+str(None)+'232321'
    print(a.zfill(0))