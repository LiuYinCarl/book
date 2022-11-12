# Real World OCaml 2ed note

[online ebook](https://dev.realworldocaml.org/)


## 配置 OCaml 环境

[官方文档](https://v2.ocaml.org/docs/install.html)

```bash
# 安装 OCaml 包管理器
apt install opam
# 初始化环境
opam init
eval $(opam env)
# 安装某个版本的 OCaml 编译器
opam switch create 4.14.0
eval $(opam env)
# 检查版本
which ocaml
ocaml -version
```

实际上我安装 opam 2.1.2 的时候只执行到了 `opam init` 这一步 opam 管理器就已经帮我安装好了 ocaml 4.13.1 编译器，
也就不用进行后续的步骤。

[OCaml 开发工具配置](https://ocaml.org/docs/up-and-running#setting-up-development-tools)

```bash
opam install dune merlin ocaml-lsp-server odoc ocamlformat utop dune-release
```

如果使用 Emacs 编辑器，那么可以安装如下拓展

```bash
opam install tuareg
```

# 安装常用库

学习 Real World OCaml 这本书的时候需要用到。

```
opam install core
```


## What's the difference between include, require and open in OCaml?

[StackOverflow 问题链接](https://stackoverflow.com/questions/42631912/whats-the-difference-between-include-require-and-open-in-ocaml)

答案 1:

- `include` re-exports the components of the module in the current structure: the module you are in will contain all definitions that are in Ppx_core.

- `open` makes the components of the module directly accessible in the typing environment. Instead of typing `Core.Std.element` you can just type `element`.

- `#require` is a Topfind command that finds a library and loads it, making its modules accessible to you.

- `#use` behave as if copying a full file directly into your toplevel.

Note that the #-keywords are not part of the OCaml language but are toplevel commands: they won't work if you try to compile your file.

答案 2:

The `include Module.Name` statement in the module definition will include all definitions from a module named `Module.Name`. The definitions will be included roughly as they were copy-pasted. If the `include Module.Name` occurs inside of the module type definition (aka signature definition), the `Module.Name` should be a valid (known to a compiler) module type. It will include the definition of a module type as it is (without including any type sharing constraints).

The `open Module.Name` statement occurring in both module implementation and module signature, will allow you to refer to definitions (values, types, submodules) of a Module.Name without using a fully qualified named, i.e., using short names without the Module.Name prefix.

The `#require` statement is not a statement at all and is **not a part of OCaml grammar**. It is special directive of the OCaml toplevel - the interactive loop. The same as ipython has its own directives. The require directive will load the specified package, and all its dependencies. Moreover, this directive is not a part of a standard OCaml toplevel distribution, but is added by the topfind script that is a part of the ocamlfind toolkit.

The `#use` directive is used to load and evaluate a script. For example `#use "topfind"` will load and evaluate the topfind script from the OCaml standard library folder. This script will register the require directive. There are also `#load` and `#load_rec` directives, that work on a more fine-granular level, rather than packages -- these directives are intendend to load libraries.

## OCaml 的多态函数

下面的函数就是 OCaml 中的一个多态函数。

```ocaml
let first_if_true test x y =
  if test x then x else y;;
```

它的类型推断为

```ocaml
val first_if_true : ('a -> bool) -> 'a -> 'a -> 'a = <fun>
```

类型推断的步骤如下：

1. 因为 if 语句只接受一个 bool 值，所以 OCaml 推断 test 函数的类型为 `a -> bool`。
2. 因为 if then else 语句的 then 与 else 只接受一样类型的参数，所以 OCaml 推断 x 与 y 的类型相同。
3. 因为 first_if_true 函数的返回值必定为 x 或 y，所以推断函数的返回值类型与 x, y 相同。
4. 因为 OCaml 无法得知 x, y 的类型，所以推断其类型为通用类型，使用 'a 来进行替代。

综上，推断出 first_if_true 函数的类型为 `('a -> bool) -> 'a -> 'a -> 'a`。因为函数接受未知的类型，所以，可以把这个函数称为多态函数。可以使用不同类型的参数来测试一下这个函数。

```ocaml
let test_str s = String.length s > 3;;
first_if_true test_str "aaa" "bbbb";;
- : string = "bbbb"

let test_int x = x > 3;;
first_if_true test_int 3 5;;
- : int = 5
```

## Tuple

OCaml 中的 tuple 数据结构可以在一个 tuple 中存储不同类型的元素。下面是创建 tuple 与访问 tuple 的语法。

```ocaml
let tup = (3, "three");;
val tup : int * string = (3, "three")

let (x,y) = tup;;
val x : int = 3
val y : string = "three"
```

其中 `let (x,y) = tup` 是模式匹配语法，分别将 tup 的第一个元素和第二个元素绑定到 x 和 y 上。

## List

OCaml 中的 list 数据结构可以存放类型相同，数量可变的元素。需要注意一样，List 中的元素使用 `;` 符号进行分隔，而不是其他语言中常用的 `,`。

```ocaml
let nums = [1;2;3];;
val nums : int list = [1; 2; 3]

List.length nums;;
- : int = 3
```

Base 库提供了一个 List 模块，包含大量与 List 数据结构相关的函数，上面示例中的 `List.length` 函数就就是求 List 长度的一个函数。

可以使用 `new_element :: List` 语法来给 List 的头部插入元素，这个语法返回一个新的 List 并且不会修改原来的 List。

```ocaml
let strs = ["a";"aa";"aaa"];;
"b" :: strs;;
- : string list = ["b"; "a"; "aa"; "aaa"]

strs;;
- : string list = ["a"; "aa"; "aaa"]
```




## Refs

Refs 是 Ocaml 中的一种可变数据结构，实质上就是带有单个 mutable 元素 `contents` 的 Record 类型。

```ocaml
let x = {contents = 0};;
(* val x : int ref = {contents = 0} *)
x.contents <- x.contents + 1;;
x.contents;;
- : int = 1
```

这个 mutable 元素的类型不一定是 int，还可以是其他类型，如 string。

```ocaml
let x = {contents = "hello"};;
val x : string ref = {contents = "hello"}
x.contents;;
- : string = "hello"
```

其中 `val x : string ref = {contents = "hello"}` 这一行并不是我们的输入，而是 utop 的输出，在定义完 `let x = {contents = "hello"};;` 这一行之后，utop 自动进行类型推导并将推导结果输出到终端。

要访问 Refs 的内容除了使用 `.contents` 外还可以使用 `!` 符号。

```ocaml
let x = ref 0;;
val x : int ref = {contents = 0}
x := !x + 1;;
!x;;
- : int = 1
x.contents;;
- : int = 1
```
可以看到，使用 `x := !x + 1` 语句成功地让 `x.contents` 自增了 1，`!x` 是 `x.contents` 的语法糖，`:=` 在对 Refs 类型的赋值中等于 `<-`。

## For 循环和 While 循环

```ocaml
utop # let print_array array =
           let length = Array.length array in
           for i = 0 to length-1 do
               Format.print_string array.(i);
               Format.print_string "\n";
           done;;
utop # print_array [|"a"; "b"; "c"|];;
a
b
c
```

```ocaml
utop # let find_first_negative array =
           let pos = ref 0 in
               while !pos < Array.length array && array.(!pos) >= 0 do
                   pos := !pos + 1
               done;
           if !pos = Array.length array then None else Some !pos;;

utop # find_first_negative [|1;2;-1;3|];;
- : int option = Some 2
```

这两种循环看代码都很好理解，基本和命令式语言中差不多。


## 使用 dune 为 OCaml 代码生成可执行文件

dune 是 OCaml 的项目管理工具，假设我们在目录 example 下。想用 dune 为模块 `test.ml` 生成一个可执行文件，那么需要按照如下步骤。

### 1 创建一个 `dune-project` 文件

```ocaml
(lang dune 2.9)
(name example)
```

这两行分别表示使用的 dune 版本和项目名字。

### 2 创建一个 `dune` 文件

```ocaml
(executable
  (name test)
  (libraries base stdio))
```

第一行 `executable` 表示要还生成一个可执行文件，第二行表示源文件名，第三行是源文件中用到的模块。

### 3 执行

在终端中执行如下命令，构建一个可执行文件。

```bash
dune build test.exe
```

需要注意的是可执行文件 `*.exe` 的前缀 `*` 需要和 `dune` 文件中定义的 `(name *)` 一致，在这个例子中都是 `test`。

## OCaml 中的变量

定义变量的时候，首字母需要为小写字母或者下划线。

OCaml 一个比较有意思的点是虽然它是强类型语言，但是变量并非与类型绑定，变量可以以其他类型重定义，如果你定义了一个 string 类型的变量 x, 可以立刻在下一行重新定义一个 int 类型的变量 x。

```ocaml
let a = "hello";;
val a : string = "hello"
let a = 10;;
val a : int = 10
 a;;
- : int = 10
```

如果在多层的 let 绑定中出现了重复定义，那么内层的表达式中使用的变量是距离它最近的外层中的 let 绑定的定义。

```ocaml
let area_of_ring inner_radius outer_radius =
           let pi = Float.pi in
           let area_of_circle r = pi *. r *. r in
           let pi = 0. in
           area_of_circle outer_radius -. area_of_circle inner_radius;;
Line 4, characters 15-17:
Warning 26 [unused-var]: unused variable pi.
val area_of_ring : float -> float -> float = <fun>
```

这个例子中 `let area_of_circle r = pi *. r *. r` 中使用的 `pi` 的定义就是最外层的 `let pi = Float.pi` 而不是内层的 `let pi = 0.`。




