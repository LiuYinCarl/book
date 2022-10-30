# parser 流程

测试代码

```python
src = "a = 10"
compile(src, "", "exec")
```

```c
// python.c
// 程序入口
main(int argc, char **argv);

// main.c
// Py_BytesMain 和 Py_Main 的区别
Py_BytesMain(int argc, char **argv);

// 
static int
pymain_main(_PyArgv *args);


int
Py_RunMain(void);

static void
pymain_run_python(int *exitcode);

static int
pymain_run_file(const PyConfig *config);


static int
pymain_run_file_obj(PyObject *program_name, PyObject *filename,
                    int skip_source_first_line);


int
_PyRun_AnyFileObject(FILE *fp, PyObject *filename, int closeit,
                     PyCompilerFlags *flags);

int
_PyRun_SimpleFileObject(FILE *fp, PyObject *filename, int closeit,
                        PyCompilerFlags *flags);

static PyObject *
pyrun_file(FILE *fp, PyObject *filename, int start, PyObject *globals,
           PyObject *locals, int closeit, PyCompilerFlags *flags);


mod_ty
_PyParser_ASTFromFile(FILE *fp, PyObject *filename_ob, const char *enc,
                      int mode, const char *ps1, const char* ps2,
                      PyCompilerFlags *flags, int *errcode, PyArena *arena);

mod_ty
_PyPegen_run_parser_from_file_pointer(FILE *fp, int start_rule, PyObject *filename_ob,
                             const char *enc, const char *ps1, const char *ps2,
                             PyCompilerFlags *flags, int *errcode, PyArena *arena);

void *
_PyPegen_run_parser(Parser *p);

// PEG parser 入口？
void *
_PyPegen_parse(Parser *p);

static mod_ty
file_rule(Parser *p);

mod_ty
_PyPegen_make_module(Parser *p, asdl_stmt_seq *a);

```



```c
// compile.c
// 生成字节码的位置
static PyCodeObject *
assemble(struct compiler *c, int addNone);


// ceval.c
// 执行字节码的位置
PyObject *
PyEval_EvalCode(PyObject *co, PyObject *globals, PyObject *locals);

// 字节码执行位置
PyObject* _Py_HOT_FUNCTION
_PyEval_EvalFrameDefault(PyThreadState *tstate, PyFrameObject *f, int throwflag);
```



## PEG 解析器

1. PEG 解析器原理
2. PEG 解析器Demo
3. PEG 解析器可视化


PEG 解析器的规则中，越特殊的规则应该放在最上面进行匹配，越通用的规则应该放在下面

```
# 错误写法
my_rule:
    | 'if' expression 'then' block
    | 'if' expression 'then' block 'else' block

# 正确写法
my_rule:
    | 'if' expression 'then' block 'else' block
    | 'if' expression 'then' block
```