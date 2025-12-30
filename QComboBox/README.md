# QComboBox

- 目录
  - [下拉数据关联](#1下拉数据关联)
  - [文本居中显示](#2文本居中显示)
  - [样式美化](#3样式美化)

## 1、下拉数据关联

[运行 CityLinkage.py](CityLinkage.py)

一个省市区关联的三级联动，数据源在data.json中

1. 主要用了`QComboBox`的`setModel`设置一个`QSortFilterProxyModel`过滤模型
2. 并根据唯一编码过滤，为了不影响内容显示，唯一编码的角色为`ToolTipRole`
3. 用`QColumnView`可以实现类似效果

![CityLinkage](ScreenShot/CityLinkage.gif)

## 2、文本居中显示

[运行 CenterText.py](CenterText.py)

1. 使用`QProxyStyle`对文件居中显示
2. 新增得item数据使用`setTextAlignment`对齐

![CenterText](ScreenShot/CenterText.png)

## 2、样式美化

[运行 ComboBoxStyle.py](ComboBoxStyle.py)

1. 使用`setView`使得`QComboBox`的下拉窗口支持样式
2. 通过`setAttribute`和`setWindowFlags`设置下拉窗口的属性，支持透明和无边框
3. 样式中通过`qlineargradient`设置 | 的渐变效果，让两端透明

![ComboBoxStyle](ScreenShot/ComboBoxStyle.png)
