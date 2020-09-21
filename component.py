# encoding:utf-8
from enum import Enum
import re
import logging
import math
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
def RegType(text:str):
    n=typeList.index(text.upper())
    return typeList[n]

def check_type(obj,T:str):
    t_obj = type(obj).__name__
    if t_obj != T and (not isinstance(obj,Node)):
        raise TypeError('Type is {},expect {} or its subclasses'. \
                        format(t_obj, T))
    return None

def _callback():
    pass

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

    def recall(self):
        rootList = []
        e=self
        for i in range(self._rank):
            root = e.get_root()
            rootList.insert(0,root)
            if root:
                e=root
        return rootList

class EnumValue(Node):
    def __init__(self, value, name: str, description: str):
        Node.__init__(self,3)
        self.value = value
        self.name = name
        self.description = description
        self.__resolve()

    def __resolve(self):
        self.value = HWvalue(remove_space(str(self.value)))
        self.name = remove_space(self.name)
        self.description = remove_space(self.description)

    def __str__(self):
        rootList=map(lambda x:x.name if x else None,self.recall())
        return '{}.{}.{}.{}({})'. \
            format(*rootList, \
                   self.name,self.value)

class Bits(Node):
    def __init__(self,section:str,width:str,name:str,regType:str,resetValue:str,description:str):
        Node.__init__(self,2)
        self.section=section
        self.width=width
        self.name=name
        self.regType=regType
        self.resetValue=resetValue
        self.description = description
        self.__resolve()

    def __resolve(self):
        self.section = remove_space(self.section)
        self.width = int(remove_space(str(self.width)))
        self.name = remove_space(self.name)
        self.regType = RegType(remove_space(self.regType))
        self.resetValue = HWvalue(remove_space(str(self.resetValue)))
        self.description = remove_space(self.description)

    def __str__(self):
        rootList=map(lambda x:x.name if x else None,self.recall())
        return '{}.{}.{}({}:{})'. \
            format(*rootList, \
                   self.name,self.section,self.resetValue)

class Reg(Node):
    def __init__(self,offset:str,name:str,width:str,description:str):
        Node.__init__(self,1)
        self.offset=offset
        self.name=name
        self.width=width
        self.description=description
        self.__resolve()

    def __resolve(self):
        self.width = int(remove_space(str(self.width)))
        self.offset=HWvalue(remove_space(str(self.offset)))
        self.name=remove_space(self.name)
        self.description=remove_space(self.description)

    def __str__(self):
        rootList=map(lambda x:x.name if x else None,self.recall())
        return '{}.{}({}:{} bit)'.format(*rootList,self.name,self.offset,self.width)


class Peripheral(Node):
    def __init__(self,baseAdr:str,name:str,description:str):
        Node.__init__(self,0)
        self.baseAdr=baseAdr
        self.name=name
        self.description=description
        self.__resolve()
    def __resolve(self):
        self.baseAdr=HWvalue(remove_space(str(self.baseAdr)))
        self.name = remove_space(self.name)
        self.description = remove_space(self.description)

    def __str__(self):
        return '{}({})'.format(self.name,self.baseAdr)


class HWvalue:
    __radix_dict={'b':2,'o':8,'d':10,'h':16}
    def __init__(self,sValue:str,width:int=32,*,errorcallback=_callback):
        self.width=width
        self.__errorcallback = errorcallback
        self.val=self.__desolve(sValue)

    def __str__(self):
        return str(hex(self.val))
    def __int__(self):
        return self.val

    def __desolve(self,sValue:str):
        def is_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
        sValue=remove_space(sValue.lower())
        # (\d)'[bodh]\d(可带下划线)格式
        obj=re.match(r'(\d*)\'([bodh]){1}(\w+)',sValue)
        if obj :
            items=obj.groups()
            # 未指明位宽的时候以给定位宽为准
            width=int(items[0]) if items[0]!='' else self.width
            radix=HWvalue.__radix_dict[items[1]]
            val=int(items[2],radix)
            # self.__is_match_width(val,width)
            return val

        # 0X格式
        obj = re.match(r'0x(\w+)', sValue)
        if obj:
            val = int(obj.group(1), 16)
            # self.__is_match_width(val, self.width)
            return val

        # 10进制数字模式
        if is_int(sValue):
            val = int(sValue, 10)
            # self.__is_match_width(val,self.width)
            return val

        # 错误格式
        raise Exception('格式错误，无效数值')

    # 考虑去掉，将语法检查和逻辑检查分开
    # def __is_match_width(self,val,width):
    #     if width != self.width or val > (2 ** self.width) - 1:
    #         self.__errorcallback()
    #         raise Exception('位宽不匹配')
    #     else:
    #         return True

    def toBin(self):
        text = bin(self.val)[2:].zfill(self.width)
        v = self.__split_by_len(text,4)
        v = str(self.width)+'\'b'+v
        return v

    def toOct(self):
        text = oct(self.val)[2:]
        v = self.__split_by_len(text, 4)
        v = str(self.width) + '\'o' + v
        return v

    def toDec(self):
        text = str(self.val)
        v = self.__split_by_len(text, 4)
        v = str(self.width) + '\'d' + v
        return v

    def toHex(self):
        text = hex(self.val)[2:]
        v = self.__split_by_len(text,4)
        v = str(self.width)+'\'h'+v
        return v

    # 按长度倒叙以指定字符分割字符串
    def __split_by_len(self,text,lenth,separator:str='_'):
        l = len(text)
        if l<=lenth:
            return text
        else:
            mod=len(text)%lenth
            t1=text[0:mod]
            t2=re.findall(r'.{'+str(lenth)+'}', text[mod:])
            t = t1 + separator + separator.join(t2) if t1!='' else separator.join(t2)
            return t

def remove_space(s:str):
    s.strip(' \t\r\f\v\n')
    return s





# # 以多个symbol作为分隔符，拆分出长度为maxlen的list(大于等于minlen时默认补'')
# # 少于minlen时报错
# def myspilt(line:int,text:str,symbol:str,minlen:int,maxlen:int,default=''):
#     symbol = "[" + symbol + "]+"
#     mylist=re.split(symbol,text,maxsplit=maxlen-1)
#     assert len(mylist)>=minlen,"Miss parameter at {}".format(line)
#     while(len(mylist)<maxlen):
#         mylist.append(default)
#     return mylist

