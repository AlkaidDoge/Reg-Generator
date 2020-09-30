# encoding:utf-8
from component import *
import logging
logging.basicConfig(level=logging.INFO)

class Generator:

    def __init__(self,file_path,tab_size:int=4):
        textList,spaceList=self.__resolve1(file_path,tab_size)
        self.__resolve2(textList,spaceList)

    def __resolve1(self,file_path,tab_size:int=4):
        with open(file_path,'r',encoding='utf-8') as f:
            textList=f.readlines()
        # 通过缩进分段
        spaceList=list()
        for e in textList:
            spaceList.append(self.__space_count(e,tab_size))
        spaceSet=set(spaceList)
        spaceSetRemoveSpaceLine=spaceSet.copy()
        spaceSetRemoveSpaceLine.discard(-1)
        assert len(spaceSetRemoveSpaceLine)<=4 and min(spaceSetRemoveSpaceLine)==0,"Format of indent error!"
        spaceSet.add(-1)                  
        spaceSet2List=list(spaceSet)
        spaceSet2List.sort()
        spaceDict=dict(zip(spaceSet2List,[-1,0,1,2,3]))
        for i in range(len(spaceList)):
            spaceList[i]=spaceDict[spaceList[i]]
        # 去除左右空白字符
        for i in range(len(textList)):
            textList[i] = textList[i].strip(' \t\r\f\v\n')
        # 返回段落列表和缩进等级
        logging.info(str(textList))
        logging.info(str(spaceList))
        return textList,spaceList

    def __resolve2(self,textList:list,spaceList:list):
        pList=list()
        p_new=None
        r_new=None
        b_new=None
        e_new=None
        for i in range(len(textList)):
            if spaceList[i]==0:
                s=self.__peripheral_resolve(i+1,textList[i])
                p_new=Peripheral(*s)
                pList.append(p_new)
            elif spaceList[i]==1:
                s=self.__reg_resolve(i+1,textList[i])
                r_new=Reg(*s)
                r_new.mount(p_new)
            elif spaceList[i]==2:
                s=self.__bit_resolve(i+1,textList[i])
                b_new=Bits(*s)
                b_new.mount(r_new)
            elif spaceList[i]==3:
                s=self.__enum_resolve(i+1,textList[i])
                e_new=EnumValue(*s)
                e_new.mount(b_new)
        for e in pList:
            logging.info('\n'+e.info())
        return pList


    def __space_count(self,text:str,tab_size:int=4):
        if text.isspace():
            count=-1
        else:
            text.expandtabs(tab_size)
            count=0
            while count<=len(text):
                if text[count] == ' ':
                    count+=1
                else:
                    break
        return count

    # 以多个symbol作为分隔符，拆分出长度为maxlen的list(大于等于minlen时默认补'')
    # 少于minlen时报错
    def __myspilt(self, line:int,text:str,symbol:str,minlen:int,maxlen:int,default=''):
        symbol = "[" + symbol + "]+"
        mylist=re.split(symbol,text,maxsplit=maxlen-1)
        assert len(mylist)>=minlen,"Miss parameter at {}".format(line)
        while(len(mylist)<maxlen):
            mylist.append(default)
        return mylist

    def __peripheral_resolve(self, line: str, text: str):
        s = self.__myspilt(line, text, ':.', 2, 3)
        logging.info(str(s))
        return s

    def __reg_resolve(self, line: str, text: str):
        s = self.__myspilt(line, text, ':.', 3, 4)
        logging.info(str(s))
        return s

    def __bit_resolve(self, line: str, text: str):
        s = self.__myspilt(line, text, ':.', 4, 5)
        logging.info(str(s))
        return s

    def __enum_resolve(self,line:int,text:str):
        s=self.__myspilt(line,text,".:",2,3)
        logging.info(str(s))
        return s



