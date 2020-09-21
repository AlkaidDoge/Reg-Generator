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
    # 定义初始字符串
    s = '12;;7.osjd;.jshdjdknx+'
    s = "[2-1]:name:rw:0x00"
    # 定义分隔符
    symbol = ';:./+'

    result = go_split(s, symbol)
    print(result)
    print(int('0x12_12',16))
    a=(dict(zip([1,2,3],[0,-1,2,3])))
    print(int('00_10',10))
    print(hex(10))
    b='b'
    print(b)
    s={'1':"a",'2':"b",'b':1}
    print(re.findall('.{4}','1234'))

