# -*- coding:utf-8 -*-
## 递归下降法
## 形成语法分析树，遍历并打印语法分析树，打印的形式是文件树形式
import os
import sys
import lexeme
import grammar
from tree import node
## sys.setrecursionlimit(1000000)

token_list = []    ## token序列
lookahead = []    ## 向前看符号
grammar_node = []    ## 结点序列
space = "|   "    ## 打印树所用的空格

## 非终结符结点的初始化
def nt_init(father, init_node, instance, children):
	if father == 1:
		init_node.is_root(1)    ## 设置为根
		init_node.set_node(instance, [])    ## 结点内容和子结点（空列表）
	else:
		init_node.is_root(0)    ## 非根
		init_node.set_node(instance, [], father)    ## 结点内容，子结点（空列表）和父结点
	grammar_node.append(init_node)    ## 在grammar_node中添加新建的结点

## 终结符结点的初始化
def t_init(father, init_node, instance, children):
	init_node.is_root(0)    ## 非根
	init_node.set_node(instance, children, father)    ## 结点内容，子结点（空列表）和父结点
	grammar_node.append(init_node)    ## 在grammar_node中添加新建的结点

def scan(lexical_out):
	global lookahead, token_list, node
	token_list = lexical_out
	token_list.reverse()    ## 反转，便于pop操作
	lookahead = token_list.pop()    ## 弹出元素
	syntactic_analysis()    ## 进行递归下降的语法分析

def match(t):	 ## 匹配终结符
	global lookahead, token_list, node

	if lookahead[1] == t:
		if token_list != []:
			lookahead = token_list.pop()    ## 弹出下一个token
		return True
	elif lookahead[2] == t and lookahead[1] != t:
		if token_list != []:
			lookahead = token_list.pop()    ## 弹出下一个token
		return True
	else:
		print "At line", lookahead[0], "syntax error!"    ## 错误出现的行号
		print t, "is not", lookahead[1]    ## 错误信息
		sys.exit(0)    ## 退出
		return False

def syntactic_analysis():    ## 开始语法分析
	global lookahead, token_list, node, space

	Program(1)    ## SNL文法

	## 设置结点的层数信息
	for x in grammar_node:
		x.level()

	## 中序遍历结点，并形成文件树
	def scan_tree(head):
		global vector, space
		print space * head.level + str(head.node_value)
		for x in head.get_node()[1]:
			if x.children != []:
				scan_tree(x)
			else:
				print space * x.level + str(x.node_value)

	scan_tree(grammar_node[0])    ## 中序遍历结点，并形成文件树

'''
以下为SNL文法的实现
每个非终结符对应一个函数，参数为其父节点
每个函数先产生非终结符号结点，并进行非终结符号的初始化
然后根据具体的文法
进行递归下降的语法分析
遇到终结符号，调用match函数进行匹配
遇到非终结符号，调用非终结符号对应的函数继续进行语法分析
'''

def Program(father):
	global lookahead, token_list, node

	PROGRAM = node()
	nt_init(father, PROGRAM, "Program", [])

	ProgramHead(PROGRAM)    ## 第一步
	DeclarePart(PROGRAM)    ## 第二步
	ProgramBody(PROGRAM)    ## 第三步

def ProgramHead(father):
	global lookahead, token_list, node

	PROGRAMHEAD = node()
	nt_init(father, PROGRAMHEAD, "ProgramHead", [])

	if match("program"):
		T_PROGRAM = node()
		t_init(PROGRAMHEAD, T_PROGRAM, "program", [])
	ProgramName(PROGRAMHEAD)

def ProgramName(father):
	global lookahead, token_list, node

	PROGRAMNAME = node()
	nt_init(father, PROGRAMNAME, "ProgramName", [])

	if match("id"):
		T_ID = node()
		t_init(PROGRAMNAME, T_ID, lookahead[1], [])

def DeclarePart(father):
	global lookahead, token_list, node

	DECLAREPART = node()
	nt_init(father, DECLAREPART, "DeclarePart", [])

	TypeDecPart(DECLAREPART)
	VarDecPart(DECLAREPART)
	ProcDecpart(DECLAREPART)

def TypeDecPart(father):
	global lookahead, token_list, node

	TYPEDECPART = node()
	nt_init(father, TYPEDECPART, "TypeDecPart", [])

	TypeDec(TYPEDECPART)

def TypeDec(father):
	global lookahead, token_list, node

	TYPEDEC = node()
	nt_init(father, TYPEDEC, "TypeDec", [])

	if lookahead[1] == "type":
		if match("type"):
			T_TYPE = node()
			t_init(TYPEDEC, T_TYPE, "type", [])
		TypeDecList(TYPEDEC)
	else:
		## print "ε"
		T_VOID = node()
		t_init(TYPEDEC, T_VOID, "ε", [])

def TypeDecList(father):
	global lookahead, token_list, node

	TYPEDECLIST = node()
	nt_init(father, TYPEDECLIST, "TypeDecList", [])

	TypeId(TYPEDECLIST)
	if match("="):
		T_EQUAL = node()
		t_init(TYPEDECLIST, T_EQUAL, "=", [])
	TypeDef(TYPEDECLIST)
	if match(";"):
		SEMICOLON = node()
		t_init(TYPEDECLIST, SEMICOLON, ";", [])
	TypeDecMore(TYPEDECLIST)

def TypeDecMore(father):
	global lookahead, token_list, node

	TYPEDECMORE = node()
	nt_init(father, TYPEDECMORE, "TypeDecMore", [])

	if lookahead[2] == "id":
		TypeDecList(TYPEDECMORE)
	else:
		T_VOID = node()
		t_init(TYPEDECMORE, T_VOID, "ε", [])

def TypeId(father):
	global lookahead, token_list, node

	TYPEID = node()
	nt_init(father, TYPEID, "TypeId", [])

	if match("id"):
		T_ID = node()
		t_init(TYPEID, T_ID, lookahead[1], [])

def TypeDef(father):    ## 需要回溯
	global lookahead, token_list, node

	TYPEDEF = node()
	nt_init(father, TYPEDEF, "TypeDef", [])

	if lookahead[2] == "id":
		if match("id"):
			T_ID = node()
			t_init(TYPEDEF, T_ID, lookahead[1], [])
	elif lookahead[1] == "integer" or lookahead[1] == "char":
		BaseType(TYPEDEF)
	else:
		StructureType(TYPEDEF)

def BaseType(father):
	global lookahead, token_list, node

	BASETYPE = node()
	nt_init(father, BASETYPE, "BaseType", [])

	if match("integer"):
		T_INTEGER = node()
		t_init(BASETYPE, T_INTEGER, "integer", [])
	elif match("char"):
		T_CHAR = node()
		t_init(BASETYPE, T_CHAR, "char", [])

def StructureType(father):    ## 需要回溯
	global lookahead, token_list, node

	STRUCTURETYPE = node()
	nt_init(father, STRUCTURETYPE, "StructureType", [])

	if lookahead[1] == "array":
		ArrayType(STRUCTURETYPE)
	else:
		RecType(STRUCTURETYPE)

def ArrayType(father):
	global lookahead, token_list, node

	ARRAYTYPE = node()
	nt_init(father, ARRAYTYPE, "ArrayType", [])

	if match("array"):
		T_ARRAY = node()
		t_init(ARRAYTYPE, T_ARRAY, "array", [])
	if match("["):
		T_LEFT_BRACKET = node()
		t_init(ARRAYTYPE, T_LEFT_BRACKET, "[", [])
	Low(ARRAYTYPE)
	if match(".."):
		T_ARRAYFIELD = node()
		t_init(ARRAYTYPE, T_ARRAYFIELD, "..", [])
	Top(ARRAYTYPE)
	if match("]"):
		T_RIGHT_BRACKET = node()
		t_init(ARRAYTYPE, T_RIGHT_BRACKET, "]", [])
	if match("of"):
		T_OF = node()
		t_init(ARRAYTYPE, T_OF, "of", [])
	BaseType(ARRAYTYPE)

def Low(father):
	global lookahead, token_list, node

	LOW = node()
	nt_init(father, LOW, "Low", [])

	if match("intc"):
		T_INTC = node()
		t_init(LOW, T_INTC, lookahead[1], [])

def Top(father):
	global lookahead, token_list, node

	TOP = node()
	nt_init(father, TOP, "Top", [])

	if match("intc"):
		T_INTC = node()
		t_init(TOP, T_INTC, lookahead[1], [])

def RecType(father):
	global lookahead, token_list, node

	RECTYPE = node()
	nt_init(father, RECTYPE, RecType, [])

	if match("record"):
		T_RECORD = node()
		t_init(RECTYPE, T_RECORD, "record", [])
	FieldDecList(RECTYPE)
	if match("end"):
		T_END = node()
		t_init(RECTYPE, T_END, "end", [])

def FieldDecList(father):
	global lookahead, token_list, node

	FIELDDECLIST = node()
	nt_init(father, FIELDDECLIST, "FieldDecList", [])

	if lookahead[1] == "array":
		ArrayType(FIELDDECLIST)
		IdList(FIELDDECLIST)
		if match(";"):
			T_SEMICOLON = node()
			t_init(FIELDDECLIST, T_SEMICOLON, ";", [])
		FieldDecMore(FIELDDECLIST)
	else:
		BaseType(FIELDDECLIST)
		IdList(FIELDDECLIST)
		if match(";"):
			T_SEMICOLON = node()
			t_init(FIELDDECLIST, T_SEMICOLON, ";", [])
		FieldDecMore(FIELDDECLIST)

def FieldDecMore(father):
	global lookahead, token_list, node

	FIELDDECMORE = node()
	nt_init(father, FIELDDECMORE, "FieldDecList", [])

	if lookahead[1] == "integer":
		FieldDecList(FIELDDECMORE)
	elif lookahead[1] == "char":
		FieldDecList(FIELDDECMORE)
	else:
		T_VOID = node()
		t_init(FIELDDECMORE, T_VOID, "ε", [])

def IdList(father):
	global lookahead, token_list, node

	IDLIST = node()
	nt_init(father, IDLIST, "IdList", [])

	if match("id"):
		T_ID = node()
		t_init(IDLIST, T_ID, lookahead[1], [])
	IdMore(IDLIST)

def IdMore(father):
	global lookahead, token_list, node

	IDMORE = node()
	nt_init(father, IDMORE, "IdMore", [])

	if lookahead[1] == ",":
		if match(","):
			T_COMMA = node()
			t_init(IDMORE, T_COMMA, ",", [])
		IdList(IDMORE)
	else:
		T_VOID = node()
		t_init(IDMORE, T_VOID, "ε", [])

def VarDecPart(father):
	global lookahead, token_list, node

	VARDECPART = node()
	nt_init(father, VARDECPART, "VarDecPart", [])

	if lookahead[1] == "var":
		VarDec(VARDECPART)
	else:
		T_VOID = node()
		t_init(VARDECPART, T_VOID, "ε", [])

def VarDec(father):
	global lookahead, token_list, node

	VARDEC = node()
	nt_init(father, VARDEC, "VarDec", [])

	if match("var"):
		T_VAR = node()
		t_init(VARDEC, T_VAR, "var", [])
	VarDecList(VARDEC)

def VarDecList(father):
	global lookahead, token_list, node

	VARDECLIST = node()
	nt_init(father, VARDECLIST, "VarDecList", [])

	TypeDef(VARDECLIST)
	VarIdList(VARDECLIST)
	if match(";"):
		T_SEMICOLON = node()
		t_init(VARDECLIST, T_SEMICOLON, ";", [])
	VarDecMore(VARDECLIST)

def VarDecMore(father):
	global lookahead, token_list, node

	VARDECMORE = node()
	nt_init(father, VARDECMORE, "VarDecMore", [])

	if lookahead[2] == "id":
		VarDecList(VARDECMORE)
	elif lookahead[1] in ["integer", "array", "char"]:
		VarDecList(VARDECMORE)
	else:
		T_VOID = node()
		t_init(VARDECMORE, T_VOID, "ε", [])

def VarIdList(father):
	global lookahead, token_list, node

	VARIDLIST = node()
	nt_init(father, VARIDLIST, "VarIdList", [])

	if match("id"):
		T_ID = node()
		t_init(VARIDLIST, T_ID, lookahead[1], [])
	VarIdMore(VARIDLIST)

def VarIdMore(father):
	global lookahead, token_list, node

	VARIDMORE = node()
	nt_init(father, VARIDMORE, "VarIdMore", [])

	if lookahead[1] == ",":
		if match(","):
			T_COMMA = node()
			t_init(VARIDMORE, T_COMMA, ",", [])
		VarIdList(VARIDMORE)
	else:
		T_VOID = node()
		t_init(VARIDMORE, T_VOID, "ε", [])

def ProcDecpart(father):
	global lookahead, token_list, node

	PROCDECPART = node()
	nt_init(father, PROCDECPART, "ProcDecpart", [])

	if lookahead[1] == "procedure":
		ProcDec(PROCDECPART)
	else:
		T_VOID = node()
		t_init(PROCDECPART, T_VOID, "ε", [])

def ProcDec(father):
	global lookahead, token_list, node

	PROCDEC = node()
	nt_init(father, PROCDEC, "ProcDec", [])

	if match("procedure"):
		T_PROCEDURE = node()
		t_init(PROCDEC, T_PROCEDURE, "procedure", [])
	ProcName(PROCDEC)
	if match("("):
		T_LEFT_SM_COL = node()
		t_init(PROCDEC, T_LEFT_SM_COL, "(", [])
	ParamList(PROCDEC)
	if match(")"):
		T_RIGHT_SM_COL = node()
		t_init(PROCDEC, T_RIGHT_SM_COL, ")", [])
	if match(";"):
		T_SEMICOLON = node()
		t_init(PROCDEC, T_SEMICOLON, ";", [])
	ProcDecPart(PROCDEC)
	ProcBody(PROCDEC)
	ProcDecMore(PROCDEC)

def ProcDecMore(father):
	global lookahead, token_list, node

	PROCDECMORE = node()
	nt_init(father, PROCDECMORE, "ProcDecMore", [])

	if lookahead[1] == "procedure":
		ProcDec(PROCDECMORE)
	else:
		T_VOID = node()
		t_init(PROCDECMORE, T_VOID, "ε", [])

def ProcName(father):
	global lookahead, token_list, node

	PROCNAME = node()
	nt_init(father, PROCNAME, "ProcName", [])

	if match("id"):
		T_ID = node()
		t_init(PROCNAME, T_ID, lookahead[1], [])

def ParamList(father):
	global lookahead, token_list, node

	PARAMLIST = node()
	nt_init(father, PARAMLIST, "ParamList", [])

	if lookahead[2] == "id":
		ParamDecList(PARAMLIST)
	elif lookahead[1] in ["char", "integer", "array"]:
		ParamDecList(PARAMLIST)
	else:
		T_VOID = node()
		t_init(PARAMLIST, T_VOID, "ε", [])

def ParamDecList(father):
	global lookahead, token_list, node

	PARAMDECLIST = node()
	nt_init(father, PARAMDECLIST, "ParamDecList", [])

	Param(PARAMDECLIST)
	ParamMore(PARAMDECLIST)

def ParamMore(father):
	global lookahead, token_list, node

	PARAMMORE = node()
	nt_init(father, PARAMMORE, "ParamMore", [])

	if lookahead[1] == ";":
		if match(";"):
			T_SEMICOLON = node()
			t_init(PARAMMORE, T_SEMICOLON, ";", [])
		ParamDecList(PARAMMORE)
	else:
		T_VOID = node()
		t_init(PARAMMORE, T_VOID, "ε", [])

def Param(father):
	global lookahead, token_list, node

	PARAM = node()
	nt_init(father, PARAM, "Param", [])

	if lookahead[1] == "var":
		if match("var"):
			T_VAR = node()
			t_init(PARAM, T_VAR, "var", [])
		TypeDef(PARAM)
		FormList(PARAM)
	else:
		TypeDef(PARAM)
		FormList(PARAM)

def FormList(father):
	global lookahead, token_list, node

	FORMLIST = node()
	nt_init(father, FORMLIST, "FormList", [])

	if match("id"):
		T_ID = node()
		t_init(FORMLIST, T_ID, lookahead[1], [])
	FidMore(FORMLIST)

def FidMore(father):
	global lookahead, token_list, node

	FIDMORE = node()
	nt_init(father, FIDMORE, "FidMore", [])

	if lookahead[1] == ",":
		if match(","):
			T_COMMA = node()
			t_init(FIDMORE, T_COMMA, ",", [])
		FormList(FIDMORE)
	else:
		T_VOID = node()
		t_init(FIDMORE, T_VOID, "ε", [])

def ProcDecPart(father):
	global lookahead, token_list, node

	PROCDECPART = node()
	nt_init(father, PROCDECPART, "ProcDecPart", [])

	DeclarePart(PROCDECPART)

def ProcBody(father):
	global lookahead, token_list, node

	PROCBODY = node()
	nt_init(father, PROCBODY, "ProcBody", [])

	ProgramBody(PROCBODY)

def ProgramBody(father):
	global lookahead, token_list, node

	PROGRAMBODY = node()
	nt_init(father, PROGRAMBODY, "ProgramBody", [])

	if match("begin"):
		T_BRGIN = node()
		t_init(PROGRAMBODY, T_BRGIN, "begin", [])
	StmList(PROGRAMBODY)
	if match("end"):
		T_END = node()
		t_init(PROGRAMBODY, T_END, "end", [])

def StmList(father):
	global lookahead, token_list, node

	STMLIST = node()
	nt_init(father, STMLIST, "StmList", [])

	Stm(STMLIST)
	StmMore(STMLIST)

def StmMore(father):
	global lookahead, token_list, node

	STMMORE = node()
	nt_init(father, STMMORE, "StmMore", [])

	if lookahead[1] == ";":
		if match(";"):
			T_SEMICOLON = node()
			t_init(STMMORE, T_SEMICOLON, ";", [])
		StmList(STMMORE)
	else:
		T_VOID = node()
		t_init(STMMORE, T_VOID, "ε", [])

def Stm(father):    ## 回溯
	global lookahead, token_list, node

	STM = node()
	nt_init(father, STM, "Stm", [])

	if lookahead[2] == "id":
		if match("id"):
			T_ID = node()
			t_init(STM, T_ID, lookahead[1], [])
		AssCall(STM)
	elif lookahead[1] == "return":
		ReturnStm(STM)
	elif lookahead[1] == "write":
		OutputStm(STM)
	elif lookahead[1] == "read":
		InputStm(STM)
	elif lookahead[1] == "while":
		LoopStm(STM)
	elif lookahead[1] == "if":
		ConditionalStm(STM)

def AssCall(father):    ## 回溯
	global lookahead, token_list, node

	ASSCALL = node()
	nt_init(father, ASSCALL, "AssCall", [])

	if lookahead[1] == "(":
		CallStmRest(ASSCALL)
	else:
		AssignmentRest(ASSCALL)

def AssignmentRest(father):
	global lookahead, token_list, node

	ASSIGNMENTREST = node()
	nt_init(father, ASSIGNMENTREST, "AssignmentRest", [])

	VariMore(ASSIGNMENTREST)
	if match(":="):
		T_ASSIGNMENT = node()
		t_init(ASSIGNMENTREST, T_ASSIGNMENT, ":=", [])
	Exp(ASSIGNMENTREST)

def ConditionalStm(father):
	global lookahead, token_list, node

	CONDITIONALSTM = node()
	nt_init(father, CONDITIONALSTM, "ConditionalStm", [])

	if match("if"):
		T_IF = node()
		t_init(CONDITIONALSTM, T_IF, "if", [])
	RelExp(CONDITIONALSTM)
	if match("then"):
		T_THEN = node()
		t_init(CONDITIONALSTM, T_THEN, "then", [])
	StmList(CONDITIONALSTM)
	if match("else"):
		T_ELSE = node()
		t_init(CONDITIONALSTM, T_ELSE, "else", [])
	StmList(CONDITIONALSTM)
	if match("fi"):
		T_FI = node()
		t_init(CONDITIONALSTM, T_FI, "fi", [])

def LoopStm(father):
	global lookahead, token_list, node

	LOOPSTM = node()
	nt_init(father, LOOPSTM, "LoopStm", [])

	if match("while"):
		T_WHILE = node()
		t_init(LOOPSTM, T_WHILE, "while", [])
	RelExp(LOOPSTM)
	if match("do"):
		T_DO = node()
		t_init(LOOPSTM, T_DO, "do", [])
	StmList(LOOPSTM)
	if match("endwh"):
		T_ENDWH = node()
		t_init(LOOPSTM, T_ENDWH, "endwh", [])

def InputStm(father):
	global lookahead, token_list, node

	INPUTSTM = node()
	nt_init(father, INPUTSTM, "InputStm", [])

	if match("read"):
		T_READ = node()
		t_init(INPUTSTM, T_READ, "read", [])
	if match("("):
		T_LEFT_SM_COL = node()
		t_init(INPUTSTM, T_LEFT_SM_COL, "(", [])
	Invar(INPUTSTM)
	if match(")"):
		T_RIGHT_SM_COL = node()
		t_init(INPUTSTM, T_RIGHT_SM_COL, ")", [])

def Invar(father):
	global lookahead, token_list, node

	INVAR = node()
	nt_init(father, INVAR, "Invar", [])

	if match("id"):
		T_ID = node()
		t_init(INVAR, T_ID, lookahead[1], [])

def OutputStm(father):
	global lookahead, token_list, node

	OUTPUTSTM = node()
	nt_init(father, OUTPUTSTM, "OutputStm", [])

	if match("write"):
		T_WRITE = node()
		t_init(OUTPUTSTM, T_WRITE, "write", [])
	if match("("):
		T_LEFT_SM_COL = node()
		t_init(OUTPUTSTM, T_LEFT_SM_COL, "(", [])
	Exp(OUTPUTSTM)
	if match(")"):
		T_RIGHT_SM_COL = node()
		t_init(OUTPUTSTM, T_RIGHT_SM_COL, ")", [])

def ReturnStm(father):
	global lookahead, token_list, node

	RETURNSTM = node()
	nt_init(father, RETURNSTM, "ReturnStm", [])

	if match("return"):
		T_RETURN = node()
		t_init(RETURNSTM, T_RETURN, "return", [])

def CallStmRest(father):
	global lookahead, token_list, node

	CALLSTMTREST = node()
	nt_init(father, CALLSTMTREST, "CallStmTRest", [])

	if match("("):
		T_LEFT_SM_COL = node()
		t_init(CALLSTMTREST, T_LEFT_SM_COL, "(", [])
	ActParamList(CALLSTMTREST)
	if match(")"):
		T_RIGHT_SM_COL = node()
		t_init(CALLSTMTREST, T_RIGHT_SM_COL, ")", [])

def ActParamList(father):
	global lookahead, token_list, node

	ACTPARAMLIST = node()
	nt_init(father, ACTPARAMLIST, "ActParamList", [])

	if lookahead[1] == "(":
		Exp(ACTPARAMLIST)
		ActParamMore(ACTPARAMLIST)
	elif lookahead[2] in ["id", "intc"]:
		Exp(ACTPARAMLIST)
		ActParamMore(ACTPARAMLIST)
	else:
		T_VOID = node()
		t_init(ACTPARAMLIST, T_VOID, "ε", [])

def ActParamMore(father):
	global lookahead, token_list, node

	ACTPARAMMORE = node()
	nt_init(father, ACTPARAMMORE, "ActParamMore", [])

	if lookahead[1] == ",":
		if match(","):
			T_COMMA = node()
			t_init(ACTPARAMMORE, T_COMMA, ",", [])
		ActParamList(ACTPARAMMORE)
	else:
		T_VOID = node()
		t_init(ACTPARAMMORE, T_VOID, "ε", [])

def RelExp(father):
	global lookahead, token_list, node

	RELEXP = node()
	nt_init(father, RELEXP, "RelExp", [])

	Exp(RELEXP)
	OtherRelE(RELEXP)

def OtherRelE(father):
	global lookahead, token_list, node

	OTHERRELE = node()
	nt_init(father, OTHERRELE, "OtherRelE", [])

	CmpOp(OTHERRELE)
	Exp(OTHERRELE)

def Exp(father):
	global lookahead, token_list, node

	EXP = node()
	nt_init(father, EXP, "Exp", [])

	Term(EXP)
	OtherTerm(EXP)

def OtherTerm(father):
	global lookahead, token_list, node

	OTHERTERM = node()
	nt_init(father, OTHERTERM, "OtherTerm", [])

	if lookahead[1] in ["+", "-"]:
		AddOp(OTHERTERM)
		Exp(OTHERTERM)
	else:
		T_VOID = node()
		t_init(OTHERTERM, T_VOID, "ε", [])

def Term(father):
	global lookahead, token_list, node

	TERM = node()
	nt_init(father, TERM, "TERM", [])

	Factor(TERM)
	OtherFactor(TERM)

def OtherFactor(father):
	global lookahead, token_list, node

	OTHERFACTOR = node()
	nt_init(father, OTHERFACTOR, "OtherFactor", [])

	if lookahead[1] in ["*", "/"]:
		MultOp(OTHERFACTOR)
		Term(OTHERFACTOR)
	else:
		T_VOID = node()
		t_init(OTHERFACTOR, T_VOID, "ε", [])

def Factor(father):
	global lookahead, token_list, node

	FACTOR = node()
	nt_init(father, FACTOR, "Factor", [])

	if lookahead[1] == "(":
		if match("("):
			T_LEFT_SM_COL = node()
			t_init(FACTOR, T_LEFT_SM_COL, "(", [])
		Exp(FACTOR)
		if match(")"):
			T_RIGHT_SM_COL = node()
			t_init(FACTOR, T_RIGHT_SM_COL, ")", [])
	elif lookahead[2] == "intc":
		if match("intc"):
			T_INTC = node()
			t_init(FACTOR, T_INTC, lookahead[1], [])
	else:
		Variable(FACTOR)

def Variable(father):
	global lookahead, token_list, node

	VARIABLE = node()
	nt_init(father, VARIABLE, "Variable", [])

	if match("id"):
		T_ID = node()
		t_init(VARIABLE, T_ID, lookahead[1], [])
	VariMore(VARIABLE)

def VariMore(father):
	global lookahead, token_list, node

	VARIMORE = node()
	nt_init(father, VARIMORE, "VariMore", [])

	if lookahead[1] == "[":
		if match("["):
			T_LEFT_BRACKET = node()
			t_init(VARIMORE, T_LEFT_BRACKET, "[", [])
		Exp(VARIMORE)
		if match("]"):
			T_RIGHT_BRACKET = node()
			t_init(VARIMORE, T_RIGHT_BRACKET, "]", [])
	elif lookahead[1] == ".":
		if match("."):
			T_DOTE = node()
			t_init(VARIMORE, T_DOTE, ".", [])
		FieldVar(VARIMORE)
	else:
		T_VOID = node()
		t_init(VARIMORE, T_VOID, "ε", [])

def FieldVar(father):
	global lookahead, token_list, node

	FIELDVAR = node()
	nt_init(father, FIELDVAR, "FieldVar", [])

	if match("id"):
		T_ID = node()
		t_init(FIELDVAR, T_ID, lookahead[1], [])
	FieldVarMore(FIELDVAR)

def FieldVarMore(father):
	global lookahead, token_list, node

	FIELDVARMORE = node()
	nt_init(father, FIELDVARMORE, "FieldVarMore", [])

	if lookahead[1] == "[":
		if match("["):
			T_LEFT_BRACKET = node()
			t_init(FIELDVARMORE, T_LEFT_BRACKET, "[", [])
		Exp(FIELDVARMORE)
		if match("]"):
			T_RIGHT_BRACKET = node()
			t_init(FIELDVARMORE, T_RIGHT_BRACKET, "]", [])
	else:
		T_VOID = node()
		t_init(FIELDVARMORE, T_VOID, "ε", [])

def CmpOp(father):
	global lookahead, token_list, node

	CMPOP = node()
	nt_init(father, CMPOP, "CmpOp", [])

	if lookahead[1] == "<":
		if match("<"):
			T_SMALL = node()
			t_init(CMPOP, T_SMALL, "<", [])
	elif lookahead[1] == "=":
		if match("="):
			T_EQUAL = node()
			t_init(CMPOP, T_EQUAL, "=", [])

def AddOp(father):
	global lookahead, token_list, node

	ADDOP = node()
	nt_init(father, ADDOP, "AddOp", [])

	if lookahead[1] == "+":
		if match("+"):
			T_ADD = node()
			t_init(ADDOP, T_ADD, "+", [])
	elif lookahead[1] == "-":
		if match("-"):
			T_SUB = node()
			t_init(ADDOP, T_SUB, "-", [])

def MultOp(father):
	global lookahead, token_list, node

	MULTOP = node()
	nt_init(father, MULTOP, "MultOp", [])

	if lookahead[1] == "*":
		if match("*"):
			T_MUL = node()
			t_init(MULTOP, T_MUL, "*", [])
	elif lookahead[1] == "/":
		if match("/"):
			T_DIV = node()
			t_init(MULTOP, T_DIV, "/", [])
