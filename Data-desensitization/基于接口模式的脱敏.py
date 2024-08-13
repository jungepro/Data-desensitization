
import re
import time
from functools import update_wrapper

class DataWM:
    def __init__(self,func):
    # def __init__(self):
        self.data_list = []
        self.hiden2="*"
        # 身份证匹配表达式
        self.IDCARD = "[0-9]{18}"
        # 敏感关键字匹配规则
        self.keyword_list=["张","科技"]
        # 匹配密码
        self.passwd = "(password=|passwd=)[0-9]+"
        self.filterdata = []
        self.partten7 = "[0-9]+"
        self._func = func
        self._func_name = func.__name__
        update_wrapper(self, self._func)

    def __partten_passwd(self,value):
        print(value)
        return value
    def __partten_number(self,value):
        value=str(value)
        phone_list=re.findall("[1-9]{1}[0-9]{10}",value)
        for item in phone_list:
            value=value.replace(item[2:-2],len(item[2:-2])*self.hiden2)
        return value
    def __partten_all(self,value):
        '''
        全字段脱敏:
        身份证、电话、关键字、密码
        '''
        value=str(value)
        re_pass=re.findall("'密码':\s'\S+'",value)[0].split(":")[1]
        value=value.replace(re_pass,len(re_pass)*self.hiden2)

        phone_list=re.findall("[1-9]{1}[0-9]{10}",value)

        for item in phone_list:
            value=value.replace(item[2:-2],len(item[2:-2])*self.hiden2)

        for item in self.keyword_list:
            if re.findall(item,value):
                value=self.__partten_keyword(value,item)
        return value

    def __partten_keyword(self,value,keyword):
           value=value.replace(keyword,len(keyword)*self.hiden2)
           return value
    def hitIDCARD(self,value):
            value=self.__partten_number(value)
            return value
    def hitPasswd(self,value):
        '''
        只取首位与最后一位
        '''
        value=str(value)
        if re.match(self.passwd, value):
            value=self.__partten_passwd(value)
            return value
    def hitPhone(self,value):
            return self.__partten_number(value)
    def hitKeyWord(self,value):
        value=str(value)
        for item in self.keyword_list:
            if re.findall(item,value):
                value=self.__partten_keyword(value,item)
        return value
    def hitall(self,value):
        return self.__partten_all(value)


    def __call__(self,val):
        if self.hitall(val):
            return self.hitall(val)
        # if self.hitPhone(val):
        #     return self.hitPhone(val)
        # if self.hitKeyWord(val):
        #     return self.hitKeyWord(val)
        # if self.hitPasswd(val):
        #     return self.hitPasswd(val)
        # if self.hitIDCARD(val):
        #     return self.hitIDCARD(val)





def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(args)
        end_time = time.time()
        print(end_time - start_time)
        print(args)

    return wrapper
@DataWM
def test(data):
    return data
