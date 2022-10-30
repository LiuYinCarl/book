# JavaScript 高级程序设计第四版笔记


## script 标签

使用了 `src` 属性的 `<script>` 元素不应该再在 `<script>` 和 `</script>` 标签中再包含其他 JavaScript 代码。如果两者都提供的话，则浏览器只会下载并执行脚本文件，从而忽略行内代码。下面的写法就不会有一个弹窗弹出。

```html
<html>
<head>
    <script src="test.js">alert("hello");</script>
</head>
<body>this is a message.</body>
</html>
```


过去，所有 `<script>` 元素都被放在页面的 `<head>` 标签内，这种做法的主要目的是把外部的 CSS 和 JavaScript 文件都集中放到一起。不过，把所有 JavaScript 文件都放在 `<head>` 里，也就意味着必须把所有 JavaScript代码都下载、解析和解释完成后，才能开始渲染页面（页面在浏览器解析到 `<body>` 的起始标签时开始渲染）。对于需要很多 JavaScript 的页面，这会导致页面渲染的明显延迟，在此期间浏览器窗口完全空白。为解决这个问题，现代 Web 应用程序通常将所有 JavaScript引用放在 `<body>` 元素中的页面内容后面，这样一来，页面会在处理 JavaScript 代码之前完全渲染页面。用户会感觉页面加载更快。

## 推迟执行脚本

HTML 4.01 为 `<script>` 元素定义了一个叫 `defer` 的属性。这个属性表示脚本在执行的时候不会改变页面的结构。也就是说，脚本会被延迟到整个页面都解析完毕后再运行。因此，在 `<script>` 元素上 设置 `defer` 属性，相当于告诉浏览器立即下载，但延迟执行。HTML5 规范要求脚本应该按照它们出现的顺序执行，因此第一个推迟的脚 本会在第二个推迟的脚本之前执行，而且两者都会在 DOMContentLoaded 事件之前执行，不过在实际当中，推迟执行的脚本不一定总会按顺序执行或者在 DOMContentLoaded 事件之前执行，因此最好只包含一个这样的脚本。`defer` 属性只对外部脚本文件才有效。这是 HTML5中明确规定的，因此支持 HTML5 的浏览器会忽略行内脚本的 `defer` 属性。

## 异步执行脚本

HTML5为 `<script>` 元素定义了 `async` 属性。从改变脚本处理方式上看，`async` 属性与 `defer` 类似。当然，它们两者也都只适用于外部脚本，都会告诉浏览器立即开始下载。不过，与 `defer` 不同的是，标记为 `async` 的脚本并不保证能按照它们出现的次序执行。给脚本添加 `async` 属性的目的是告诉浏览器，不必等脚本下载和执行完后再加载页面，同样也不必等到该异步脚本下载和执行后再加载其他脚本。异步脚本保证会在页面的 `load` 事件前执行，但可能会在DOMContentLoaded 之前或之后。

## 严格模式

ECMAScript 5 增加了严格模式（strict mode）的概念。严格模式是一种不同的 JavaScript 解析和执
行模型，ECMAScript 3的一些不规范写法在这种模式下会被处理，对于不安全的活动将抛出错误。要对 整个脚本启用严格模式，在脚本开头加上这一行：

```js
"use strict";
```

也可以单独指定一个函数在严格模式下执行，只要把这个预处理指令放到函数体开头即可。

```js
function doSomething() {
    "use strict"; // 函数体
}
```

## 变量

ECMAScript 变量是松散类型的，意思是变量可以用于保存任何类型的数据。每个变量只不过是一个用于保存任意值的命名占位符。有 3 个关键字可以声明变量：var、const 和 let。其中，var 在 ECMAScript 的所有版本中都可以使用，而 const 和 let 只能在 ECMAScript 6 及更晚的版本中使用。

使用 var 操作符定义的变量会成为包含它的函数的局部变量。比如，使用 var 在一个函数内部定义一个变量，就意味着该变量将在函数退出时被销毁。去掉 var 操作符之后，就变成了全局变量。

```js
function test() {
    message = "hello"; // 全局变量
}
test();
alert(message);
```

## var 声明

使用 var 时，下面的代码不会报错。这是因为使用这个关键字声明的变量会自动提升到函数作用域顶部。这就是所谓的“提升”（hoist），也就是把所有变量声明都拉到函数作用域的顶部。
```js
function test() {
    console.log(name);
    var name = "Bob";
}
test();

// 等价于
function test() {
    var name;
    console.log(name);
    name = "Bob";
}
test();
```

## let 声明

let 跟 var 的作用差不多，但有着非常重要的区别。最明显的区别是，let 声明的范围是块作用域，而 var 声明的范围是函数作用域。let 也不允许同一个块作用域中出现重复声明。

```js
function test() {
    if (true) {
        var name = "Bob";
        console.log(name); // Bob
    }
    console.log(name);  // Bob
}
test();

function test() {
    if (true) {
        let name = "Bob";
        console.log(name); // Bob
    }
    console.log(name);  // ReferenceError
}
```

let 与 var 的另一个重要的区别，就是 let 声明的变量不会在作用域中被提升。在解析代码时，JavaScript引擎也会注意出现在块后面的 let 声明，只不过在此之前不能以任何方式来引用未声明的变量。在 let 声明之前的执行瞬间被称为“暂时性死区”（temporal dead zone），在此 阶段引用任何后面才声明的变量都会抛出 ReferenceError。

## const 声明

const 的行为与 let 基本相同，唯一一个重要的区别是用它声明变量时必须同时初始化变量，且尝试修改 const 声明的变量会导致运行时错误。const 声明的限制只适用于它指向的变量的引用。换句话说，如果 const 变量引用的是一个对象，那么修改这个对象内部的属性并不违反 const 的限制。

```js
const person = {};
person.name = "Bob"; // ok
```

## 数据类型

ECMAScript 有 6种简单数据类型（也称为原始类型）：Undefined、Null、Boolean、Number、String 和 Symbol。Symbol（符号）是 ECMAScript 6 新增的。还有一种复杂数据类型叫 Object（对象）。Object 是一种无序名值对的集合。因为在 ECMAScript 中不能定义自己的数据类型，所有值都可 以用上述 7种数据类型之一来表示。

### typeof 操作符

因为 ECMAScript 的类型系统是松散的，所以需要一种手段来确定任意变量的数据类型。typeof
操作符就是为此而生的。对一个值使用 typeof 操作符会返回下列字符串之一：
- "undefined"表示值未定义；
- "boolean"表示值为布尔值；
- "string"表示值为字符串；
"number"表示值为数值；
- "object"表示值为对象（而不是函数）或 null；
- "function"表示值为函数；
- "symbol"表示值为符号。

注意typeof在某些情况下返回的结果可能会让人费解，但技术上讲还是正确的。比如，调用 typeof null 返回的是"object"。这是因为特殊值 null 被认为是一个对空对象的引用。

严格来讲，函数在 ECMAScript中被认为是对象，并不代表一种数据类型。可是，函数也有自己特殊的属性。为此，就有必要通过 typeof 操作符来区分函数和其他对象。

### Undefined 类型

Undefined 类型只有一个值，就是特殊值 undefined。当使用 var 或 let 声明了变量但没有初始化时，就相当于给变量赋予了 undefined 值。

注意，包含 undefined 值的变量跟未定义变量是有区别的。请看下面的例子：

```js
let name1;
// let name2;
console.log(name1); // undefined
console.log(name2); // ReferenceError
```

对未声明的变量，只能执行一个 有用的操作，就是对它调用 typeof。在对未初始化的变量调用 typeof 时，返回的结果是"undefined"，但对未声明的变量调用它时，返回的结果还是 "undefined"。无论是声明还是未声明，typeof 返回的都是字符串"undefined"。逻辑上讲这是对的，因为虽然严格来讲这两个变量存在根本性差异，但它们都无法执行实际操作。

```js
let name1;
// let name2;
console.log(typeof name1); // undefined
console.log(typeof name2); // undefined
```

### Null 类型

Null 类型同样只有一个值，即特殊值 null。逻辑上讲，null 值表示一个空对象指针，这也是给 typeof 传一个 null 会返回"object"的原因。在定义将来要保存对象值的变量时，建议使用 null 来初始化，不要使用其他值。这样，只要检查这个变量的值是不是 null 就可以知道这个变量是否在后来被重新赋予了一个对象的引用。

undefined 值是由 null 值派生而来的，因此 ECMA-262 将它们定义为表面上相等，如下面的例子所示。

```js
console.log(null == undefined); // true
```

### Boolean 类型

Boolean（布尔值）类型是 ECMAScript中使用最频繁的类型之一，有两个字面值：true 和 false。这两个布尔值不同于数值，因此 true 不等于 1，false 不等于 0。

虽然布尔值只有两个，但所有其他 ECMAScript类型的值都有相应布尔值的等价形式。要将一个其他类型的值转换为布尔值，可以调用特定的 Boolean()转型函数。

```js
let name = "Bob";
console.log(Boolean(name)); // true
```

其他类型转换到 Boolean 的规：

| 数据类型 | 转换为 true 的值 | 转换为 false 的值 |
|---|---|---|
| String    | 非空字符串 | 空字符串   |
| Number    | 非零数值   | 0, NaN    |
| Object    | 任意对象   | null      |
| Undefined | 不存在     | undefined |


### Number 类型

ECMAScript中最有意思的数据类型或许就是 Number 了。Number 类型使用 IEEE 754格式表示整数和浮点值（在某些语言中也叫双精度值）。不同的数值类型相应地也有不同的数值字面量格式。

整数也可以用八进制（以 8为基数）或十六进制（以 16为基数）字面量表示。对于八进制字面量，第一个数字必须是零（0），然后是相应的八进制数字（数值 0~7）。如果字面量中包含的数字超出了应 有的范围，就会忽略前缀的零，后面的数字序列会被当成十进制数。

**八进制字面量在严格模式下是无效的，会导致 JavaScript引擎抛出语法错误。ECMAScript 2015 或 ES6中的八进制值通过前缀 0o 来表示；严格模式下，前缀 0 会被视为语法错误，如果要表示 八进制值，应该使用前缀 0o。**

要创建十六进制字面量，必须让真正的数值前缀 0x（区分大小写），然后是十六进制数字（0~9 以 及 A~F）。十六进制数字中的字母大小写均可。

如果某个计算得到的 数值结果超出了 JavaScript 可以表示的范围，那么这个数值会被自动转换为一个特殊的 Infinity（无 穷）值。任何无法表示的负数以-Infinity（负无穷大）表示，任何无法表示的正数以 Infinity（正 无穷大）表示。 如果计算返回正 Infinity 或负 Infinity，则该值将不能再进一步用于任何计算。这是因为
Infinity 没有可用于计算的数值表示形式。要确定一个值是不是有限大（即介于 JavaScript 能表示的 最小值和最大值之间），可以使用 isFinite()函数。

```js
let res = Number.MAX_VALUE + Number.MAX_VALUE;
console.log(isFinite(res)); // false
```

有一个特殊的数值叫 NaN，意思是“不是数值”（Not a Number），用于表示本来要返回数值的操作失败了（而不是抛出错误）。比如，用 0 除任意数值在其他语言中通常都会导致错误，从而中止代码执行。但在 ECMAScript中，0、+0 或 -0 相除会返回 NaN。NaN 有几个独特的属性。首先，任何涉及 NaN 的操作始终返回 NaN（如 NaN/10），在连续多步计算时这可能是个问题。其次，NaN 不等于包括 NaN 在内的任何值。例如，下面的比较操作会返回 false。

```js
console.log(NaN == NaN); // false
```

为此，ECMAScript提供了 isNaN()函数。该函数接收一个参数，可以是任意数据类型，然后判断这个参数是否“不是数值”。把一个值传给 isNaN()后，该函数会尝试把它转换为数值。某些非数值的 值可以直接转换成数值，如字符串"10"或布尔值。任何不能转换为数值的值都会导致这个函数返回 true。

有 3个函数可以将非数值转换为数值：Number()、parseInt() 和 parseFloat()。Number()是转型函数，可用于任何数据类型。后两个函数主要用于将字符串转换为数值。

Number()函数基于如下规则执行转换。

- 布尔值，true 转换为 1，false 转换为 0。
- 数值，直接返回。
- null，返回 0。
- undefined，返回 NaN。
- 字符串，应用以下规则。
-- 如果字符串包含数值字符，包括数值字符前面带加、减号的情况，则转换为一个十进制数值。因此，Number("1") 返回 1，Number("123") 返回 123，Number("011") 返回 11（忽略前面 的零）。
- - 如果字符串包含有效的浮点值格式如"1.1"，则会转换为相应的浮点值（同样，忽略前面的零）。
- - 如果字符串包含有效的十六进制格式如"0xf"，则会转换为与该十六进制值对应的十进制整 数值。
- - 如果是空字符串（不包含字符），则返回 0。  如果字符串包含除上述情况之外的其他字符，则返回 NaN。
- 对象，调用 valueOf()方法，并按照上述规则转换返回的值。如果转换结果是 NaN，则调用 toString()方法，再按照转换字符串的规则转换。

考虑到用 Number()函数转换字符串时相对复杂且有点反常规，通常在需要得到整数时可以优先使用 parseInt()函数。parseInt()函数更专注于字符串是否包含数值模式。字符串最前面的空格会被 忽略，从第一个非空格字符开始转换。如果第一个字符不是数值字符、加号或减号，parseInt()立即 返回 NaN。这意味着空字符串也会返回 NaN（这一点跟 Number()不一样，它返回 0）。如果第一个字符 是数值字符、加号或减号，则继续依次检测每个字符，直到字符串末尾，或碰到非数值字符。比如， "1234blue"会被转换为 1234，因为"blue"会被完全忽略。类似地，"22.5"会被转换为 22，因为小数 点不是有效的整数字符。

假设字符串中的第一个字符是数值字符，parseInt()函数也能识别不同的整数格式（十进制、八进制、十六进制）。换句话说，如果字符串以"0x"开头，就会被解释为十六进制整数。如果字符串以"0" 开头，且紧跟着数值字符，在非严格模式下会被某些实现解释为八进制整数。不同的数值格式很容易混淆，因此 parseInt() 也接收第二个参数，用于指定底数（进制数）。

parseFloat()函数的工作方式跟 parseInt()函数类似，都是从位置 0开始检测每个字符。同样，它也是解析到字符串末尾或者解析到一个无效的浮点数值字符为止。这意味着第一次出现的小数点是有 效的，但第二次出现的小数点就无效了，此时字符串的剩余字符都会被忽略。parseFloat()函数的另一个不同之处在于，它始终忽略字符串开头的零。这个函数能识别前面讨论的所有浮点格式，以及十进制格式（开头的零始终被忽略）。十六进制数值始终会返回 0。因为 parseFloat()只解析十进制值，因此不能指定底数。最后，如果字符串表示整数（没有小数点或者小 数点后面只有一个零），则 parseFloat()返回整数。

### String 类型

String（字符串）数据类型表示零或多个 16 位 Unicode 字符序列。字符串可以使用双引号（"）、单引号（'）或反引号（`）标示。

字符串的长度可以通过其 length 属性获取，这个属性返回字符串中 16位字符的个数。

```js
console.log("hi,世界".length); // 5
```

ECMAScript中的字符串是不可变的（immutable），意思是一旦创建，它们的值就不能变了。要修改某个变量中的字符串值，必须先销毁原始的字符串，然后将包含新值的另一个字符串保存到该变量。

toString()方法可见于数值、布尔值、对象和字符串值。（没错，字符串值也有 toString()方法，该方法只是简单地返回自身的一个副本。）null 和 undefined 值没有 toString()方法。

ECMAScript 6 新增了使用模板字面量定义字符串的能力。与使用单引号或双引号不同，模板字面量保留换行字符，可以跨行定义字符串，使用反引号表示。

模板字面量最常用的一个特性是支持字符串插值，也就是可以在一个连续定义中插入一个或多个值。技术上讲，模板字面量不是字符串，而是一种特殊的 JavaScript 句法表达式，只不过求值后得到的 是字符串。模板字面量在定义时立即求值并转换为字符串实例，任何插入的变量也会从它们最接近的作 用域中取值。字符串插值通过在 `${}` 中使用一个 JavaScript表达式实现：

```js
let n = 10;
let s = `n = ${n}`
console.log(s); // n = 10
```

使用模板字面量也可以直接获取原始的模板字面量内容（如换行符或 Unicode 字符），而不是被转换后的字符表示。为此，可以使用默认的 String.raw 标签函数。
```js
console.log(`\u00A9`); // ©
console.log(String.raw`\u00A9`); // \u00A9
```

### Symbol 类型

Symbol（符号）是 ECMAScript 6新增的数据类型。符号是原始值，且符号实例是唯一、不可变的。符号的用途是确保对象属性使用唯一标识符，不会发生属性冲突的危险。

符号需要使用 Symbol()函数初始化。因为符号本身是原始类型，所以 typeof 操作符对符号返回symbol。

```js
let sym = Symbol();
console.log(typeof sym); // symbol
```

Symbol()函数不能与 new 关键字一起作为构造函数使用。这样做是为了避免创建符号包装对象。如果你确实想使用符号包装对象，可以借用 Object()函数：

```js
let sym = Symbol();
let wrappedSymbol = Object(sym);
console.log(typeof wrappedSymbol); // object
```

如果运行时的不同部分需要共享和重用符号实例，那么可以用一个字符串作为键，在全局符号注册表中创建并重用符号。 为此，需要使用 Symbol.for()方法。Symbol.for()对每个字符串键都执行幂等操作。第一次使用某个字符串调用时，它会检查全局运行时注册表，发现不存在对应的符号，于是就会生成一个新符号实例并添加到注册表中。后续使用相同 字符串的调用同样会检查注册表，发现存在与该字符串对应的符号，然后就会返回该符号实例。

```js
let sym = Symbol.for('foo'); // 创建新符号
let sym2 = Symbol.for('foo'); // 重用已有符号
console.log(sym === sym2); // true
```

即使采用相同的符号描述，在全局注册表中定义的符号跟使用 Symbol()定义的符号也并不等同。

```js
let sym = Symbol('foo');
let sym2 = Symbol.for('foo');
console.log(sym === sym2); // false
```

还可以使用 Symbol.keyFor()来查询全局注册表，这个方法接收符号，返回该全局符号对应的字
符串键。如果查询的不是全局符号，则返回 undefined。

```js
let sym = Symbol.for('foo');
console.log(Symbol.keyFor(sym)); // foo
```

凡是可以使用字符串或数值作为属性的地方，都可以使用符号。这就包括了对象字面量属性和 Object.defineProperty()/Object.defineProperties()定义的属性。对象字面量只能在计算属 性语法中使用符号作为属性。

```js
let sym = Symbol.for('foo');
let obj = {};
obj[sym] = "a Symbol";
console.log(obj[sym]); // a Symbol
```

### Object 类型

ECMAScript中的对象其实就是一组数据和功能的集合。对象通过 new 操作符后跟对象类型的名称来创建。ECMAScript中的 Object 也是派生其他对象的基类。Object 类型的所有属性和方法在派生 的对象上同样存在。

每个 Object 实例都有如下属性和方法。
- constructor：用于创建当前对象的函数。在前面的例子中，这个属性的值就是 Object() 函数。
- hasOwnProperty(propertyName)：用于判断当前对象实例（不是原型）上是否存在给定的属性。要检查的属性名必须是字符串（如 o.hasOwnProperty("name")）或符号。
- isPrototypeOf(object)：用于判断当前对象是否为另一个对象的原型。（第 8 章将详细介绍原型。）
- propertyIsEnumerable(propertyName)：用于判断给定的属性是否可以使用（本章稍后讨 论的）for-in 语句枚举。与 hasOwnProperty()一样，属性名必须是字符串。
- toLocaleString()：返回对象的字符串表示，该字符串反映对象所在的本地化执行环境。
- toString()：返回对象的字符串表示。
- valueOf()：返回对象对应的字符串、数值或布尔值表示。通常与 toString()的返回值相同。 因为在 ECMAScript中 Object 是所有对象的基类，所以任何对象都有这些属性和方法。
