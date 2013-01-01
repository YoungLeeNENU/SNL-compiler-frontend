# -*- coding:utf-8 -*-
## 错误提示
import os
import sys
import tag
import de_comment
import symbol_list
import lexeme

lex_error = ": SyntaxError. Symbol illegal"    ## 词法分析错误
cmt_error = ": CommentError. Only one comment symbol found"    ## 注释错误
ch_error = ": SyntaxError. Char illegal"	## 字符起始和结束符错误

flag = 0

## 错误检查
def error_sence(element, line):
	global flag

	## 注释错误
	if element == symbol_list.symbol_list['cmt_start']:
		print "at line", line, cmt_error
		flag = 1
		return tag.snl_tag[5]
	elif element == symbol_list.symbol_list['cmt_end']:
		print "at line", line, cmt_error
		flag = 1
		return tag.snl_tag[6]
	## 字符错误
	elif element == symbol_list.symbol_list['ch_start_end']:
		print "at line", line, ch_error
		flag = 1
		return None
	## 字符
	elif element[0] == "'" and len(element) > 1:
		return tag.snl_tag[7]
	## 双字符分界符
  	elif element == symbol_list.symbol_list['double_char']:
		return tag.snl_tag[4]
	## 数组下标界限符
	elif element == symbol_list.symbol_list['ch_array']:
		return tag.snl_tag[8]
	## 单字符分界符
	elif element in symbol_list.symbol_list['single_char'].values():
		return tag.snl_tag[3]
	## 保留字
	elif element in symbol_list.symbol_list['reserved'].values():
		return tag.snl_tag[1]
	## 无符号整数
	elif element.isdigit():
		return tag.snl_tag[2]
	else:
		error = 0
		if element[0] == "'" and element[len(element) - 1] == "'":
			return tag.snl_tag[7]
		for x in element:
			if x.isdigit() == False and x.isalpha() == False:
				error = 1
		if error == 0:
			return tag.snl_tag[0]
		elif error == 1:
			print "at line", line, lex_error
			flag = 1
			return None
