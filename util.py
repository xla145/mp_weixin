# -*- coding: UTF-8 -*-

# 工具类 分隔符
import hashlib


class CommonUtil:

    @staticmethod
    def md5(text):
        hl = hashlib.md5()
        hl.update(text.encode(encoding='utf-8'))
        return hl.hexdigest()

    @staticmethod
    def str_join(arr, separator=","):
        if arr.__len__() == 1:
            return str(arr)
        return separator.join(arr)


if __name__ == '__main__':
    print(CommonUtil.str_join(['3', '4', '6']))
