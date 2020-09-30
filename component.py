# encoding:utf-8
from enum import Enum
import re
import math
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
        self.value = HWvalue(_remove_space(str(self.value)))
        self.name = _remove_space(self.name)
        self.description = _remove_space(self.description)

    # def __str__(self):
    #     rootList=map(lambda x:x.name if x else None,self.recall())
    #     return '{}.{}.{}.{}({})'. \
    #         format(*rootList, \
    #                self.name,self.value)
    def __str__(self):
        rootList=map(lambda x:x.name if x else None,self.recall())
        return '{}({})'. \
            format(self.name,self.value)

class Bits(Node):
    def __init__(self,section:str,name:str,regType:str,resetValue:str,description:str):
        Node.__init__(self,2)
        self.section=section
        # self.width=width
        self.name=name
        self.regType=regType
        self.resetValue=resetValue
        self.description = description
        self.offset=0
        self.width = 0
        self.__resolve()

    def __resolve(self):
        self.section = _remove_space(self.section)
        self.name = _remove_space(self.name)
        self.regType = RegType(_remove_space(self.regType))
        self.resetValue = HWvalue(_remove_space(str(self.resetValue)))
        self.description = _remove_space(self.description)

        obj=re.findall('(\d+)',self.section)
        if len(obj)==1:
            self.offset=int(obj[0])
            self.width=1
        elif len(obj)==2:
            self.offset=int(obj[1])
            self.width=int(obj[0])-int(obj[1])+1

        # self.width = int(_remove_space(str(self.width)))


    # def __str__(self):
    #     rootList=map(lambda x:x.name if x else None,self.recall())
    #     return '{}.{}.{}({}:{})'. \
    #         format(*rootList, \
    #                self.name,self.section,self.resetValue)
    def __str__(self):
        rootList=map(lambda x:x.name if x else None,self.recall())
        return '{}({}:{})({} downto {})'. \
            format(self.name,self.section,self.resetValue,self.offset+self.width-1,self.offset)

class Reg(Node):
    def __init__(self,offset:str,name:str,width:str,description:str):
        Node.__init__(self,1)
        self.offset=offset
        self.name=name
        self.width=width
        self.description=description
        self.__resolve()

    def __resolve(self):
        self.width = int(_remove_space(str(self.width)))
        self.offset=HWvalue(_remove_space(str(self.offset)))
        self.name=_remove_space(self.name)
        self.description=_remove_space(self.description)

    # def __str__(self):
    #     rootList=map(lambda x:x.name if x else None,self.recall())
    #     return '{}.{}({}:{} bit)'.format(*rootList,self.name,self.offset,self.width)
    def __str__(self):
        return '{}({}:{} bit)'.format(self.name,self.offset,self.width)


class Peripheral(Node):
    def __init__(self,baseAdr:str,name:str,description:str):
        Node.__init__(self,0)
        self.baseAdr=baseAdr
        self.name=name
        self.description=description
        self.__resolve()
    def __resolve(self):
        self.baseAdr=HWvalue(_remove_space(str(self.baseAdr)))
        self.name = _remove_space(self.name)
        self.description = _remove_space(self.description)

    def __str__(self):
        return '{}({})'.format(self.name,self.baseAdr)

    def info(self):
        s=str(self)+'\n'
        for e_reg in self.get_branch():
            s+='\t'+str(e_reg)+'\n'
            for e_bit in e_reg.get_branch():
                s += '\t'*2 + str(e_bit) + '\n'
                for e_enum in e_bit.get_branch():
                    s += '\t' * 3 + str(e_enum) + '\n'
        return s




class HWvalue:
    __radix_dict={'b':2,'o':8,'d':10,'h':16}
    __radix_func={'b':lambda x:bin(x),'o':lambda x:oct(x),\
                  'd':lambda x:'00'+str(x),'h':lambda x:hex(x)}
    
    def __init__(self,sValue:str,width:int=32,*,errorcallback=_callback):
        self.__errorcallback = errorcallback
        self.val,\
        self.width=self.__desolve(sValue,width)

    def __str__(self):
        return str(hex(self.val))

    def __int__(self):
        return self.val

    def __desolve(self,sValue:str,width):
        def is_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
            
        sValue=_remove_space(sValue.lower())
        # (\d)'[bodh]\d(可带下划线)格式
        obj=re.match(r'(\d*)\'([bodh]){1}(\w+)',sValue)
        if obj :
            items=obj.groups()
            radix=HWvalue.__radix_dict[items[1]]
            val = int(items[2],radix)
            # 指明位宽的时候以给定位宽为准
            # 未指明位宽以给定值为准
            width = int(items[0]) if items[0] != '' else width 
            # self.__is_match_width(val,width)
            return val,width

        # 0X格式
        obj = re.match(r'0x(\w+)', sValue)
        if obj:
            val = int(obj.group(1), 16)
            # self.__is_match_width(val, self.width)
            return val,width

        # 10进制数字模式
        if is_int(sValue):
            val = int(sValue, 10)
            # self.__is_match_width(val,self.width)
            return val,width

        # 错误格式
        raise ValueError('格式错误，无效数值')

    def toHWvalue(self,radix:str,separator='',step=4,full_display=False):
        if radix in HWvalue.__radix_dict:
            w=math.ceil(self.width/(math.log2(HWvalue.__radix_dict[radix])))
            text=HWvalue.__radix_func[radix](self.val)[2:].\
                zfill(w if full_display else 0)
            value=HWvalue.__split_by_len(text,step,separator)
            value=str(self.width)+'\''+radix+value
            return value
        else:
            raise ValueError('{}不属于可选进制'.format(radix))

    def toDec(self):
        return str(self.val)

    def toHex(self,separator='',step=4,full_display=False):
        w = math.ceil(self.width / 4)
        text = hex(self.val)[2:].zfill(w if full_display else 0)
        value = HWvalue.__split_by_len(text, step, separator)
        value = '0x' + value
        return value
    
    # 按长度倒叙以指定字符分割字符串
    @classmethod
    def __split_by_len(cls,text,step,separator:str='_'):
        l = len(text)
        if l<=step:
            return text
        else:
            mod=len(text)%step
            t1=text[0:mod]
            t2=re.findall(r'.{'+str(step)+'}', text[mod:])
            t = t1 + separator + separator.join(t2) if t1!='' else separator.join(t2)
            return t

    # 考虑去掉，将语法检查和逻辑检查分开
    # def __is_match_width(self,val,width):
    #     if width != self.width or val > (2 ** self.width) - 1:
    #         self.__errorcallback()
    #         raise Exception('位宽不匹配')
    #     else:
    #         return True

def _remove_space(s:str):
    s.strip(' \t\r\f\v\n')
    return s







