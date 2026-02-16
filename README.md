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

## 🚀 如何使用（openclaw）

### 什么是 Agent Skills？

本项目遵循 [AgentSkills](https://agentskills.io) 规范，这是一个为 AI Agent 设计的结构化知识库格式。每个技能都是一个包含 `SKILL.md` 文件的目录，文件中包含 YAML frontmatter 和 Markdown 格式的指导内容。

### 在 OpenClaw 中使用

OpenClaw 原生支持 AgentSkills 格式。根据 [OpenClaw 文档](https://docs.openclaw.ai/tools/skills)，技能从以下位置加载（优先级从高到低）：

1. **工作区技能**：`<workspace>/skills`（最高优先级）
2. **本地技能**：`~/.openclaw/skills`
3. **捆绑技能**：随 OpenClaw 安装包一起发布

#### 使用方式一：通过 ClawHub 安装

[ClawHub](https://clawhub.com) 是 OpenClaw 的公共技能注册中心。如果本技能已发布到 ClawHub：

```bash
# 安装技能到当前工作区
clawhub install nsfc-agent-skills

# 或安装到 OpenClaw 的共享技能目录
clawhub install nsfc-agent-skills --global
```

#### 使用方式二：手动安装到工作区

将技能目录复制到 OpenClaw 工作区的 `skills` 文件夹：

```bash
# 克隆仓库
git clone https://github.com/njzjz/nsfc-agent-skills.git

# 复制技能到 OpenClaw 工作区（假设工作区在 ~/my-openclaw-workspace）
cp -r nsfc-agent-skills/nsfc-write ~/my-openclaw-workspace/skills/
cp -r nsfc-agent-skills/nsfc-figure ~/my-openclaw-workspace/skills/
cp -r nsfc-agent-skills/nsfc-literature ~/my-openclaw-workspace/skills/
cp -r nsfc-agent-skills/nsfc-policy ~/my-openclaw-workspace/skills/
```

#### 使用方式三：配置额外的技能目录

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/nsfc-agent-skills"]
    }
  }
}
```

OpenClaw 会自动加载该目录下的所有技能子目录（`nsfc-write`、`nsfc-figure` 等）。

#### 技能配置（可选）

如果技能需要 API 密钥或环境变量，可在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "nsfc-literature": {
        "enabled": true,
        "env": {
          "OPENALEX_EMAIL": "your-email@example.com"
        }
      }
    }
  }
}
```

## ⚠️ 免责声明

- 本技能包仅供学习和参考，不保证申请成功
- 请务必遵守 NSFC 的科研诚信要求和 AI 使用规范
- 不得使用 AI 直接生成申请书，必须人工核实所有内容
- 政策信息以基金委当年官方指南为准
