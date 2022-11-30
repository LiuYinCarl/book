# Real World OCaml 2nd note

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

## 如何在 utop 中加载一个源代码模块

[Loading a module with dependencies in utop](https://stackoverflow.com/questions/46916099/loading-a-module-with-dependencies-in-utop)

假设有两个模块 m1 和 m2, 并且 m2 依赖 m1。那么：

如果要在 utop 中加载模块 m1, 那么使用如下的命令

```ocaml
#use "m1.ml";;
```

如果要在 utop 中加载模块 m2, 那么需要先编译 m1, 然后再在 utop 中加载 m1 和 m2

```bash
ocamlc -c m1.ml # 编译出 m1.cmo
```

```ocaml
#load "m1.cmo";;
#use "m2.ml";;
```

如果 m1 中使用了 base 或者 core 包之类的包的话，编译的时候需要写参数进行说明，不然会编译失败，如果使用了多个包，需要使用多个 `-package` 参数，例如 `-package base -package core`。

```bash
ocamlfind ocamlc -package core -c m1.ml
```

```ocaml
#load "m1.cmo";;
#use "m2.ml";;
```


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


## 匿名函数

OCaml 中的匿名函数定义方法如下。

```ocaml
(fun x -> x + 1)
```

等价于

```ocaml
let add_one x = x + 1
```

## Curried 函数

OCaml 中的一个多参函数如下

```ocaml
let abs_diff x y = abs (x - y);;
```

它的类型是

```ocaml
val abs_diff : int -> int -> int = <fun>
```

这个函数等价于

```ocaml
let abs_diff =
(fun x -> (fun y -> abs (x - y)));;
val abs_diff : int -> int -> int = <fun>
```

下面这种形式的函数称为 Curried 函数，理解 Curried 函数的关键在于类型签名，需要知道 OCaml 中函数的类型签名是右结合的。

```ocaml
int -> int -> int
```

等价于

```ocaml
int -> (int -> int)
```

Curried 函数的作用在于可以构造 partial application (部分应用的函数)，例如下面的 `dist_from_3`。

```ocaml
let dist_from_3 = abs_diff 3
val dist_from_3 : int -> int = <fun>
dist_from_3 8;;
- : int = 5
```

部分应用的函数就是通过给一个多参函数提供部分函数而构造出一个新函数。

## 递归函数

一个在定义中引用了自身的函数被称为递归函数。例如

```ocaml
let rec find_first_repeat list =
           match list with
           | [] | [_] -> None
           | x :: y :: tl ->
               if x = y then Some x else find_first_repeat (y::tl);;
val find_first_repeat : 'a list -> 'a option = <fun>

find_first_repeat [1;2;3;3];;
- : int option = Some 3
```

使用 `and` 关键字定义相互递归的函数，OCaml 定义这个语法是出于技术原因，当前的类型推断算法需要程序员标明哪些函数是相互递归调用的。

```ocaml
let rec is_even x =
           if x = 0 then true else is_odd (x - 1)
and is_odd x =
    if x = 0 then false else is_even (x -1);;
val is_even : int -> bool = <fun>
val is_odd : int -> bool = <fun>

List.map ~f:is_even [0;1;2;3;4;5];;
- : bool list = [true; false; true; false; true; false]
```

## 管道操作符

OCaml 标准库中的管道操作符定义如下

```ocaml
let (|>) x f = f x;;
val ( |> ) : 'a -> ('a -> 'b) -> 'b = <fun>
```

它的作用和 Shell 中的管道操作符 `|` 类似。

```ocaml
let str = "a;b;c";;
val str : string = "a;b;c"

String.split ~on:';' str
|> List.iter ~f:print_endline;;
a
b
c
- : unit = ()
```

需要注意的是，`|>` 操作符的左结合(先计算操作符左边的表达式)性质才使得它能够实现管道效果，如果它是右结合性质的话，那管道功能是无法实现的。

`|>` 被称为 reverse application operator(反向应用操作符)，与之相对的，还有一个被称为 application operator(应用操作符) 的 `@@`，`@@` 的作用是简化多层括号表达式的写法，`f (g (h x))` 可以写为 `f @@ g @@ h x`，从代码中可以看出，`@@` 自然是右结合(先计算操作符右边的表达式)性质。


## 使用 function 关键字定义函数

定义一个函数，除了匿名函数写法 `(fun x -> x + 1)`，简写法 (let add_1 x = x + 1) 之外，还可以使用 `function` 关键字。

```ocaml
let some_or_zero = function
    | Some x -> x
    | None -> 0;;
val some_or_zero : int option -> int = <fun>

List.map ~f:some_or_zero [Some 3; None; Some 4];;
- : int list = [3; 0; 4]
```

等价于

```ocaml
let some_or_zero num_opt =
  match num_opt with
  | Some x -> x
  | None -> 0;;
val some_or_zero : int option -> int = <fun>
```

使用 `function` 也能定义一个参数以上的函数

```ocaml
let some_or_default default = function
  | Some x -> x
  | None -> default;;
val some_or_default : 'a -> 'a option -> 'a = <fun>

List.map ~f:(some_or_default 100) [Some 3; None; Some 4];;
- : int list = [3; 100; 4]
```

## 标签参数

OCaml 中除了位置参数以外，还有标签参数。在调用函数的时候，标签参数不需要按照函数定义中的顺序书写，只需要在调用时使用 `~` 前缀来表明其是一个标签参数。

```ocaml
let ratio ~num ~denom = Float.of_int num /. Float.of_int denom;;
val ratio : num:int -> denom:int -> float = <fun>

ratio ~denom:10 ~num:3;;
- : float = 0.3
```

如果调用时使用的形参名字和函数定义时的形参名字一致，那么调用时可以省略 `:` 及之后的实参。

```ocaml
let num = 3 in
let denom = 4 in
ratio ~num ~denom;;
- : float = 0.75
```

## 可选参数

OCaml 中的可选参数和标签参数类似，不需要按照顺序传递，只需要在使用时使用 `~` 前缀来表明是一个可选参数。可选参数都是 `Some` 类型，当没有传递可选参数的时候，可选参数的值默认为 None。

```ocaml
let concat ?sep x y =
  let sep = match sep with
            | None -> "" 
            | Some s -> s in
    x ^ sep ^ y;;
val concat : ?sep:string -> string -> string -> string = <fun>
concat "foo" "bar";;
- : string = "foobar"
concat ~sep:":" "foo" "bar";;
- : string = "foo:bar"
```

为可选参数提供默认值的写法如下

```ocaml
let concat ?(sep="") x y = x ^ sep ^ y;;
val concat : ?sep:string -> string -> string -> string = <fun>
```

函数调用者传递默认参数的时候对于自己传递的是一个 `Some` 类型的参数是不明确的(因为使用的是和标签参数一样的前缀 `~`)。如果想要强调传递的是 `Some` 类型的参数，可以用下面这种 `?` 前缀的写法。

```ocaml
concat ~sep:":" "foo" "bar" (* provide the optional argument *);;
- : string = "foo:bar"
concat ?sep:(Some ":") "foo" "bar" (* pass an explicit [Some] *);;
- : string = "foo:bar"
```

## 标签参数推断和可选参数

标记参数和可选参数的一个微妙方面是它们是如何由类型系统推断出来的。考虑下面的例子，用于计算两个实变量函数的数值导数。这个函数有一个自变量 delta，它决定了计算导数的大小; x 和 y 值，它决定了计算导数的时间点; f 函数，它的导数正在计算中。函数 f 本身有两个带标签的参数 x 和 y。注意你可以使用撇号作为变量名的一部分，所以 x’和 y’只是普通变量。

```ocaml
let numeric_deriv ~delta ~x ~y ~f =
    let x' = x +. delta in
    let y' = y +. delta in
    let base = f ~x ~y in
    let dx = (f ~x:x' ~y -. base) /. delta in
    let dy = (f ~x ~y:y' -. base) /. delta in
    (dx, dy);;
val numeric_deriv :
  delta:float -> x:float -> y:float -> f:(x:float -> y:float -> float) -> float * float = <fun>
```

原则上，如何选择 f 的参数顺序并不明显。因为标签参数可以按任意顺序传递，所以类型签名可以是 `y: float-> x: float-> float` 或者 `x: float-> y: float-> float`。

更糟糕的是，如果 f 使用可选参数而不是标签参数，那么 f 将是完全一致的，这可能导致 numeric _ deriv 的类型签名如下所示。

```ocaml
val numeric_deriv :
  delta:float ->
  x:float -> y:float -> f:(?x:float -> y:float -> float) -> float * float
```

由于有多种合理的类型可供选择，OCaml 需要一些启发式方法来在它们之间进行选择。编译器使用的启发式方法是优先认为是标签参数而不是可选参数，并以源代码中出现的参数顺序为准。


```ocaml
let numeric_deriv ~delta ~x ~y ~f =
    let x' = x +. delta in
    let y' = y +. delta in
    let base = f ~x ~y in
    let dx = (f ~y ~x:x' -. base) /. delta in
    let dy = (f ~x ~y:y' -. base) /. delta in
    (dx, dy);;
Error: This function is applied to arguments
       in an order different from other calls.
       This is only allowed when the real type is known.
```

出现这个编译错误的原因就是我们在调用 f 函数的时候没有按同一个顺序写标签参数，导致编译器无法做出类型推断。根据错误消息的建议，如果我们提供显式的类型信息，我们可以让 OCaml 接受 f 与不同的参数顺序一起使用。因此，由于 f 上的类型注释，下面的代码编译没有错误。

```ocaml
let numeric_deriv ~delta ~x ~y ~(f: x:float -> y:float -> float) =
  let x' = x +. delta in
  let y' = y +. delta in
  let base = f ~x ~y in
  let dx = (f ~y ~x:x' -. base) /. delta in
  let dy = (f ~x ~y:y' -. base) /. delta in
  (dx,dy);;
val numeric_deriv :
  delta:float -> x:float -> y:float -> f:(x:float -> y:float -> float) -> float * float = <fun>
```

## 可选参数和部分应用函数

在存在部分应用程序的情况下，可选参数可能很难考虑。当然，我们可以部分地应用可选参数本身。

```ocaml
let colon_concat = concat ~sep:":";;
val colon_concat : string -> string -> string = <fun>
colon_concat "a" "b";;
- : string = "a:b"
```

但是如果我们只部分地应用第一个参数会发生什么呢？

```ocaml
let prepend_pound = concat "# ";;
val prepend_pound : string -> string = <fun>
prepend_pound "a BASH comment";;
- : string = "# a BASH comment"
```

可选参数 `?Sep` 现在已经消失或者被删除了。事实上，如果我们现在尝试传递那个可选参数将导致一个编译错误。

```ocaml
prepend_pound "a BASH comment" ~sep:":";;
Line 1, characters 1-14:
Error: This function has type Base.String.t -> Base.String.t
       It is applied to too many arguments; maybe you forgot a `;'.
```

那么 OCaml 什么时候决定丢弃一个可选参数呢？

规则是: 在这个可选参数之后定义的第一个位置参数(即既不带标记也不带可选参数)被传入的时候，这个可选参数会被丢弃。这就解释了 `prepend_ound` 函数的行为。但是如果我们在第二个参数位置才定义了 concat 的可选参数会如何呢:

```ocaml
let concat x ?(sep="") y = x ^ sep ^ y;;
val concat : string -> ?sep:string -> string -> string = <fun>
```

现在部分应用第一个参数不会导致可选参数被丢弃。

```ocaml
let prepend_pound = concat "# ";;
val prepend_pound : ?sep:string -> string -> string = <fun>
prepend_pound "a BASH comment";;
- : string = "# a BASH comment"
prepend_pound "a BASH comment" ~sep:"--- ";;
- : string = "# --- a BASH comment"
```

然而，如果一个函数在调用时提供了所有参数，那么直到所有参数都传入之后，才会考虑删除可选参数。这保留了我们在参数列表的任何位置传递可选参数的能力。因此，我们可以写。

```ocaml
concat "a" "b" ~sep:"=";;
- : string = "a=b"
```

如果在定义函数的时候，可选参数之后没有定义任何一个位置参数，那么编译器有一个警告。

```ocaml
let concat x y ?(sep="") = x ^ sep ^ y;;
Line 1, characters 18-24:
Warning 16 [unerasable-optional-argument]: this optional argument cannot be erased.
val concat : string -> string -> ?sep:string -> string = <fun>
```

在这种情况下，当我们提供两个位置参数时，`sep` 参数不会删除，函数表达式不会进行计算，而是返回一个希望提供 `sep` 参数的部分应用函数。

```ocaml
concat "a" "b";;
- : ?sep:string -> string = <fun>
```

**所以，在定义含有可选参数的函数时，最好不要将可选参数放在最后。**

## 使用 dune 管理项目(TODO: 补充内容)

使用 dune 管理项目需要两个配置文件，`dune` 和 `dune-project`，`dune-project` 文件包含项目的基本配置，最简单的 `dune-project` 文件只包含项目要求的 `dune` 软件的版本。

```dune
(lang dune 3.0)
```

`dune` 文件则包含编译信息，包括要编译的文件及文件使用的库。一个单文件并且使用了 base, stdio 库的项目的 `dune` 配置如下。

```dune
(executable
  (name test)
  (libraries base stdio)
)
```

## 模块 Module

OCaml 中每个文件称为一个 Module。

基本的模块定义语法如下

```ocaml
module <name> : <signature> = <implementation>
```

使用 open 打开模块的时候一般不建议全局打开，而是通过 local open, 只在使用到的地方打开，例如

```ocaml
open Base;;
let average x y =
    Int64.((x + y) / of_int 2);;
val average : int64 -> int64 -> int64 = <fun>
```

或者

```ocaml
open Base;;
let average x y =
    let open Int64 in
    (x + y) / of_int 2;;
val average : int64 -> int64 -> int64 = <fun>
```

还可以使用模块别名来减少模块输入的字符数

```ocaml
open Base;;

let average x y =
    let module I = Int64 in
    I.((x + y) / of_int 2);;
val average : int64 -> int64 -> int64 = <fun>
```

## Include Modules

open Module 是将模块的内容添加到标识符搜索空间，而 include Module 则是向 Module 中添加新的标识符。

```ocaml
module Interval = struct
    type t = | Interval of int * int
             | Empty

    let create low high =
        if high < low then Empty else Interval (low,high)
end;;
module Interval :
  sig type t = Interval of int * int | Empty val create : int -> int -> t end


module Extended_interval = struct
    include Interval
    let contains t x =
        match t with
        | Empty -> false
        | Interval (low, high) -> x >= low && x <= high
end;;
module Extended_interval :
  sig
    type t = Interval.t = Interval of int * int | Empty
    val create : int -> int -> t
    val contains : t -> int -> bool
  end
```

如果使用了 include 的话，那么在编写模块类型文件 `.mli` 的时候，也需要进行处理。

```ocaml
(* extend_option.ml *)

open Base

include Option

let apply f_opt x =
  match f_opt with
  | None -> None
  | Some f -> Some (f x)
```

```ocaml
(* extend_option.mli *)

open Base

include module type of Option

val apply : ('a -> 'b) t -> 'a -> 'b t
```

另外，如果想要重新定义原模块中的同名函数函数的话，可以先 include 原模块，然后再写一个同名函数对原模块中的函数进行覆盖。

如果像要将对原函数的模块拓展都集中到一处进行处理的话，以上面我们拓展的 Option 模块为例，可以定义一个新的例如名字为 `import.ml` 的文件，然后在这个文件中写入如下内容。

```ocaml
(* 导入模块的时候，模块名首字母需要大写 *)
module Option = Extend_option
```

在使用 Extend_option 模块的时候，调用方法如下。

```ocaml
open Import

(* other code *)
```

## 使用模块时候的常见错误

**Type Mismatches**

常见原因是 `.mli` 文件中的函数签名 `.ml` 文件中的函数定义不匹配。

**Missing Definitions**

常见原因是只在 `.mli` 文件中写了签名，没有在 `.ml` 文件中写定义。

**Type Definition Mismatches**

常见原因是 `.mli` 文件中的类型签名顺序和 `.ml` 文件中的类型定义中字段顺序不匹配。

```ocaml
(* .ml 文件*)

type median =
  | Median of string
  | Before_and_after of string * string

(* .mli 文件 *)
type median =
  | Before_and_after of string * string
  | Median of string
```

**Cyclic Dependencies**

循环依赖，和其他语言类似，OCaml 特殊情况下允许模块级的循环依赖，但不是一个好的方案。

## Record

Record 是 OCaml 中可以包含不同类型的成员的数据结构，与 C 语言中的 Struct 类似。Record 的定义语法如下，每个 field 的首字母需要小写。

```ocaml
type <record-name> =
    { <field> : <type>;
      <field> : <type>;
      ...
    }
```

通过一个例子来看 Record 的用法。

```ocaml
open Core;;

type service_info =
  { service_name : string;
    port         : int;
    protocol     : string;
  };;
type service_info = { service_name : string; port : int; protocol : string; }

#require "re";;
let service_info_of_string line =
  let matches =
    let pat = "([a-zA-Z]+)[ \t]+([0-9]+)/([a-zA-Z]+)" in
    Re.exec (Re.Posix.compile_pat pat) line
  in
  { service_name = Re.Group.get matches 1;
    port = Int.of_string (Re.Group.get matches 2);
    protocol = Re.Group.get matches 3;
  }
;;
val service_info_of_string : string -> service_info = <fun>

let ssh = service_info_of_string "ssh 22/udp";;
val ssh : service_info = {service_name = "ssh"; port = 22; protocol = "udp"}

ssh.port;;
- : int = 22
```

其中 `service_info_of_string` 函数根据 返回值中的成员自动推断返回类型为 `service_info`。如果需要访问 Record 对象的成员，使用 `record.field` 语法即可。

定义一个多态 Record 类型。

```ocaml
type 'a with_line_num = { item: 'a; line_num: int }
```

在实际代码中使用多态 Record

```ocaml
let parse_lines parse file_contents =
    let lines = String.split ~on:'\n' file_contents in
    List.mapi lines ~f:(fun line_num line ->
        { item = parse line;
          line_num = line_num + 1;
        });;
val parse_lines : (string -> 'a) -> string -> 'a with_line_num list = <fun>

parse_lines service_info_of_string
  "rtmp              1/ddp     # Routing Table Maintenance Protocol
   tcpmux            1/udp     # TCP Port Service Multiplexer
   tcpmux            1/tcp     # TCP Port Service Multiplexer";;
- : service_info with_line_num list =
[{item = {service_name = "rtmp"; port = 1; protocol = "ddp"}; line_num = 1};
 {item = {service_name = "tcpmux"; port = 1; protocol = "udp"}; line_num = 2};
 {item = {service_name = "tcpmux"; port = 1; protocol = "tcp"}; line_num = 3}]

parse_lines Int.of_string "1\n10\n100\n1000";;
- : int with_line_num list =
[{item = 1; line_num = 1}; {item = 10; line_num = 2};
 {item = 100; line_num = 3}; {item = 1000; line_num = 4}]
```

在上面的例子中，根据 `parse_lines` 函数给出的不同参数，`parse_lines` 函数返回的类型也不同，这说明 `parse_lines` 也是一个多态函数。

前面提到了，返回值构建的 Record 的字段如果和已有的 Record 定义相符，那么 OCaml 会自动将返回值推断为这个已定义的 Record 类型。那么这会带来一个问题，如果多个 Record 定义中存在相同的 field，那么类型推断还会生效吗？

```ocaml
type ta = {
  f1 : string;
  f2 : string;
};;
type ta = { f1 : string; f2 : string; }

type tb = {
  f1: string;
  f3: string;
};;
type tb = { f1 : string; f3 : string; }
```

如果定义一个获取记录的 f1 field 的函数如下

```ocaml
let get_f1 t = t.f1;;
val get_f1 : tb -> string = <fun>
```

ocaml 默认使用最近的一个符合要求的 Record 类型作为函数参数 t 的类型，那么如果要获取 Rrcord ta 的 f1 字段要怎么写呢？

```ocaml
let get_f1 (t:ta) = t.f1;;
val get_f1 : ta -> string = <fun>
```

如上所示，需要使用类型注释的方式，注明参数 t 的类型为 ta。

另外一种方式是将 ta 和 tb 放置到不同的 module 中，使用的时候通过 module 来推断使用的 Record 类型。

```ocaml
module Ta = struct
  type t = {
    f1: string;
    f2: string;
  }
end;;
module Ta : sig type t = { f1 : string; f2 : string; } end

module Tb = struct
  type t = {
    f1: string;
    f3: string;
  }
end;;
module Tb : sig type t = { f1 : string; f3 : string; } end

let create ~a ~b =
  { Ta.f1 = a; f2 = b };;
val create : a:string -> b:string -> Ta.t = <fun>
```

使用模块中的类型时，只要在一个 field 上注明 module name 就可以，其他的 field 可以省略 module name，例如这里的 Ta.f1 和 f2。

或者使用类型注释

```ocaml
let create ~a ~b : Tb.t =
  { f1 = a; f3 = b };;
val create : a:string -> b:string -> Tb.t = <fun>
```

除了在构造的时候可以这样子写，在模式匹配的时候也可以使用。

```ocaml
let test_f1 {Ta.f1; _} =
  String.uppercase f1;;
val test_f1 : Ta.t -> string = <fun>

let test_f1 t = t.Tb.f1;;
val test_f1 : Tb.t -> string = <fun>
```

其中 `t.Tb.f1` 可能看起来比较奇怪，在 OCaml 中，`.` 有两种使用用法，第一种用法是访问模块的内容，第二种用法是访问 Record field，又由于 Record 类型都是大写的，例如这里的 `Tb`，所以 `t.Tb` 一定是访问模块的内容，所以这两种用法在这里不会产生歧义。

对于使用模块包含类型的方式，可以使用类型注释来简化代码

```ocaml
let test_f1 ({ f1; _} : Ta.t) = String.uppercase f1;;
val test_f1 : Ta.t -> string = <fun>

let test_f1 ({ f1; _} : Tb.t) = String.uppercase f1;;
val test_f1 : Tb.t -> string = <fun>
```

类型注释在这里效果不是很明显，但是如果 Record 中含有很多的 field 的话，那么简化代码带来的收益还是比较可观的。

### functional update 语法

这个语法主要用来对一个 Record 进行部分更新，产生一个新的 Record 对象，并且不修改旧的 Record 对象。在原来的做法中，如果要实现这个功能，需要复制旧 Record 对象的大部分 field 并且只修改我们想修改的 field，做法如下。

```ocaml
type ta =
{ f1: string;
  f2: string
};;
type ta = { f1 : string; f2 : string; }

let update_ta t b =
  { f1 = t.f1;
    f2 = b;
};;
val update_ta : ta -> string -> ta = <fun>

let old = {f1 = "hello"; f2 = "hi"};;
val old : ta = {f1 = "hello"; f2 = "hi"}

update_ta old "good";;
- : ta = {f1 = "hello"; f2 = "good"}

old;;
- : ta = {f1 = "hello"; f2 = "hi"}
```

可以看到，为了只修改 f2 我们还需要复制旧 Record 的 f1 字段，使用 functional update 语法可以帮助我们去掉这一步。

```ocaml
let functional_update t b =
  { t with f2 = b };;
val functional_update : ta -> string -> ta = <fun>

let old = {f1 = "hello"; f2 = "hi"};;
val old : ta = {f1 = "hello"; f2 = "hi"}

functional_update old "good";;
- : ta = {f1 = "hello"; f2 = "good"}

old;;
- : ta = {f1 = "hello"; f2 = "hi"}
```

functional update 虽然可以简化代码，但是也有坏处，那就是如果你之后修改了原始的 Record 定义的话，那么 OCaml 编译器不会提示你同步修改使用了 functional update 的 Record 字段，这样子就可能造成 functional update 的功能与预期不符合。例如下面的例子。

```ocaml
type ta =
{ f1: string;
  f2: string;
};;
type ta = { f1 : string; f2 : string; }

let functional_update ta1 ta2 =
 { ta1 with f2 = ta2.f2; };;
val functional_update : ta -> ta -> ta = <fun>
```

`functional_update` 函数的功能是以 ta1 为基础，将 ta2 中除 f1 字段以外的功能复制到一个新的 Record 对象中。假设之后修改了 Record ta 的定义，增加了 field f3。

```ocaml
type ta =
{ f1: string;
  f2: string;
  f3: string;
};;
type ta = { f1 : string; f2 : string; f3 : string; }
```

再重新编译代码的话，`functional_update` 函数不会报错，但是它的功能已经不正确了，因为它创建的新的 Recoed 对象的 f3 字段是复制的 ta1 的而不是 ta2 的。

### Record 中的 mutable fields

默认情况下，Record 是不可变的，但是可以通过 `mutable` 关键字定义可变的 Record field。

```ocaml
type ta =
{ f1: string;
  mutable f2: string;
};;
type ta = { f1 : string; mutable f2 : string; }

let copy_f2 ta1 ta2 =
  ta1.f2 <- ta2.f2;;
val copy_f2 : ta -> ta -> unit = <fun>

let ta1 = {f1 = "hello"; f2 = "hi"};;
val ta1 : ta = {f1 = "hello"; f2 = "hi"}

let ta2 = {f1 = "book"; f2 = "pen"};;
val ta2 : ta = {f1 = "book"; f2 = "pen"}

copy_f2 ta1 ta2;;
- : unit = ()

ta1;;
- : ta = {f1 = "hello"; f2 = "pen"}

ta2;;
- : ta = {f1 = "book"; f2 = "pen"}
```

`<-` 操作符被用来设置 Record 的 mutable field，在上面的例子中，调用函数 `copy_f2` 成功地将 `ta1` 的 `f2` 字段从 `"hi"` 修改为了 `"pen"`。

### First-Class Fields

TODO: 不是很理解

## Variants

定义可变类型的语法如下，其中 `Tag` 的首字母需要大写。

```ocaml
type <variant> =
  | <Tag> [ of <type> [* <type>]... ]
  | <Tag> [ of <type> [* <type>]... ]
  | ...
``

例如定义 8 种基本颜色

```ocaml
type basic_color =
  | Black | Red | Green | Yellow | Blue | Magenta | Cyan | White
```

负载一点的 Variants 用法直接看书中提供的表示终端下 256 色的例子。

```ocaml
open Base
open Stdio

type basic_color =
  | Black | Red | Green | Yellow | Blue | Magenta | Cyan | White

let basic_color_to_int = function
  | Black -> 0 | Red -> 1 | Green -> 2 | Yellow -> 3
  | Blue -> 4 | Magenta -> 5 | Cyan -> 6 | White -> 7

let color_by_number number text =
  Printf.sprintf "\027[38;5;%dm%s\027[0m" number text

type weight = Regular | Bold

type color =
  | Basic of basic_color * weight
  | RGB   of int * int * int
  | Gray  of int

let color_to_int = function
  | Basic (basic_color, weight) ->
    let base = match weight with Bold -> 8 | Regular -> 0 in
    base + basic_color_to_int basic_color
  | RGB (r, g, b) -> 16 + b + g * 6 + r * 36
  | Gray i -> 232 + i

let color_print color s =
  print_string (color_by_number (color_to_int color) s)

(* test *)
color_print (Basic (Red, Bold)) "A bold red"

color_print (Gray 4) "A muted gray"
```

### Record type and Variants

关于 Record type 和 Variants 的关系，书中有一句话形容的特别好

> More generally, you can think of record types as conjunctions. Variants, on the other hand, are disjunctions, letting you represent multiple possibilities.

简单来说，Record type 像合取，Variants 像析取。

### Polymorphic Variants

Polymorphic Variants 使用反引号开头。

```ocaml
let three = `Int 3;;
val three : [> `Int of int ] = `Int 3

let four = `Float 4.;;
val four : [> `Float of float ] = `Float 4.

let is_positive = function
  | `Int x -> x > 0
  | `Float x -> Float.(x > 0.);;
val is_positive : [< `Float of float | `Int of int ] -> bool = <fun>
```

多态类型中需要注意的是类型标记中的 `<` 和 `>`，其中 `<` 表示 “这些标记或者更少”，`>` 表示 “这些标记或更多”。可以把 `<` 和 `>` 标志当作相应标记的上界和下界。如果同样的一组标记既是上界又是下界，就得到了一个明确的多态变体类型，没有 `<` 和 `>` 标志。

```ocaml
let exact = List.filter ~f:is_positive [three; four];;
val exact : [ `Float of float | `Int of int ] list = [`Int 3; `Float 4.]
```

还可以创建有不同上界和下界的多态变体类型，这可能有些奇怪。下面例子中的 `Ok` 和 `Error` 来自 Core 库中的 `Result.t` 类型。

```ocaml
let is_positive = function
  | `Int x -> Ok (x > 0)
  | `Float x -> Ok Float.O.(x > 0.)
  | `Not_a_number -> Error "not a number";;
val is_positive : [< `Float of float | `Int of int | `Not_a_number ] -> (bool, string) result = <fun>

List.filter [three; four] ~f:(fun x ->
match is_positive x with Error _ -> false | Ok b -> b);;
- : [< `Float of float | `Int of int | `Not_a_number > `Float `Int ] list =
[`Int 3; `Float 4.]
```

这个例子中，推断的类型指出，标记不能超过 `` `Float``, `` `Int`` 和 `` `Not_a_number``, 而且至少包含 `` `Float`` 和 `` `Int``。

### 模式匹配的一个简写

```ocaml
type color =
  [ `Basic of basic_color * [ `Bold | `Regular ]
  | `Gray of int
  | `RGB  of int * int * int ]

let extended_color_to_int = function
  | `RGBA (r,g,b,a) -> 256 + a + b * 6 + g * 36 + r * 216
  | `Grey x -> 2000 + x
  | (`Basic _ | `RGB _ | `Gray _) as color -> color_to_int color

let extended_color_to_int : extended_color -> int = function
  | `RGBA (r,g,b,a) -> 256 + a + b * 6 + g * 36 + r * 216
  | #color as color -> color_to_int color
```

这个例子中可以使用 `#color` 代替 ``(`Basic _ | `RGB _ | `Gray _)`` 来简写代码。

## Error Handling

### Bind

`bind` 的实现如下
```ocaml
let bind option ~f =
  match option with
  | None -> None
  | Some x -> f x;;
val bind : 'a option -> f:('a -> 'b option) -> 'b option = <fun>
```

`bind` 的功能就是如果 `option` 为 `None` 的话则什么都不做返回 `None`，如果为 `Some x` 的话，则返回 `f x`。

`bind` 使用的常见用法如下

```ocaml
let compute_bounds ~compare list =
  let sorted = List.sort ~compare list in
  Option.bind (List.hd sorted) ~f:(fun first ->
    Option.bind (List.last sorted) ~f:(fun last ->
      Some (first,last)));;
val compute_bounds : compare:('a -> 'a -> int) -> 'a list -> ('a * 'a) option =
  <fun>
```

`compute_bounds` 函数用来计算一个列表的上下界。

```ocaml
compute_bounds ~compare:(fun x y -> x - y) [4;3;2;1];;
- : (int * int) option = Base.Option.Some (1, 4)
```

`Option.Monad_infix` 模块中实现了 `bind` 中缀写法 `>>=` 用来简化代码。

```ocaml
let compute_bounds ~compare list =
  let open Option.Monad_infix in
  let sorted = List.sort ~compare list in
  List.hd sorted   >>= fun first ->
  List.last sorted >>= fun last  ->
  Some (first,last);;
val compute_bounds : compare:('a -> 'a -> int) -> 'a list -> ('a * 'a) option = <fun>
```

### 捕捉异常

以常见的文本解析代码为例，如果需要不符合规则的文件，如果代码写的不够健壮，就容易因为文件格式不对导致代码异常退出，导致文件句柄泄露，如下所示。

```ocaml
open Stdio;;
open Base;;

let parse_line line =
  String.split_on_chars ~on:[','] line
  |> List.map ~f:Float.of_string;;
val parse_line : string -> float list = <fun>

let load filename =
  let inc = In_channel.create filename in
  let data =
    In_channel.input_lines inc
    |> List.map ~f:parse_line
  in
  In_channel.close inc;
  data;;
val load : string -> float list list = <fun>
```

Base 库中提供了 `Exn.protect` 函数来捕捉异常，使用它来重写 `load` 函数。

```ocaml
let load filename =
  let inc = In_channel.create filename in
  Exn.protect
    ~f:(fun () -> In_channel.input_lines inc |> List.map ~f:parse_line)
    ~finally:(fun () -> In_channel.close inc);;
val load : string -> float list list = <fun>
```

对于遇到异常时关闭文件句柄这种情况 In_channel 模块也提供了 `with_file` 函数来处理。

```ocaml
let load filename =
  In_channel.with_file filename ~f:(fun inc ->
    In_channel.input_lines inc |> List.map ~f:parse_line);;
val load : string -> float list list = <fun>
```

Ocaml 中也可以使用 `try ... with` 语法捕捉特定的异常。

```ocaml
let lookup_weight ~compute_weight alist key =
  try
    let data = find_exn alist key in
    compute_weight data
  with
  Key_not_found _ -> 0.;;
val lookup_weight :
  compute_weight:('a -> float) -> (string * 'a) list -> string -> float =
  <fun>
```

`find_exn` 假设是一个从列表中查找元素的函数，如果找不到的话则会抛出异常 `Key_not_found`。在这里例子中，如果 `try` 语句块中抛出了 `Key_not_found`，则 `with` 语句块中会进行捕捉，并返回 `0.`。

如果不只是想处理特定的异常，而是处理任何异常，可以使用模式匹配来匹配异常。

```ocaml
let lookup_weight ~compute_weight alist key =
  match find_exn alist key with
  | exception _ -> 0.
  | data -> compute_weight data;;
val lookup_weight : compute_weight:('a -> float) -> (string * 'a) list -> string -> float = <fun>
```

### 调用栈

OCaml 中可以使用 `Backtrace.Exn.most_recent` 来获取异常调用栈。由于 OCaml 默认关闭了调用栈，所以需要在编译代码的时候链接调试符号。但是即使链接了调试符号，也可以通过环境变量 `OCAMLRUNPARAM` 来关闭捕获调用栈。

```bash
OCAMLRUNPARAM=b=0 dune exec -- ./test.exe
```

在代码中也可以通过调用 `Backtrace.Exn.set_recording false` 函数来关闭调用栈。

这一章的重点是理解 error-aware 和 Exception 的差异以及这两者的适用场景。总结来说就是，对于不可预见的错误，例如内存不足，使用 Exception，对于可以预见到并且比较平常的错误，使用 error-aware。


## 命令式编程

### ref

ref 的定义如下

```ocaml
type 'a ref = { mutable contents : 'a };;
type 'a ref = { mutable contents : 'a; }
```

标准库为 ref 定义了三个重要的操作

**ref expr**

构造一个包含 expr 表达式的值的 reference cell。

**!refcell**

返回 reference cell 的值。

**refcell := expr**

使用 expr 的值替换 reference cell 的值。

用法如下
```ocaml
let x = ref 1;;
val x : int ref = {contents = 1}

!x;;
- : int = 1

x := !x + 1;;
- : unit = ()

!x;;
- : int = 2
```

### for

For 循环的结构是 `for 下限 to 上限 done` 或者 `for 上限 downto 下限 done` 并且上限和下限都包含在循环中。

```ocaml
open Stdio;;

for i = 0 to 3 do printf "i = %d\n" i done;;
i = 0
i = 1
i = 2
i = 3
- : unit = ()
```

### whiel

```ocaml
let i =ref 0;;
val i : int ref = {Base.Ref.contents = 0}

while !i < 3 do
  printf "i = %d\n" !i;
  i := !i + 1
done;;
i = 0
i = 1
i = 2
- : unit = ()
```
