# DX Pass Generator

基于 PIL 的 DX Pass 图片生成器。

> [!WARNING]
> 此项目正在开发当中。
> 目前的可用程度：**基本可用**。

## 安装

1. 安装 Python 3.12 或更高版本；
2. 克隆该项目：
   ```
   git clone https://github.com/nhdsd/dx-pass-generator
   ```
3. 安装依赖：
    ```
    pip install -r requirements.txt
    ```
4. 安装资源文件：
   > [!NOTE]
   > 资源文件正在整理中，链接将在后续提供。
   > 自 FESTiVAL 代起，原始资源文件的质量显著下降，并且纵横比不正确。
   > 我们修复了纵横比，但是对于画质问题我们无能为力。

## 使用

目前未实现 IO，需要自行修改 [`main.py`](./main.py) 中的常量的值。
输出为 [`output.png`](./output.png)，此仓库中已有的为示例输出。

> [!WARNING]
> 每次输出会覆盖掉上一次的输出！请注意保存。

## 许可证

[Apache License 2.0](./LICENSE)