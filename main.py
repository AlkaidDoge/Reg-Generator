# encoding:utf-8
from component import *
from generator import *
# from test import *
if __name__ == "__main__":
    pass
    # p=Peripheral('0x00','SPI','I AM SPI')
    # regList=[]
    # for i in range(10):
    #     r = Reg(str(i), 'reg'+str(i), "32", 'I am REG'+str(i))
    #     bitsList=[]
    #     for j in range(10):
    #         b = Bits('['+str(i)+']', 1, "bit"+str(i),'RW','1\'b0', 'I am BIT' + str(i))
    #         enumList=[]
    #         for k in range(10):
    #             e = EnumValue(str(i), 'enum' + str(i),'I am ENUM' + str(i))
    #             enumList.append(e)
    #         b.add(*enumList)
    #         bitsList.append(b)
    #     r.add(*bitsList)
    #     regList.append(r)
    # p.add(*regList)

    # r=Reg('0x00','reg1',"32",'noe')
    # b=Bits('[15:9]',"7",'bitsss','Ro',"0x00",'dessss')
    # e=EnumValue('0','ssss','ddddddddd')
    # print('{}\t{}\t{}\t{}'.format(p,r,b,e))
    # b.add(e)
    # p.add(r)
    # r.add(b)
    # print('{}\t{}\t{}\t{}'.format(p,r,b,e))
    p=Peripheral('0x00','SPI','I AM SPI')
    for i in range(10):
        r = Reg(str(i), 'reg'+str(i), "32", 'I am REG'+str(i))
        r.mount(p)
        # print('=========regs{}=========='.format(i))
        for j in range(10):
            b = Bits('['+str(j)+']', 1, "bit"+str(j),'RW','1\'b0', 'I am BIT' + str(j))
            b.mount(r)
            # print('=========bits{}=========='.format(j))
            for k in range(10):
                e = EnumValue(str(k), 'enum' + str(k),'I am ENUM' + str(k))
                e.mount(b)
            else:
                print(e)
        else:
            print(b)
    else:
        print(r)
    print(p)




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











