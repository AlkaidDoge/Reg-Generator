# encoding:utf-8
from enum import Enum
import re
import logging
logging.basicConfig(level=logging.INFO)

typeList=[
    'RO'    , # w: no effect,                                                       r: no effect
    'RW'    , # w: as-is,                                                           r: no effect
    'RC'    , # w: no effect,                                                       r: clears all bits
    'RS'    , # w: no effect,                                                       r: sets all bits
    'WRC'   , # w: as-is,                                                           r: clears all bits
    'WRS'   , # w: as-is,                                                           r: sets all bits
    'WC'    , # w: clears all bits,                                                 r: no effect
    'WS'    , # w: sets all bits,                                                   r: no effect
    'WSRC'  , # w: sets all bits,                                                   r: clears all bits
    'WCRS'  , # w: clears all bits,                                                 r: sets all bits
    'W1C'   , # w: 1/0 clears/no effect on matching bit,                            r: no effect
    'W1S'   , # w: 1/0 sets/no effect on matching bit,                              r: no effect
    'W1T'   , # w: 1/0 toggles/no effect on matching bit,                           r: no effect
    'W0C'   , # w: 1/0 no effect on/clears matching bit,                            r: no effect
    'W0S'   , # w: 1/0 no effect on/sets matching bit,                              r: no effect
    'W0T'   , # w: 1/0 no effect on/toggles matching bit,                           r: no effect
    'W1SRC' , # w: 1/0 sets/no effect on matching bit,                              r: clears all bits
    'W1CRS' , # w: 1/0 clears/no effect on matching bit,                            r: sets all bits
    'W0SRC' , # w: 1/0 no effect on/sets matching bit,                              r: clears all bits
    'W0CRS' , # w: 1/0 no effect on/clears matching bit,                            r: sets all bits
    'WO'    , # w: as-is,                                                           r: error
    'WOC'   , # w: clears all bits,                                                 r: error
    'WOS'   , # w: sets all bits,                                                   r: error
    'W1'    , # w: first one after hard reset is as-is, other w have no effects,    r: no effect
    'WO1'   , # w: first one after hard reset is as-is, other w have no effects,    r: error
    'NA'    , # w: reserved,                                                        r: reserved
    'W1P'   , # w: 1/0 pulse/no effect on matching bit,                             r: no effect
    'W0P'     # w: 0/1 pulse/no effect on matching bit,                             r: no effect
     ]
def RegType(text:str,line:int=-1):
    try:
        n=typeList.index(text.upper())
    except :
        print("Type error at",line)
    else:
        return typeList[n]

def check_type(obj,T:str):
    t_obj = type(obj).__name__
    if t_obj != T and (not isinstance(obj,Node)):
        raise TypeError('Type is {},expect {} or its subclasses'. \
                        format(t_obj, T))
    return None


class Node:
    def __init__(self,rank:int=-1):
        self._root=None
        self._branch=[]
        self._rank=rank

    def _mount(self, e):
        check_type(e,'Node')
        if self._rank == e._rank + 1:
            if not self._root:
                self._root = e
            else:
                raise OverflowError('Root already exist!')
        else:
            raise TypeError('Please make sure  \
            self\'s rank({}) == parameter\'s rank({})+1'. \
                            format(self._rank, e._rank))

    def _add(self, e):
            check_type(e, 'Node')
            if self._rank+1 ==e._rank:
                self._branch.append(e)
            else:
                raise TypeError('Please make sure  \
                self\'s rank({})+1 == parameter\'s rank({})'. \
                                format(self._rank, e._rank))
        
    def mount(self, e):
        # e比self高级
        if e._rank + 1==self._rank:
            e._add(self)
            self._mount(e)
        else:
            raise TypeError('Rank is {},expect {}'. \
                            format(e._rank, self._rank-1))
    

    def add(self, *args):
        for e in args:
            # self比e高级
            if e._rank==self.get_rank() + 1:
                self._add(e)
                e._mount(self)
            else:
                raise TypeError('Rank is {},expect {}'. \
                                format(e._rank, self._rank+1))

    def get_root(self):
        return self._root

    def get_branch(self):
        return self._branch

    def get_rank(self):
        return self._rank




class EnumValue(Node):
    def __init__(self, value, name: str, description: str):
        Node.__init__(self,3)
        self.value = value
        self.name = name
        self.description = description

    # def __resolve(self,line:int,text:str):
    #     s=myspilt(line,text,":",1,2)
    #     s[0]=int(s[0],16)
    #     logging.info(str(s))
    #     return s
class Bits(Node):
    def __init__(self,section,width:int,name:str,regType:str,resetValue,description:str):
        Node.__init__(self,2)
        # self.enumvalue=[]
        self.section=section
        self.width=width
        self.name=name
        self.regType=regType
        self.resetValue=resetValue
        self.description = description

    # def __resolve(self,line:str,text:str):
    #     s = myspilt(line,text, ':.', 4,5)
    #     condition = s[0][0] == "[" and s[0][-1] == "]"
    #     assert condition, "Miss parameter at {}".format(line)
    #     s[2] = RegType(s[2], line)
    #     s[3] = int(s[3], 16)
    #     s[0] = s[0][1:-1].split("-")
    #     if len(s[0]) == 2:
    #         a, b = map(lambda x: int(x), s[0])
    #         s.insert(1, a - b + 1)
    #         s[0] = b
    #     elif len(s[0])==1:
    #         s[0] = int(s[0][0])
    #     else:
    #         assert False,"Syntax error at {}".format(line)
    #     logging.info(str(s))
    #     return s
    # def add_enum(self,e:EnumValue):
    #     self.enumList.append(e)
class Reg(Node):
    def __init__(self,offset,name:str,width,description:str):
        Node.__init__(self,1)
        # self.bits=[]
        self.offset=offset
        self.name=name
        self.width=width
        self.description=description

    # def __resolve(self, line: str, text: str):
    #     s = myspilt(line, text, ':.', 3, 4)
    #     s[0]=int(s[0],16)
    #     s[2]=int(s[2])
    #     logging.info(str(s))
    #     return s
    # def add_Bits(self,e:Bits):
    #     self.bitsList.append(e)

class Peripheral(Node):
    def __init__(self,baseAdr,name:str,description:str):
        Node.__init__(self,0)
        # self.reg=[]
        self.baseAdr=baseAdr
        self.name=name
        self.description=description



    # def __resolve(self, line: str, text: str):
    #     s = myspilt(line, text, ':.', 2, 3)
    #     s[0]=int(s[0],16)
    #     logging.info(str(s))
    #     return s
    # def add_reg(self,e:Reg):
    #     self.regList.append(e)

# # 以多个symbol作为分隔符，拆分出长度为maxlen的list(大于等于minlen时默认补'')
# # 少于minlen时报错
# def myspilt(line:int,text:str,symbol:str,minlen:int,maxlen:int,default=''):
#     symbol = "[" + symbol + "]+"
#     mylist=re.split(symbol,text,maxsplit=maxlen-1)
#     assert len(mylist)>=minlen,"Miss parameter at {}".format(line)
#     while(len(mylist)<maxlen):
#         mylist.append(default)
#     return mylist

