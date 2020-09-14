from component import EnumValue
from component import Bits
from component import Reg
from component import Peripheral
import component

if __name__ == "__main__":
    a = EnumValue(3,"0x00:11223")
    a = EnumValue(3, "0x00:11223:dddd")
    b = Bits(5,"[2]:name:rw:0x00.description")
    b = Bits(4, "[7-0]:name:rw:0x00")
    b = Reg(4, "0x01:name.32:des")
    b = Reg(4, "0x01:name.32")
    b = Peripheral(4, "0x01:namedes")
    b = Peripheral(4, "0x01:name:32")
