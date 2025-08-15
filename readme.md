# DX Pass Generator

基于 PIL 的 DX Pass 图片生成器。

## 安装

### 从源代码使用
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
   在根目录下新建 `resources` 目录，并把内容解压到该目录下。
   
### 从可执行文件使用（仅限 Windows）
1. 前往 [Release](https://github.com/nhdsd/dx-pass-generator/releases) 页面。
2. 下载可执行文件压缩包并解压。
3. 安装资源文件(约 200 MiB)：[OneDrive](https://1drv.ms/u/c/68dff5f977fb346f/EWVbUaAGXVpNgOnmXDfGwY8BIDpuBi-IrsE2haxx-yK3jg)  
   在根目录下新建 `resources` 目录，并把内容解压到该目录下。

> 注：仓库中包含的资源文件是给 GitHub Actions 使用的。

<details>
   <summary>实验性内容...</summary>
   实验性内容链接(约 50 MiB)：<a href="https://1drv.ms/u/c/68dff5f977fb346f/EVBcx0tfUJ1JuYThQyk2nsMBee_19dfnhLsGTCgpHk_V2g?e=AXyHLx">OneDrive</a><br>
   将内容复制到资源目录下即可。
</details>

## 使用

使用命令行操作。参数可参考下表。所有参数都有默认值，带有 :ballot_box_with_check: 的参数不接受值（布尔型参数）：
> [!WARNING]
> 不要从下表复制参数名！为了保证显示效果，下表的参数名包含了不间断连字符（`U+2011`）。此外，表头文字之间有文字连接符（`U+2060`）。

| 短⁠参⁠数 | 长⁠参⁠数 | 说⁠明 |
| --- | --- | --- |
| `‑h` | `‑‑help` | :ballot_box_with_check: 显示帮助信息并退出。|
| `‑l` | `‑‑pass‑level` | DX Pass 的等级。允许 `bronze`、`silver`、`gold`（默认）、`freedom`。不区分大小写。|
| `‑c` | `‑‑chara` | 角色的 ID。可以通过查看 `resources/character` 下图片的文件名获取。可以忽略掉前导零。不指定就会随机抽取。|
| `‑C` | `‑‑chara‑from` | 从指定路径加载角色图片。如果指定该选项，那么必须要指定 `‑n`/`‑‑name`。图片会被缩放到 768 \* 1052。|
| `‑b` | `‑‑background` | 背景的 ID。可以通过查看 `resources/background` 下图片的文件名获取。可以忽略掉前导零。不指定就会随机抽取。|
| `‑B` | `‑‑background‑from` | 从指定路径加载背景图片。图片会被缩放到 768 \* 1052。|
| *`‑H`* | *`‑‑holographic`* | :ballot_box_with_check: :warning:**实验性**:warning: 应用镭射效果。目前的镭射效果底图的视觉效果很差，且遮罩图片包含大量实际打印时不会出现的极小区域，严重限制了本参数的视觉效果（大多数时候是反效果）。只会应用角色遮罩以在一定程度上提升视觉效果（但还是不好看）。|
| | *`‑‑holo‑from`* | :warning:**实验性**:warning: 从指定路径加载镭射效果底图。|
| `‑n` | `‑‑name` | 自定义显示的角色名称。|
| | `‑‑skip‑name` | :ballot_box_with_check: 完全跳过角色名生成。|
| | `‑‑discard‑comment` | :ballot_box_with_check: 忽略角色名中 \[\] 的部分。此选项是给音击角色设计的。|
| `‑p` | `‑‑player‑name` | 玩家名称。不指定会显示为 "maimai"。为了方便起见，默认情况下玩家名称会被转换为全角的。|
| | `‑‑full‑width` | :ballot_box_with_check: 指定玩家名称使用全角字符显示。这也是默认效果。|
| | `‑‑half‑width` | :ballot_box_with_check: 指定玩家名称使用半角字符显示。这并不会把原有的全角字符转换为半角的。|
| | `‑‑skip‑player‑name` | 完全跳过玩家名称生成。|
| `‑r` | `‑‑rating` | 玩家的 DX Rating 值。不指定就会显示为几条横线。|
| | `‑‑override‑rating` | 使用此处的值而不是 `‑r`/`‑‑rating` 中的值来决定使用什么 DX Rating 框。|
| | `‑‑skip‑rating` | :ballot_box_with_check: 完全跳过 DX Rating 生成。|
| `‑f` | `‑‑friend‑code` | 玩家的好友码。不指定就会显示为几条横线。你可以选择使用自定义的文本。|
| | `‑‑skip‑friend‑code` | :ballot_box_with_check: 完全跳过好友码生成。|
| `‑a` | `‑‑aime` | 玩家的 Aime 卡号。不指定就会留空。你可以选择使用自定义的文本。需要注意的是纯数字的 Aime 会被校验（超过 20 位报错，不足 20 位补零），并添加每 4 位之间的空格。|
| | `‑‑raw‑aime` | :ballot_box_with_check: 跳过纯数字 Aime 处理。|
| `‑v` | `‑‑version` | 版本信息。不指定就会留空。你可以选择使用自定义的文本。|
| `‑q` | `‑‑qr‑code` | 二维码文本。不指定就会使用默认的占位符。|
| | `‑‑empty‑qr‑code` | :ballot_box_with_check: 不显示二维码。| 
| | `‑‑skip‑qr‑code` | :ballot_box_with_check: 完全跳过二维码生成。|
| `‑i` | `‑‑icon` | 左下方显示的增益效果。不指定就会留空。可以使用空格分隔多个效果图标名以输入多个效果。允许 `power1`\~`power4`（旧版铜卡\~白金卡的区域前进增幅效果）、`level`（旅行伙伴升级增幅）、`freedom`（自由模式时间延长）、`master`（解禁 Master 和 Re:Master 难度）、`rating`（显示参与 DX Rating 计算的乐曲）。|
| `‑d` | `‑‑date` | 到期日期。留空会自动填写 14 日后的日期。支持 yyyymmdd、yyyy-mm-dd 和 yyyy/mm/dd。|
| | `‑‑skip‑date` | :ballot_box_with_check: 完全跳过日期生成。|
| | `‑‑skip-name-date` | :ballot_box_with_check: 在`‑‑skip‑name`和`‑‑skip‑date`的基础上，跳过它们下方的底板的生成。|
| | `‑‑skip‑all` | :ballot_box_with_check: 上述所有`‑‑skip`选项的叠加。|
| `‑o` | `‑‑output` | 输出路径。不指定会使用"`output.png`"。默认会覆盖已有文件。|
| | `--no-override` | :ballot_box_with_check: 如果输出路径下已经有同名文件，不保存生成结果而是报错退出。 |

生成示例图片（[`output.png`](./output.png)）：
```bash
py main.py -c 550105 -b 500001 -p AAAAAAAA -r 15000 -a 12345678901234567890 -v "[maimaiDX]1.55-0291" -q "C:\7sRef\System256\metaverse\lasthope" -i level master rating -d "20250826"
```

> [!WARNING]
> 每次输出会覆盖掉上一次的输出！请注意保存。

## 计划中功能

下面列表的顺序是计划实现这些功能的顺序，但是实际顺序可能依据实现难度而变化。

- 镭射效果降噪与底图替换
- 中二节奏角色与背景资源

## 许可证

[Apache License 2.0](./LICENSE.txt)
