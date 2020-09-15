# encoding:utf-8
from component import *

class Generator:

    def __init__(self,file_path,tab_size:int=4):
        print(self.__resolve(file_path,tab_size))

    def __resolve(self,file_path,tab_size:int=4):
        f=open(file_path,'r',encoding='utf-8')
        textList=f.readlines()
        f.close()
        # 通过缩进分段
        spaceList=list()
        for e in textList:
            spaceList.append(self.space_count(e,tab_size))
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
        return textList,spaceList


    def space_count(self,text:str,tab_size:int=4):
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



