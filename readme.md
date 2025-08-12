# DX Pass Generator

基于 PIL 的 DX Pass 图片生成器。

## 安装

1. 安装 Python 3.12 或更高版本；
2. 克隆该项目：
```bash
git clone https://github.com/nhdsd/dx-pass-generator
```
3. 安装依赖：
```bash
pip install -r requirements.txt
```
4. 安装资源文件(约 200 MiB)：[OneDrive](https://1drv.ms/u/c/68dff5f977fb346f/EWVbUaAGXVpNgOnmXDfGwY8BIDpuBi-IrsE2haxx-yK3jg)

## 使用

使用命令行操作。可以使用
```bash
py main.py -h
```
查看内置帮助（英文）。你也可以参考下表：
> [!WARNING]
> 不要从下表复制参数名！为了保证显示效果，下表的参数名包含了不间断连字符(`U+2011`)。此外，表头文字之间有文字连接符（`U+2060`）。

| 短⁠参⁠数 | 长⁠参⁠数 | 说⁠明 | 是⁠否⁠必⁠选 |
| --- | --- | --- | :---: |
| `‑h` | `‑‑help` | 显示帮助信息并退出。| |
| `‑l` | `‑‑pass‑level` | DX Pass 的等级。允许 `bronze`、`silver`、`gold`（默认）、`freedom`。不区分大小写。| |
| `‑c` | `‑‑chara` | 角色的 ID。可以通过查看 `resources/character` 下图片的文件名获取。可以忽略掉前导零。| :white_check_mark: |
| `‑b` | `‑‑background` | 背景的 ID。可以通过查看 `resources/background` 下图片的文件名获取。可以忽略掉前导零。 | :white_check_mark: |
| `‑n` | `‑‑name` | 自定义显示的角色名称。目前没有作用。| |
| `‑p` | `‑‑player‑name` | 玩家名称。为了方便起见，默认情况下玩家名称会被转换为全角的。| :white_check_mark: |
| | `‑‑full‑width` | 指定玩家名称使用全角字符显示。这也是默认效果。| |
| | `‑‑half‑width` | 指定玩家名称使用半角字符显示。这并不会把原有的全角字符转换为半角的。| |
| `‑r` | `‑‑rating` | 玩家的 DX Rating 值。| :white_check_mark: |
| `‑f` | `‑‑friend‑code` | 玩家的好友码。不指定就会显示为几条横线。你可以选择使用自定义的文本。| |
| `‑a` | `‑‑aime` | 玩家的 Aime 卡号。不指定就会留空。你可以选择使用自定义的文本。需要注意的是纯数字的 Aime 会被校验（超过 20 位报错，不足 20 位补零），并添加每 4 位之间的空格。| |
| | `‑‑raw‑aime` | 跳过纯数字 Aime 处理。目前不起作用。| |
| `‑v` | `‑‑version` | 版本信息。不指定就会留空。你可以选择使用自定义的文本。| |
| `‑q` | `‑‑qr‑code` | 二维码文本。不指定就会留空。| |
| `‑i` | `‑‑icon` | 左下方显示的增益效果。不指定就会留空。可以使用空格分隔多个效果图标名以输入多个效果。允许 `power1`~`power4`（旧版铜卡~白金卡的区域前进增幅效果）、`level`（旅行伙伴升级增幅）、`freedom`（自由模式时间延长）、`master`（解禁 Master 和 Re:Master 难度）、`rating`（显示参与 DX Rating 计算的乐曲）。| |
| `‑d` | `‑‑date` | 到期日期。留空会自动填写 14 日后的日期。支持 yyyymmdd、yyyy-mm-dd 和 yyyy/mm/dd。| |

生成示例图片（[`output.png`](./output.png)）：
```bash
py main.py -c 550105 -b 500001 -p AAAAAAAA -r 15000 -a 12345678901234567890 -v "[maimaiDX]1.55-0291" -q "C:\7sRef\System256\metaverse\lasthope" -i level master rating -d "20250826"
```

> [!WARNING]
> 每次输出会覆盖掉上一次的输出！请注意保存。

## 许可证

[Apache License 2.0](./LICENSE)