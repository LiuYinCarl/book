# book
latex books

## 编译说明

使用 XeLaTex 引擎进行编译。

## 开源库使用

ElegantBook v4.4


## 插入书籍中图片 draw.io导出图像标准

png 400ppi 边框宽度为 5 非透明


## Listings package 中使用希腊字母设置

```latex
\lstset{
    % basicstyle = \ttfamily,           % 基本样式 + 小号字体
    % breaklines = true,                  % 代码过长则换行
    % frame = shadowbox,                  % 用（带影子效果）方框框住代码块
    % showspaces = false,                 % 不显示空格
    % columns = fixed,                    % 字间距固定
    % numbers=left,                       % 左侧展示行号
    % numberstyle=\it,                    % 斜体行号
    escapeinside={@(}{)@},  % 设置 escape 字符，放置在 @( )@ 中间的内容会被当作 LaTex 进行解释,例如 @($\alpha$)@
}
```