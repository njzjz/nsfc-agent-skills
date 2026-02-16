---
name: nsfc-proposal
description: >
  撰写国家自然科学基金（NSFC）项目申请书。支持青年科学基金（C类）等项目类型。
  覆盖立项依据、研究内容、研究基础等全部章节的撰写指导，包含文献搜索与引用生成。
  Use when: (1) 用户需要撰写或修改 NSFC 基金申请书, (2) 需要搜索学术文献并生成引用,
  (3) 需要了解 NSFC 申请书的结构和写作规范, (4) 需要根据评审标准优化申请书内容。
---

# NSFC 基金申请书撰写 Skill

## 总体流程

1. **确定项目类型** → 加载对应模板（见 `references/templates/`）
2. **确定研究方向** → 搜索相关文献（用 `scripts/search_literature.py`）
3. **逐章节撰写** → 按模板结构，参考写作指南
4. **生成参考文献** → 用 `wenxian` skill 或 `scripts/generate_references.py`
5. **审查优化** → 对照评审标准检查

## 项目类型

当前支持：
- **青年科学基金（C类）** → `references/templates/youth-c.md`

后续可扩展：面上项目、重点项目等，添加对应模板文件即可。

## 写作规范

### 通用原则
- 正文不超过 30 页，鼓励简洁表达
- 不得删除或改动提纲标题及括号中的文字
- 层次分明，标题突出，内容翔实清晰
- 两类研究属性：「自由探索类基础研究」或「目标导向类基础研究」

### AI 使用声明（2026年新规）
如借助 AI 技术跟踪研究动态、收集整理参考文献，须：
- 人工核实 AI 生成信息和参考文献的真实性
- 全面如实声明使用情况
- 按规定对 AI 生成内容进行标识
- **不得使用 AI 直接生成的申请书，不得使用未经核实的生成内容**

⚠️ 本 skill 用于辅助撰写，所有输出必须经申请人审核确认。

## 文献工具

### 搜索文献
```bash
python3 scripts/search_literature.py "关键词" [--limit 10] [--year-from 2020]
```
使用 OpenAlex API（免费，无需 API key），返回标题、DOI、引用数、摘要等。

### 生成引用
```bash
python3 scripts/generate_references.py dois.txt [--format bibtex|text|markdown]
```
批量调用 `wenxian` 从 DOI 列表生成参考文献。也可直接使用 wenxian skill：
```bash
uvx wenxian from <DOI>
```

## 各章节写作指导

详见 `references/writing-guide.md`（待补充，需从专家报告和范本中脱敏提炼）。

## 评审标准

详见 `references/review-criteria.md`（待补充）。

## 文件结构

```
nsfc-proposal/
├── SKILL.md                          # 本文件
├── references/
│   ├── templates/
│   │   └── youth-c.md                # 青年C类申请书结构模板
│   ├── writing-guide.md              # 写作技巧（待补充）
│   └── review-criteria.md            # 评审标准（待补充）
└── scripts/
    ├── search_literature.py          # OpenAlex 文献搜索
    └── generate_references.py        # 批量引用生成
```
