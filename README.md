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

Agent Skills 是为 AI Agent 设计的结构化知识库，以 Markdown 格式存储专业知识和操作指南。通过将这些技能加载到 openclaw 等 AI 工具中，Agent 可以获得特定领域的专业能力。

### 在 openclaw 中使用本技能包

#### 方式一：通过技能目录安装（推荐）

如果 openclaw 支持技能市场或技能目录：

```bash
# 安装所有技能
openclaw skills install njzjz/nsfc-agent-skills

# 或单独安装某个技能
openclaw skills install njzjz/nsfc-agent-skills/nsfc-write
openclaw skills install njzjz/nsfc-agent-skills/nsfc-figure
```

#### 方式二：本地加载技能

1. **克隆本仓库**：
   ```bash
   git clone https://github.com/njzjz/nsfc-agent-skills.git
   cd nsfc-agent-skills
   ```

2. **配置 openclaw**：

   在 openclaw 的配置文件中添加技能路径，参考 [openclaw 技能文档](https://docs.openclaw.ai/tools/skills)：

   ```yaml
   # openclaw 配置示例
   skills:
     - path: /path/to/nsfc-agent-skills/nsfc-write
       enabled: true
     - path: /path/to/nsfc-agent-skills/nsfc-figure
       enabled: true
     - path: /path/to/nsfc-agent-skills/nsfc-literature
       enabled: true
     - path: /path/to/nsfc-agent-skills/nsfc-policy
       enabled: true
   ```

3. **与 Agent 对话时调用技能**：

   ```
   用户：帮我写一份 NSFC 面上项目的立项依据部分
   
   Agent：（自动加载 nsfc-write 技能）
         根据 NSFC 申请书撰写指南，立项依据部分应该...
   ```

#### 方式三：直接引用技能内容

如果 openclaw 支持直接引用 Markdown 文件：

```bash
openclaw chat --skill-file ./nsfc-write/SKILL.md
```

### 使用示例

#### 场景 1：撰写申请书摘要

```
用户：我在研究机器学习势函数，请帮我写一份 400 字的项目摘要

Agent：（使用 nsfc-write 技能）
      根据 NSFC 摘要撰写模板，我为您起草如下：
      
      "机器学习势函数（MLP）作为连接量子力学与分子动力学的桥梁，
      在材料设计和药物发现中展现出巨大潜力。针对......"
```

#### 场景 2：制作技术路线图

```
用户：我需要为申请书制作一张技术路线图，展示"数据收集→模型训练→性能评估→应用验证"的流程

Agent：（使用 nsfc-figure 技能）
      我为您生成 Mermaid 流程图代码如下：
      
      ```mermaid
      graph LR
          A[数据收集] --> B[模型训练]
          B --> C[性能评估]
          C --> D[应用验证]
          D -->|反馈优化| B
      ```
      
      您可以使用 https://mermaid.live 导出为高分辨率图片。
```

#### 场景 3：检索相关文献

```
用户：帮我查找近 3 年关于"深度学习分子动力学"的高引文献

Agent：（使用 nsfc-literature 技能）
      使用 OpenAlex API 为您检索...
      
      1. "Machine learning force fields" (Nature, 2021, 引用 1250+)
      2. "Deep potential molecular dynamics" (PRL, 2023, 引用 890+)
      ...
```

#### 场景 4：查询申报政策

```
用户：2026 年青年基金有什么新变化？

Agent：（使用 nsfc-policy 技能）
      根据 2026 年度政策：
      
      - 交叉科学部新增受理青年 C 类项目
      - 博士生/优秀本科生也可申请
      - 代表作需说明个人贡献情况（新要求）
      - 必须全面如实声明 AI 使用情况
```

## 📖 技能详细说明

### nsfc-write：申请书撰写指南

提供全面的 NSFC 申请书撰写指导，包括：

- **核心理念**：申请书的本质、精炼原则、三要素框架、讲故事技巧
- **前置部分**：选题策略、题目撰写、摘要模板
- **正文部分**：立项依据、研究内容、研究目标、关键科学问题、研究方案、可行性分析、特色与创新、年度计划、预期成果、研究基础
- **项目类型**：青年 C 类、面上项目、重点项目的特别建议
- **评审视角**：评审要点、常见扣分点、逆向思维
- **写作技巧**：语气文风、动宾结构、避免的表达

**亮点**：
- 提供具体的撰写模板和示例
- 覆盖不同项目类型的差异化建议
- 包含详细的评审标准和扣分点分析

### nsfc-figure：图表制作指南

指导如何制作专业的申请书图表：

- **图表类型**：概念图、研究内容关系图、技术路线图、研究基础展示图、甘特图
- **制作工具**：Mermaid、Python (matplotlib)、TikZ、PowerPoint
- **设计原则**：配色、字体、分辨率、布局
- **常见错误**：从 PDF 截图、信息过载、格式不统一等

**亮点**：
- 提供 Mermaid 代码模板，可直接修改使用
- 包含多种图表布局方式（层层递进型、并行支撑型、闭环迭代型）
- 针对不同项目类型给出图表数量建议

### nsfc-literature：文献检索与引用

提供免费的文献检索和引用生成工具：

- **OpenAlex API**：免费检索学术文献（无需 API key）
- **wenxian**：生成标准引用格式（BibTeX、纯文本）
- **检索策略**：关键词选择、高引论文、最新进展
- **引用规范**：NSFC 编号引用格式、格式统一性

**亮点**：
- 提供 Python 脚本，开箱即用
- 支持按引用数、发表日期排序
- 支持年份范围筛选

### nsfc-policy：申报政策速查

汇总 2026 年度 NSFC 申报政策要点：

- **结构改革**："瘦身提质"，正文不超过 30 页
- **代表作制度**：需说明个人贡献情况
- **AI 使用规范**：可用 AI 辅助，但必须声明，不得直接生成申请书
- **项目类型**：青年 C、面上、重点、重大研究计划、联合基金
- **限项规定**：同层次人才计划限制、重点项目限制
- **评审流程**：形式审查、通讯评审、会议评审

**亮点**：
- 快速查找关键政策信息
- 避免因政策不熟悉导致的低级错误
- 包含 2025 年度申请数据参考

## 🛠️ 本地开发与测试

如果您想在本地测试或扩展这些技能：

```bash
# 克隆仓库
git clone https://github.com/njzjz/nsfc-agent-skills.git
cd nsfc-agent-skills

# 查看技能文件
cat nsfc-write/SKILL.md
cat nsfc-figure/SKILL.md
cat nsfc-literature/SKILL.md
cat nsfc-policy/SKILL.md

# 测试文献检索脚本（需要安装 uv）
uv run nsfc-literature/scripts/search_literature.py "machine learning potential" --limit 10

# 测试图表生成脚本
uv run nsfc-figure/scripts/generate_roadmap.py \
  --title "技术路线图" \
  --nodes "数据采集,模型训练,评估,应用" \
  --output roadmap.png
```

## 📝 技能文件结构

每个技能目录遵循标准的 Agent Skills 格式：

```
nsfc-xxx/
├── SKILL.md          # 技能主文件（包含 frontmatter 和内容）
├── scripts/          # 辅助脚本（可选）
│   └── *.py
└── references/       # 参考资料（可选）
    └── *.md
```

**SKILL.md 格式**：

```markdown
---
name: skill-name
description: 技能的简短描述
version: 0.1.0
---

# 技能标题

## 技能内容

详细的指导内容...
```

## 🤝 贡献指南

欢迎贡献！如果您有改进建议或发现错误，请：

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

**贡献内容可以包括**：
- 补充或更新申请书撰写技巧
- 添加新的图表模板
- 改进文献检索脚本
- 更新最新的政策信息
- 修正错误或改进文档

## ⚠️ 免责声明

- 本技能包仅供学习和参考，不保证申请成功
- 请务必遵守 NSFC 的科研诚信要求和 AI 使用规范
- 不得使用 AI 直接生成申请书，必须人工核实所有内容
- 政策信息以基金委当年官方指南为准

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件（如有）

## 📧 联系方式

- **作者**：njzjz
- **项目主页**：https://github.com/njzjz/nsfc-agent-skills
- **问题反馈**：https://github.com/njzjz/nsfc-agent-skills/issues

## 🔗 相关资源

- [NSFC 官网](https://www.nsfc.gov.cn/)
- [openclaw 文档](https://docs.openclaw.ai/tools/skills)
- [OpenAlex API](https://docs.openalex.org/)
- [wenxian 工具](https://github.com/njzjz/wenxian)

---

**祝您申请顺利！🎉**
