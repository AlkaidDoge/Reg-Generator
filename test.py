import re


def go_split(s, symbol):
    # 拼接正则表达式
    symbol = "[" + symbol + "]+"
    # 一次性分割字符串
    result = re.split(symbol, s)
    # 去除空字符
    return [x for x in result if x]


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

    print(' \t12222222\n'.strip(' \t\r\f\v\n'))
    print('13213')
    print('wwwwwwww')
    a=12345678
    for i in range(100):
        a=a*a
        a=(a>>16) & 0xffff_ffff
        print(a)

