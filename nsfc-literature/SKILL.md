---
name: nsfc-literature
description: NSFC申请书文献检索与引用生成。使用OpenAlex API免费搜索学术文献，使用wenxian生成标准引用格式。
version: 0.1.0
---

# NSFC 申请书文献检索与引用生成

## 文献在申请书中的要求

- 参考文献约**30条**，以近5年为主
- CNS等权威期刊优先
- **国际文献为主** + 国内文献为辅 + 自己的工作（可高亮）
- 不要遗漏领域关键文献（评审人会注意）
- 格式必须统一规范
- 有当年文献加分
- 勿缺失关键参考文献

---

## 文献检索

### OpenAlex API（免费，无需API key）

**脚本**：`scripts/search_literature.py`

**基本用法**：
```bash
# 搜索关键词，按引用数排序
python scripts/search_literature.py "machine learning potential" --max-results 20 --sort cited_by_count

# 搜索近3年的文献
python scripts/search_literature.py "deep learning molecular dynamics" --year-from 2023

# 按发表日期排序（找最新文献）
python scripts/search_literature.py "neural network force field" --sort publication_date
```

**返回信息**：标题、作者、期刊、年份、DOI、引用数、摘要

**搜索策略建议**：
1. 先用宽泛关键词搜索了解领域全貌
2. 再用精确关键词搜索特定方向
3. 关注高引论文（领域经典）和最新论文（前沿动态）
4. 检查是否遗漏领域大牛的工作
5. 搜索中文关键词时可能需要用英文替代

---

## 引用生成

### wenxian skill（需要代理）

**前置条件**：
- 需要 `wenxian` skill 已安装
- 需设置代理：`https_proxy=http://localhost:7890`

**脚本**：`scripts/generate_references.py`

**用法**：
```bash
# 从DOI列表文件生成BibTeX引用
https_proxy=http://localhost:7890 python scripts/generate_references.py refs.txt --format bibtex

# 生成纯文本引用
https_proxy=http://localhost:7890 python scripts/generate_references.py refs.txt --format plain
```

**refs.txt 格式**（每行一个标识符）：
```
10.1103/PhysRevLett.120.143001
10.1038/s41586-020-2242-8
arXiv:2304.09423
```

### NSFC引用格式

NSFC申请书通常使用**编号引用格式** [1], [2], ...

**格式示例**：
```
[1] 作者1, 作者2, 等. 标题. 期刊, 卷(期): 起始页-结束页, 年份.
[2] Author1, Author2, et al. Title. Journal, Volume(Issue): Pages, Year.
```

**注意**：
- 所有文献格式必须统一（姓名顺序、期刊缩写等）
- 建议手动录入基金委成果系统保持格式一致
- 自己的文献可以**加粗**或用其他方式高亮

---

## 完整工作流程

```
1. 确定研究方向和关键词
        ↓
2. 用 search_literature.py 搜索相关文献
        ↓
3. 筛选 ~30 条最相关的文献
   - 高引经典 + 近年前沿 + 自己的工作
        ↓
4. 收集所有 DOI，写入 refs.txt
        ↓
5. 用 generate_references.py 生成标准引用
        ↓
6. 检查格式统一性
        ↓
7. 确认没有遗漏关键文献
```

---

## 常见问题

### 搜索不到文献？
- 尝试不同的关键词组合
- 使用英文关键词
- 检查拼写
- OpenAlex覆盖面广但不是100%，可辅以Google Scholar

### wenxian报错？
- 确认设置了代理：`export https_proxy=http://localhost:7890`
- 确认DOI格式正确（如 `10.1038/s41586-020-2242-8`）
- PubMed API需要代理才能访问

### 格式不统一？
- 使用同一工具生成所有引用
- 手动检查并统一姓名顺序、期刊缩写
- 建议最后统一校对一遍
