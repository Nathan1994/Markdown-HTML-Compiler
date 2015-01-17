Markdown-HTML-Compiler
======================
# 1.项目说明

## 项目基本功能

本项目主要实现了 test03.md 的解析，能够正确解析的 markdown 语法最要有：

* 标题 h1 到 h3
* 列表
* 链接
* 图片
* 加粗
* 斜体
* 引用
* 分割线
* 代码


## 扩展功能

同时，我们还实现了一些 markdown 本身不具备的功能：

### 代码着色

主要使用了google-code-prettify库，在解析出代码的时候对代码进行着色处理。

* 使用的库链接：https://code.google.com/p/google-code-prettify/

测试文件和测试方法

```
测试文件位于项目目录TestDocument下
测试：
python run.py
产生文件位于项目目录Markdown-HTML-Compiler下
文件名：output.html
```


# 2.组队信息


## 小组成员贡献说明

### 邵泽满 1252949 （组长）<Nathan1994>
主要工作：列表、链接、图片、引用、代码解析以及代码着色处理
贡献率： 50%

### 时雨 1252961
主要工作：标题、加粗、斜体、引用、分割线、代码解析
贡献率： 50%
