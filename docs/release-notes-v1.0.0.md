# v1.0.0 — 首个可用版本 / Initial Release

> 把跟 AI 迭代科研的整段对话，一键变成组会汇报。
>
> Turn a whole research session with your AI into a lab-meeting report — in one shot.

`zuhui-report` 是一个标准 Agent Skill：读取**当前会话上下文**，提炼科研工作内容，输出可直接交给导师的组会汇报 Markdown。零配置、不读文件、不联网。

---

## ✨ 主要特性

- **五分类提炼**：已完成进展 / 实验与结果 / 现存难点 / 下一步计划 / 待讨论问题，一次分好。
- **完成与计划严格分离**：未验证的设想自动标注 **【待验证】**，绝不把"想做"写成"做完了"。
- **失败实验如实记录**：不粉饰、不回避。
- **三种输出模式**：`full` 完整书面报告 / `brief` 口头汇报提纲 / `ppt-outline` 贴 PPT 的要点。
- **导师提问预判**：自动生成 3–5 条导师大概率会追问的问题。
- **五项可配置参数**：`output_mode`、`include_appendix`、`include_question_prediction`、`filter_debug_noise`、`max_words`。
- **只输出 Markdown**：不生成 PPT，不夸大成果，所有内容可追溯到当前对话。

## 📦 包含内容

```
zuhui-report/
├── SKILL.md                     # 核心指令：流程、抽取规则、模板、约束
├── agents/openai.yaml           # Codex UI 元数据（显示名/默认提示语/图标）
├── assets/                      # 技能图标（PNG + SVG）
├── examples/                    # 四种输出样例（full / brief / ppt-outline / 英文）
├── README.md / README_en.md     # 中文 + 英文说明
└── LICENSE (MIT)
```

## 🚀 安装

**Codex**（项目级 / 用户级）：

```bash
git clone https://github.com/11zhangzheng/zuhui-report.git .agents/skills/zuhui-report
git clone https://github.com/11zhangzheng/zuhui-report.git ~/.agents/skills/zuhui-report
```

**Claude Code**：

```bash
git clone https://github.com/11zhangzheng/zuhui-report.git ~/.claude/skills/zuhui-report
```

## 🗣️ 使用

在会话末尾直接说：

```
把这次对话整理成组会汇报
用 brief 模式，不要附录，字数控制在 800 字
```

## 🚧 范围说明

- 只读**当前会话上下文**，不读取文件、不联网。
- 只输出 Markdown，不生成 `.pptx`。
- 没有对话上下文时会如实提示信息不足，不凭空编造。

## 🇬🇧 English

**zuhui-report v1.0.0 — Initial Release.** An Agent Skill that turns your current AI research session into a structured lab-meeting report in Markdown. Five-way extraction (progress / results / blockers / next steps / questions), done-vs-planned separation with a 【待验证】 tag, three output modes (`full` / `brief` / `ppt-outline`), and predicted advisor questions. Works with Codex and Claude Code. Markdown only — no PPT, no fabrication. See the [README](./README_en.md) for details.

---

**Full Changelog**: initial release.
