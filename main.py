# encoding:utf-8
from component import *
from generator import *
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
    b=[]
    aa=Node(0)
    bb=Node(1)
    bb.mount(aa)
    for i in range(10):
        b.append(Node(1))
    print(b)
    a.add(*b)




