# NSFC Agent Skills

> **国家自然科学基金（NSFC）申请书撰写辅助技能包**

这是一个专为 NSFC 申请书撰写设计的 Agent Skills 集合，帮助科研人员提高申请书质量，涵盖写作指导、图表制作、文献管理和政策速查等核心环节。

## 📦 技能包概览

本项目包含 4 个专业技能，每个技能都可以独立使用：

| 技能名称 | 功能简介 | 适用场景 |
|---------|---------|---------|
| **[nsfc-write](./nsfc-write/SKILL.md)** | NSFC 申请书撰写指南 | 选题、摘要、立项依据、研究内容、研究方案、创新性分析等各部分撰写 |
| **[nsfc-figure](./nsfc-figure/SKILL.md)** | NSFC 申请书图表制作指南 | 概念图、技术路线图、研究内容关系图、甘特图等专业图表制作 |
| **[nsfc-literature](./nsfc-literature/SKILL.md)** | NSFC 申请书文献检索与引用 | 使用 OpenAlex API 检索文献，使用 wenxian 生成标准引用格式 |
| **[nsfc-policy](./nsfc-policy/SKILL.md)** | NSFC 2026 年度申报政策速查 | 限项规定、AI 使用规范、申请代码、项目类型、结构改革等政策信息 |

## 🚀 如何使用（OpenClaw）

### 什么是智能体技能？

本项目遵循 [AgentSkills](https://agentskills.io) 规范，这是一个为 AI 智能体设计的结构化知识库格式。每个技能都是一个包含 `SKILL.md` 文件的目录，文件中包含 YAML frontmatter 和 Markdown 格式的指导内容。

### 在 OpenClaw 中使用

将本仓库克隆到本地后，OpenClaw 会自动识别和加载这些技能：

```bash
git clone https://github.com/njzjz/nsfc-agent-skills.git
cd nsfc-agent-skills
```

OpenClaw 会根据 [官方文档](https://docs.openclaw.ai/tools/skills) 自动管理技能的加载和配置。

## ⚠️ 免责声明

- 本技能包仅供学习和参考，不保证申请成功
- 请务必遵守 NSFC 的科研诚信要求和 AI 使用规范
- 不得使用 AI 直接生成申请书，必须人工核实所有内容
- 政策信息以基金委当年官方指南为准
