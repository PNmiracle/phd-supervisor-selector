# scripts/_archive/ —— 一次性历史脚本

**不要把这里的脚本当作可复用工具。** 这些是历史上某一次具体批次用的一次性脚本，
2026-10-07 瘦身时从技能根目录归置到这里，目的只是让根目录干净、便于 grep。

| 文件 | 当时用途 | 现在该用什么 |
|---|---|---|
| `vika-batch-patch.py` | 给 5 条已有记录补 OneWayLink 学校关联 | `references/vika-school-link.md` 的六步 + `vika-guide.md` §3/§4 |
| `vika-patch-links.py` | 同样给 5 条记录补 OneWayLink | 同上 |
| `vika-write-missouri.py` | 某次 Missouri 批次的写入脚本 | `vika-guide.md` §0.5 / §3 的代码模板 |
| `yangziyi-batch3.py` | 杨子怡 Finance 方向第三批（32 条）写入 | 同上 |

**注意**：`vika-patch-links.py` 与 `vika-write-missouri.py` 用相对路径读 `env.json`，
移动到本目录后**原样运行会找不到 `env.json`**。这也是不建议复用的原因之一——
新的一次性操作请改用 `vika-guide.md` 的模板，不要就地改这些脚本。

留它们在这里的唯一价值是「当年这批记录是怎么写进去的」这一份溯源信息。
若确认无溯源需求，可直接删除（git 历史里仍有）。
