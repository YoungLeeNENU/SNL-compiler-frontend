# -*- coding:utf-8 -*-
## SNL字符表

## 单字符分界符
snl_single_char = {
	'add': "+",
	'minus': "-",
	'multiply': "*",
	'divide': "/",
	'left_sm_col': "(",
	'right_sm_col': ")",
	'left_mid_col': "[",
	'right_mid_col': "]",
	'end': ";",
	'dote': ".",
	'mov_left': "<",
	'env': "=",
	'eof': "EOF",
	'ch_void': " ",
	'colon': ":",    ## 冒号，后加的
	'comma': ",",    ## 逗号，后加的
}

## 字母
snl_letters = {
	'a': "a",    'A': "A",
    'b': "b",    'B': "B",
    'c': "c",    'C': "C",
    'd': "d",    'D': "D",
    'e': "e",    'E': "E",
    'f': "f",    'F': "F",
    'g': "g",    'G': "G",
    'h': "h",    'H': "H",
    'i': "i",    'I': "I",
    'j': "j",    'J': "J",
    'k': "k",    'K': "K",
    'l': "l",    'L': "L",
    'm': "m",    'M': "M",
    'n': "n",    'N': "N",
    'o': "o",    'O': "O",
    'p': "p",    'P': "P",
    'q': "q",    'Q': "Q",
    'r': "r",    'R': "R",
    's': "s",    'S': "S",
    't': "t",    'T': "T",
    'u': "u",    'U': "U",
    'v': "v",    'V': "V",
    'w': "w",    'W': "W",
    'x': "x",    'X': "X",
    'y': "y",    'Y': "Y",
    'z': "z",    'Z': "Z",
}

## 数字
snl_number = {
	'one': "1",
	'two': "2",
	'three': "3",
	'four': "4",
	'five': "5",
	'six': "6",
	'seven': "7",
	'eight': "8",
	'nine': "9",
	'zero': "0",
}

## 保留字
snl_reserved = {
	'PROGRAM': "program",
	'TYPE': "type",
	'INTEGER': "integer",
	'CHAR': "char",
	'ARRAY': "array",
	'OF': "of",
	'RECORD': "record",
	'END': "end",
	'VAR': "var",
	'PROCEDURE': "procedure",
	'BEGIN': "begin",
	'IF': "if",
	'THEN': "then",
    'ELSE': "else",
	'FI': "fi",
	'WHILE': "while",
	'DO': "do",
	'ENDWH': "endwh",
	'READ': "read",
	'WRITE': "write",
	'RETURN': "return",
}

## 字符表字典
symbol_list = {
	'identifier': "ID",    ## 标志符
	'u_int': "INTC",    ## 无符号整数
	'single_char': snl_single_char,    ## 单字符分界符
	'double_char': ":=",    ## 双字符分界符
	'cmt_start': "{",    ## 注释头符
	'cmt_end': "}",    ## 注释结束符
	'ch_start_end': "'",    ## 字符起始和结束符，注意，字符串用
	'ch_array': "..",    ## 数组下标界限符
	'letter': snl_letters,    ## 字母
	'number': snl_number,    ## 数字
	'reserved': snl_reserved,    ## 保留字
}
