# -*- coding:utf-8 -*-
## SNL上下文无关文法
## 大写和符号为非终结符，小写为终极符

## 程序头
SNL_PROGRAM_HEAD = {
	"PROGRAMHEAD": "program PROGRAMNAME",
	"PROGRAMNAME": "id",
}

## 类型声明
SNL_TYPEDEF = {
	"TYPEDECPART": [None,
					"TYPEDEC"],
	"TYPEDEC": "type TYPEDECLIST",
	"TYPEDECLIST": "TYPEID = TYPEDEF;TYPEDECMORE",
	"TYPEDECMORE": [None,
					"TYPEDECLIST"],
	"TYPEID": "id",
}

## 类型
SNL_TYPE = {
	"TYPEDEF": ["BASETYPE",
				"STRUCTURETYPE",
				"id"],
	"BASETYPE": ["integer",
				 "char"],
	"STRUCTURETYPE": ["ARRAYTYPE",
					  "RECTYPE"],
	"ARRAYTYPE": "array [LOW..TOP] of BASETYPE",
	"LOW": "intc",
	"TOP": "intc",
	"RECTYPE": "record FIELDDECLIST end",
	"FIELDDECLIST": ["BASETYPE IDLIST;FIELDDECMORE",
					 "ARRAYTYPE IDLIST;FIELDDECMORE"],
	"FIELDDECMORE": [None,
					 "FIELDDECLIST"],
	"IDLIST": "id IDMORE",
	"IDMORE": [None,
			   ",IDLIST"],
}

## 变量声明
SNL_VARDEF = {
	"VARDECPART": [None,
				   "VARDEC"],
	"VARDEC": "var VARDECLIST",
	"VARDECLIST": "TYPEDEF VARIDLIST;VARDECMORE",
	"VARDECMORE": [None,
				   "VARDECLIST"],
	"VARIDLIST": "id VARIDMORE",
	"VARIDMORE": [None,
				  ",VARIDLIST"],
}

## 过程声明
SNL_PROCDEF = {
	"PROCDECPART": [None,
					"PROCDEC"],
	"PROCDEC": '''procedure
PROCNAME(PARAMLIST);
PROCDECPART
PROCBODY
PROCDECMORE''',
	"PROCDECMORE":[None,
				   "PROCDEC"],
	"PROCNAME": "id",
}

## 参数声明
SNL_PARAMDEF = {
	"PARAMLIST": [None,
				  "PARAMDECLIST"],
	"PARAMDECLIST": "PARAM PARAMMORE",
	"PARAMMORE": [None,
				  ";PARAMDECLIST"],
	"PARAM": ["TYPEDEF FORMLIST",
			  "var TYPEDEF FORMLIST"],
	"FORMLIST": "id FIDMORE",
	"FIDMORE": [None,
				",FORMLIST"],
}

## 语句序列
SNL_STMLIST = {
	"STMLIST": "STM STMMORE",
	"STMMORE": [None,
				";STMLIST"],
}

## 语句
SNL_STM = {
	"STM": ["CONDITIONALSTM",
			"LOOPSTM",
			"INPUTSTM",
			"OUTPUTSTM",
			"RETURNSTM",
			"id ASSCALL"],
	"ASSCALL": ["ASSIGNMENTREST",
				"CALLSTMREST"],
}

## 输入语句
SNL_INPUTSTM = {
	"INPUTSTM": "read (INVAR)",
	"INVAR": "id",
}

## 过程调用语句
SNL_CALL = {
	"CALLSTMREST": "(ACTPARAMLIST)",
	"ACTPARAMLIST": [None,
					 "EXP ACTPARAMMORE"],
	"ACTPARAMMORE": [None,
					 ",ACTPARAMLIST"],
}

## 条件表达式
SNL_COND = {
	"RELEXP": "EXP OTHERRELE",
	"OTHERRELE": "CMPOP EXP",
}

## 算术表达式
SNL_ALGO = {
	"EXP": "TERM OTHERTERM",
	"OTHERTERM": [None,
				  "ADDOP EXP"],
}

## 项
SNL_ITEM = {
	"TERM": "FACTOR OTHERFACTOR",
	"OTHERFACTOR": [None,
					"MULTOP TERM"],
}

## 因子
SNL_ELEMENT = {
	"FACTOR": ["(EXP)",
			   "intc",
			   "VARIABLE"],
	"VARIABLE": "id VARIMORE",
	"VARIMORE": [None,
				 "[Exp]",
				 ".FIELDVAR"],
	"FIELDVAR": "id FIELDVARMORE",
	"FIELDVARMORE": [None,
					 "[EXP]"],
	"CMPOP": ["<",
			  "="],
	"ADDOP": ["+",
			  "-"],
	"MULTOP": ["*",
			   "/"],
}

## SNL的上下文无关文法
SNL_GRAMMAR = {
	"PROGRAM": "PROGRAMHEAD DECLAREPART PROGRAMBODY",    ## 0 总程序，无左递归
	"DIC_PROGRAMHEAD": SNL_PROGRAM_HEAD,    ## 1 程序头
	"DECLAREPART": "TYPEDECPART VARDECPART PROCDECPART",    ## 2 程序声明
	"DIC_TYPEDEF": SNL_TYPEDEF,    ## 3 类型声明
	"DIC_TYPE": SNL_TYPE,    ## 4 类型
	"DIC_VARDEF": SNL_VARDEF,    ## 5 变量声明
	"DIC_PROCDEF": SNL_PROCDEF,    ## 6 过程声明
	"DIC_PARAMDEF": SNL_PARAMDEF,    ## 7 参数声明
	"PROCDECPART": "DECLAREPART",    ## 8 过程中的声明部分
	"PROCBODY": "PROGRAMBODY",    ## 9 过程体
	"PROGRAMBODY": "begin STMLIST end",    ## 10 主程序体
	"DIC_STMLIST": SNL_STMLIST,    ## 11 语句序列
	"DIC_STM": SNL_STM,    ## 12 语句
	"ASSIGNMENTREST": "VARIMORE := EXP",	 ## 13 赋值语句
	"CONDITIONALSTM": "if RELEXP then STMLIST else STMLIST fi",    ## 14 条件语句
	"LOOPSTM": "while RELEXP do STMLIST endwh",    ## 15 循环语句
	"DIC_INPUTSTM": SNL_INPUTSTM,    ## 16 输入语句
	"OUTPUTSTM": "write(EXP)",    ## 17 输出语句
	"RETURNSTM": "return",    ## 18 返回语句
	"DIC_CALL": SNL_CALL,    ## 19 过程调用语句
	"DIC_COND": SNL_COND,    ## 20 条件表达式
	"DIC_ALGO": SNL_ALGO,    ## 21 算术表达式
	"DIC_ITEM": SNL_ITEM,    ## 22 项
	"DIC_ELEMENT": SNL_ELEMENT,    ## 23 因子
}
