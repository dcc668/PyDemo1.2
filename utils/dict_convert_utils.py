#!  /usr/bin/env python
#ecoding=utf-8
class DictConvertUtils():
    @staticmethod
    def convert(content):
        result=content.replace("datetime.datetime","datetime")
        return eval(result)