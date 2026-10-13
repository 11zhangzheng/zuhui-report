<div align="center">

<img src="./assets/zuhui-report-256.png" width="88" alt="zuhui-report icon">

# 📝 zuhui-report

**把跟 AI 迭代科研的整段对话，一键变成组会汇报。**

<sub>组会前一分钟，把散落在对话里的进展、结果、卡点、计划，整理成一份能直接交给导师的 Markdown。</sub>

<sub><b>中文</b> · <a href="./README_en.md">English</a></sub>

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-5A67D8?style=flat-square)](https://agentskills.io)
[![Codex](https://img.shields.io/badge/Codex-✓-000000?style=flat-square)](https://developers.openai.com/codex/skills/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-✓-D97706?style=flat-square)](https://claude.ai/code)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](./LICENSE)
[![Output: Markdown](https://img.shields.io/badge/Output-Markdown-0B7285?style=flat-square)](#-输出示例)
[![No PPT](https://img.shields.io/badge/Only-Markdown-important?style=flat-square)](#-边界与常见问题)

</div>

---

## 😩 你是不是也这样

> 组会前一小时，你盯着屏幕上几百轮对话记录，脑子里全是这几天跟 AI 调参、推公式、改代码的碎片。
>
> 你想汇报，但：
> - 进展和"还在想的"混在一起，说不清哪些真做完了；
> - 失败的实验不想提，又怕导师一问就露馅；
> - 从零写一份汇报，光是组织语言就要半小时。

**zuhui-report 就是为这个时刻做的。** 它不读文件、不配置环境、不联网——直接读取你**当前这段会话的上下文**，提炼科研内容，输出一份可以直接发给导师的组会汇报。

## ✨ 它能做什么

- **五分类提炼**：已完成进展 / 实验与结果 / 现存难点 / 下一步计划 / 待讨论问题，一次分好。
- **完成与计划严格分离**：只是设想、还没验证的，自动标注 **【待验证】**，绝不把"想做"写成"做完了"。
- **失败实验如实记录**：不粉饰、不回避，导师最想看的恰恰是这些。
- **三种输出模式**：`full` 完整书面报告 / `brief` 口头汇报提纲 / `ppt-outline` 直接贴进 PPT 的要点。
- **导师提问预判**：根据你的项目内容，自动生成 3–5 条导师大概率会追问的问题，让你提前想好怎么答。
- **只输出 Markdown**：不生成 PPT 文件，不改写夸大，所有内容都能追溯到这段对话。

## 🚀 安装

`zuhui-report` 是一个标准的 Agent Skill（`SKILL.md` + `agents/openai.yaml`）。

### 方式一：Codex（推荐）

把仓库放进 Codex 会扫描的 skills 目录：

```bash
# 项目级（跟着仓库走，团队共用）
git clone <this-repo> .agents/skills/zuhui-report

# 用户级（本机所有项目可用）
git clone <this-repo> ~/.agents/skills/zuhui-report
```

在 Codex 里直接说一句话即可触发，或用 `/skills` / `$zuhui-report` 显式调用。

### 方式二：Claude Code

```bash
git clone <this-repo> ~/.claude/skills/zuhui-report
```

### 方式三：把安装交给 AI

把下面这段原样复制给任意 AI coding agent：

```text
请安装 zuhui-report 这个 Agent Skill：
1. 把仓库 clone 到 .agents/skills/zuhui-report（Claude Code 环境则用 .claude/skills/zuhui-report）。
2. 读取并遵循目录里的 SKILL.md 与 agents/openai.yaml。
3. 安装完成后告诉我它放在哪里，以及怎么用。
```

## 🗣️ 使用

在任意与 AI 迭代科研的会话末尾，直接说：

```
把这次对话整理成组会汇报
```

带参数也可以：

```
用 brief 模式，不要附录，字数控制在 800 字
```

```
生成组会汇报，只要 ppt-outline，并预判导师可能的问题
```

## 🎛️ 配置参数

| 参数 | 取值 | 默认 | 说明 |
|---|---|---|---|
| `output_mode` | `brief` / `full` / `ppt-outline` | `full` | 精简提纲 / 完整书面 / PPT 要点 |
| `include_appendix` | `true` / `false` | `true` | 是否附相关文献、关键代码改动摘要 |
| `include_question_prediction` | `true` / `false` | `true` | 是否生成导师潜在提问预判 |
| `filter_debug_noise` | `true` / `false` | `true` | 是否过滤调试日志、废弃草稿、闲聊 |
| `max_words` | 整数 | `2000` | 汇报正文最大字数 |

## 📋 输出示例

每种模式都有可直接查看的样例：

- 📝 完整书面报告：[`examples/example-output.md`](examples/example-output.md)
- 🗣️ 口头汇报提纲（`brief`）：[`examples/example-output-brief.md`](examples/example-output-brief.md)
- 📊 PPT 要点（`ppt-outline`）：[`examples/example-output-ppt-outline.md`](examples/example-output-ppt-outline.md)
- 🇬🇧 英文完整报告：[`examples/example-output-en.md`](examples/example-output-en.md)

结构如下：

```markdown
# 组会汇报 - 【项目名称】
## 一、本周工作进展
## 二、实验/研究结果      # 有效结果与失败尝试分开列
## 三、现存难点与踩坑      # 含已尝试的手段与效果
## 四、下一步工作计划      # 拆成可量化任务
## 五、需要组会讨论的问题
## 附录                   # 可选：文献 / 代码摘要
## 导师潜在提问预判         # 可选：3–5 条
```

## 🗂️ 仓库结构

```text
zuhui-report/
├── SKILL.md                 # 核心指令：流程、抽取规则、模板、约束
├── agents/
│   └── openai.yaml          # Codex UI 元数据（显示名、默认提示语、图标）
├── assets/                  # 技能图标（PNG + SVG）
├── examples/                # 各模式输出样例（full / brief / ppt-outline / 英文）
├── README.md / README_en.md
└── LICENSE
```

## 🚧 边界与常见问题

- **它会读文件吗？** 不会。它只读**当前会话的上下文**，这正是它"零配置"的原因。
- **会生成 PPT 吗？** 不会，只输出 Markdown（`ppt-outline` 模式给的是可粘贴的要点文本）。需要 `.pptx` 请配合 PPT 类 skill。
- **没有对话记录能用吗？** 不能。没有上下文时它会明确告诉你信息不足，而不是凭空编。
- **会编造实验和结论吗？** 约束里写死了"所有内容必须来源于当前对话"，设想内容一律标注【待验证】。

## 🤝 贡献

欢迎提 Issue 和 PR：新增输出模板、优化提问预判策略、补充示例都很有价值。

## 📄 License

[MIT](./LICENSE)

<div align="center"><sub>如果你也在组会前手忙脚乱，点个 ⭐ 让它被更多同伴看到。</sub></div>
