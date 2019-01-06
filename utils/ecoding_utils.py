#!  /usr/bin/env python
#ecoding=utf-8
import chardet
class EncodingUtils:
    #byteTarget 字节类型数据
    @staticmethod
    def getStrNotKnowEcoding(byteTarget):
        json = chardet.detect(byteTarget);
        htmlStr = EncodingUtils.decodeAndEncode(byteTarget, json["encoding"]);
        return htmlStr;

    @staticmethod
    def decodeAndEncode(target,decode):
        decode=decode.lower()
        if 'utf-8'==decode:
            htmlStr = str(target, "utf-8")  # toString
        elif decode == 'gb2312'or decode == 'iso-8859-9'or decode == 'windows-1254':
            decode='gb18030'#直接用gb2312解码，有时抱错
            bhtml = target.decode(decode,'ignore').encode("utf-8")
            htmlStr = str(bhtml, "utf-8")  # toString
        else:
            bhtml = target.decode(decode).encode("utf-8")
            htmlStr = str(bhtml, "utf-8")  # toString
        return htmlStr