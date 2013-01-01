# -*- coding:utf-8 -*-
## 自定义的对象：树的结点
class node():
    def is_root(self, judge = 0):    ## 根结点属性
        self.is_root = judge

    def is_terminal(self, token = 0):    ## 终结符属性
        self.is_terminal = token

    def set_node(self, node_value = None, children = [], parent = None):    ## 设置结点信息
        self.node_value = node_value
        self.children = children
        if self.is_root == 1:
            self.parent = None
        else:
			self.parent = parent
			if isinstance(parent, node):
				parent.add_child(self)

    def level(self):    ## 结点在树中的层数
        if self.is_root == 1:
			self.level = 0
        else:
			self.level = self.parent.level + 1

    def get_node(self):    ## 获取结点信息
        return self.node_value, self.children, self.parent

    def refresh_value(self, new_value):    ## 刷新结点
        self.node_value = new_value
        return True

    def drop_child(self, child):    ## 删除子结点
        if child in self.children:
            self.children = filter(lambda x: x != child, self.children)
            return True
        else:
            return False

    def add_child(self, child):    ## 增加子结点
        self.children.append(child)
        return True
