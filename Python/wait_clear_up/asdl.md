## ASDL 论文

ASDL 的目标
1. 足够简单和简洁
2. 可以对现有的一些 IR 进行编码
3. 提供的工具可以将 IR 转换成 C,C++,Java,ML 代码
4. 提供的工具可以生成人类可读的代码
5. 语言特性必须在所有的目标编程语言中具有一种自然的编码

ASDL 的语法限制
1. 类型名必须以小写字母开头
2. 构造器名必须以大写字母开头

一个 ASDL 规则由三个基本结构组成: 类型、构造器和产生式。
一个类型由一系列构造器产生式的枚举组成。



production type
这种限制是不令人满意的，因为它要求描述编写者也为这种类型的单个构造器提供一个名称。为了克服这个问题，ASDL提供了 production type，这些 production type 定义了一个类型，该类型是几个不同类型值的集合。production type 存在限制，因为它们无法递归定义，因为递归 production type 定义不能描述树形结构。

attribute
通常，同一类型的多个构造函数共享一组公共值。为了明确这一点，ASDL包含了一个属性表示法。由于一种类型的所有变体都携带一个属性的值，因此访问它的字段时，无需对不同的构造变量进行区分。属性可以被视为提供了一些有限的继承特性

options
大多数语言提供了特殊的分隔空值(NULL, nil, NONE)的概念。ASDL提供了一种约定，用于指定某些值可以用 "?" (可选)限定符


为什么构造器中不允许 complex type 呢，递归导致无法构造树形语法树？





## 参考资料

CPython ASDL parser 作者
https://eli.thegreenplace.net/2014/06/04/using-asdl-to-describe-asts-in-compilers

https://github.com/chinesehuazhou/guido_blog_translation


asdl parser 的实现在 asdl.py

c code generator 的实现在 asdl_c.py

asdl_c.py 的输入文件为 Python.asdl

输出文件为 Include/Python_ast.c ...

```makefile
$(PYTHON_FOR_REGEN) $(srcdir)/Parser/asdl_c.py \
    $(srcdir)/Parser/Python.asdl \
    -H $(srcdir)/Include/internal/pycore_ast.h.new \
    -I $(srcdir)/Include/internal/pycore_ast_state.h.new \
    -C $(srcdir)/Python/Python-ast.c.new
```



### 调用链分析

```python
# asdl_c.py
def main():
    mod = asdl.parse("Python.asdl")




############################################

class TokenKind:
    """TokenKind is provides a scope for enumerated token kinds."""
    (ConstructorId, TypeId, Equals, Comma, Question, Pipe, Asterisk,
     LParen, RParen, LBrace, RBrace) = range(11)

    operator_table = {
        '=': Equals, ',': Comma,    '?': Question, '|': Pipe,    '(': LParen,
        ')': RParen, '*': Asterisk, '{': LBrace,   '}': RBrace}



# asdl.py
def parser("Python.asdl"):
    parser = ASDLParser() # 创建一个 Parser
    parser.parse()

def tokenize_asdl(buf):
    # 解析一个 Token
    # yield

class ASDLParser:
    def parse(self, buf):
        #
        self._tokenizer = tokenize_asdl(buf)
        #
        self._advance()
        #
        return self._parse_module()

    def _match(self, kind):
        # 1. 检查 self.cur_token.kind 是不是属于 kind
        # 2. 返回 self.cur_token.value
        # 2. 调用 self._advance()

    def _advance(self):
        # 1. 返回上一个 self.cur_token.value
        # 2. 读入下一个 token

    def _parse_module(self):
        # 1. 检查当前解析的文件是不是一个 asdl module
        # 2. 调用 self._parse_definitions() 解析模块内容
        # 3. 返回解析完成的 Module

    def _parse_definitions(self):



```

### 正则表达式分析

```python
# \s  匹配任何Unicode空白字符
# *   对它前面的正则式匹配0到任意次重复， 尽量多的匹配字符串
# \w  匹配Unicode词语的字符，包含了可以构成词语的绝大部分字符，也包括数字和下划线
# +   对它前面的正则式匹配1到任意次重复
# .   在默认模式，匹配除了换行的任意字符
# 所以这个正则表达式匹配的就是任意 单词/注释内容/特殊符号
re.finditer(r'\s*(\w+|--.*|.)', line.strip())


```





