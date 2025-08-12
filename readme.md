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
4. 安装资源文件(约 200 MiB)：[OneDrive](https://1drv.ms/u/c/68dff5f977fb346f/EWVbUaAGXVpNgOnmXDfGwY8BIDpuBi-IrsE2haxx-yK3jg)

## 使用

目前未实现 IO，需要自行修改 [`main.py`](./main.py) 中的常量的值。
输出为 [`output.png`](./output.png)，此仓库中已有的为示例输出。

> [!WARNING]
> 每次输出会覆盖掉上一次的输出！请注意保存。

## 许可证

[Apache License 2.0](./LICENSE)