# -*- coding:utf-8 -*-
## 读取SNL源文件
def read_file(file_name):
	fp = open(file_name)
	source = fp.read()    ## 读入字符串
	fp.close()
	return source
