# encoding:utf-8
from component import *
from generator import *
# from test import *
if __name__ == "__main__":
    pass
    p=Peripheral('0x00','p1','1')
    r=Reg('0x00','reg1',32,'noe')
    b=Bits('[15:9]',7,'bitsss','Ro',0x00,'dessss')
    e=EnumValue(0,'ssss','ddddddddd')
    b.add(e)
    # r.mount(p)
    #
    # p.add(r)
    # e.mount(b)
    # r.add(b)
    # for regs in p.reg:
    #     print(regs.name)
    #     for bit in regs.bits:
    #         print(bit.name)
    #         for enum in bit.enumvalue:
    #             print (enum.name)
    a=Node(0)
    print(a)
    b=[]
    aa=Node(0)
    bb=Node(1)
    bb.mount(aa)
    for i in range(10):
        b.append(Node(1))
    print(b)
    a.add(*b)
    print('********************************')
    a=HWvalue('8\'b0       ', 8)
    HWvalue('8\'b00000000', 8)
    HWvalue('\'b0000_0000', 8)
    HWvalue('8\'h0       ', 8)
    HWvalue('8\'d0       ', 8)
    HWvalue('0           ', 8)
    HWvalue('0x00        ')
    HWvalue('0X00        ')
    print(HWvalue('\'o77       ').toBin())
    print(HWvalue('\'o77       ').toDec())
    print(HWvalue('\'o77       ').toHex())
    print(HWvalue('\'o77       ').toOct())
    print(int(a))










