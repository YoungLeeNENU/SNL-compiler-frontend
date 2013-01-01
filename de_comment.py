# -*- coding:utf-8 -*-
## 利用正则表达式去掉注释
import re

def de_comment(source):
	## pattern = re.compile(r"{+.*?}", re.DOTALL)    ## 不贪婪并且DOTALL模式
	pattern = re.compile(r"{+.*?}|{+.*?EOF", re.DOTALL)    ## 不贪婪并且DOTALL模式
	container = pattern.findall(source)    ## 搜索source并以列表形式返回全部能匹配的子串

	for x in container:
		check = re.compile(r"\n", re.DOTALL)
		result, number = check.subn(" ", x)    ## 找注释部分换行符号的个数

		source = source.replace(x, "\n" * number + " ")

	## 	## 需要而外加上的EOF
	## if source[len(source) - 4:] != " EOF":
	## 	source = source + " EOF"

	return source
