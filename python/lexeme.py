# -*- coding:utf-8 -*-
## 词法分析
import re
import sys
import tag
import error
import de_comment    ## 去掉注释
import symbol_list    ## 字符表

lexem = []    ## 词法单元的列表
element = ""    ## 每个词素
line = 1    ## 行号
i = 0    ## 计数器
jmp = 0
stack = []
pop_out = ""
ch_stack = []

## 添加词素
def add_element(element):
	if element != "":
		info = []
		info.append(line)
		info.append(element)
		info.append(error.error_sence(element, line))
		lexem.append(info)

## 分片操作
def slice(source):
	global lexem, element, line, i, stack, jmp, stack, pop_out, ch_stack

	for x in source:
		## 换行符
		if x == "\n":
			add_element(element)
			line += 1
			element = ""

			## 制表符和空格
		elif x == "\t" or x == " ":
			add_element(element)
			element = ""

			## 字符
		elif x == "'":
			add_element(element)
			element = ""
			if (source[i + 1].isalpha() or source[i + 1].isdigit()) and source[i + 2] == ",":
				element = "'" + element
			else:
				add_element(x)

		elif x in symbol_list.symbol_list['single_char'].values():
			add_element(element)
			## 处理":="
			if x == ":" and source[i + 1] == "=":
				jmp = 1
				element = ""
				tmp = ":="
				add_element(tmp)
			elif x == "=":
				if jmp == 1:
					jmp = 0
				else:
					element = ""
					tmp = x
					add_element(tmp)
				## 用栈处理".."
			elif x == ".":
				element = ""
				stack.append(x)
				if len(stack) == 2:
					for x in stack[::-1]:
						pop_out = pop_out + x
					stack = []
					add_element(pop_out)
					pop_out = ""
				if len(stack) == 1 and source[i + 1] != ".":
					for x in stack[::-1]:
						pop_out = pop_out + x
					stack = []
					add_element(pop_out)
					pop_out = ""
				## 其余情况
			else:
				element = ""
				tmp = x
				add_element(tmp)

				## 剩余的注释符
		elif x == symbol_list.symbol_list['cmt_start'] or x == symbol_list.symbol_list['cmt_end']:
			add_element(element)
			element = ""
			tmp = x
			add_element(tmp)

			## 标志符
		else:
			element = element + x
		i += 1
	add_element(element)

	if error.flag == 1:
		sys.exit(0)

	return lexem
