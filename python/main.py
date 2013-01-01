# -*- coding:utf-8 -*-
## SNL编译器前端
import sys
import symbol_list    ## 字符表
import read    ## 读文件
import lexeme    ## 词法分析
import de_comment    ## 去掉注释
import r_d_p    ## 递归下降法

## 读取文件
source = read.read_file(sys.argv[1])

## 添加末尾的EOF
## source = source + " EOF"

## 去掉注释
processed = de_comment.de_comment(source)

## 把词法分析后的结果存入result列表中
result = lexeme.slice(processed)

## 词法分析输出部分
## 创建名为output的文件并把结果输入到文件中
output = open('lexical_analysis.txt', 'w')
for item in result:
    output.write("%s\n" % item)

## 扫描token序列
r_d_p.scan(result)
