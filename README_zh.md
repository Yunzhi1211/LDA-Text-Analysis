[English](README.md) | [简体中文](README_zh.md)

# LDA 主题分析项目

> 基于企业调查问卷的潜在狄利克雷分配(LDA)自动主题挖掘系统

## 📋 项目概述

本项目对大量调查问卷文本数据进行**LDA主题分析**，自动发现隐藏的主题。具有完全可复现、易于推广、隐私保护等特点。

### ✨ 核心特性

- ✅ **完全自动化** - 从DOCX提取到结果可视化全自动
- ✅ **可完全复现** - 固定随机种子确保结果一致性
- ✅ **易于推广** - 他人可用自己的数据重新运行
- ✅ **隐私保护** - 原始数据不上传GitHub，只发布脱敏结果
- ✅ **多种可视化** - 词汇分布、主题图、热力图、词云、交互式HTML
- ✅ **灵活配置** - 所有参数可自定义

---

## 🚀 快速开始

### 1️⃣ 安装依赖（首次）

```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

### 2️⃣ 准备数据

将DOCX文件放入 `1_input/` 文件夹：

```
1_input/
├── file1.docx
├── file2.docx
└── ...
```

### 3️⃣ 运行分析

```bash
python main.py
```

### 4️⃣ 查看结果

```
2_output/
├── lda_results.json              # LDA分析结果
├── lda_model/                    # 训练的模型
└── visualizations/               # 所有图表和HTML
    ├── top_words_per_topic.png
    ├── topic_distribution.png
    ├── topic_heatmap.png
    └── lda_interactive.html      # 打开此文件查看可视化
```

### 💻 在线查看交互式可视化

**[点击这里在线查看 LDA 交互式可视化](https://yunzhi1211.github.io/LDA-Text-Analysis/lda_results.html)**

通过 GitHub Pages 托管的交互式HTML可以让您：
- 🔍 交互式浏览主题
- 📊 查看词汇-主题关系
- 🎯 点击主题查看相关词汇

---

## 📁 项目结构

```
.
├── 0_config/
│   ├── config.yaml                # ⚙️ 配置文件（可自定义）
│   └── requirements.txt           # 📦 依赖包
├── 1_input/                       # 📥 输入数据（Git忽略）
├── 2_output/                      # 📤 输出结果
│   ├── lda_results.json
│   ├── lda_model/
│   └── visualizations/
├── 3_log/                         # 📝 运行日志（每次运行自动生成）
├── 4_scripts/                     # 🔧 运行脚本
│   ├── 0_text_extraction.py       # 文本提取
│   ├── 1_preprocessing.py         # 数据预处理
│   ├── 2_lda_model.py            # LDA建模
│   └── 3_visualization.py         # 可视化
├── main.py                        # 主程序
├── run.bat                        # Windows启动
├── run.sh                         # Linux/Mac启动
├── .gitignore                     # Git配置
└── README.md                      # 本文件
```

---

## ⚙️ 配置说明

编辑 `0_config/config.yaml` 调整参数：

### 核心参数

```yaml
lda:
  num_topics: 5              # 👈 主题数量（根据数据调整）
  passes: 10                 # 训练轮数（更多=更精确但更慢）
  iterations: 100            # 每轮迭代次数
  random_state: 42           # 随机种子（确保可复现）
```

### 预处理参数

```yaml
preprocessing:
  min_word_length: 2         # 词语最少字数
  max_df: 0.85               # 词出现的最大文档比例（过滤常见词）
  min_df: 2                  # 词最少出现次数（过滤罕见词）
```

### 参数调优建议

| 情况 | 调整 |
|------|------|
| 主题过于相似 | 减少 `num_topics` |
| 主题太分散 | 增加 `num_topics` |
| 运行太慢 | 减少 `passes` 或 `iterations` |
| 内存溢出 | 增加 `min_df` 或减少 `max_df` |

---

## 📊 输出文件详解

### `lda_results.json` - 核心结果

```json
{
  "model_config": {
    "num_topics": 5,
    "coherence_score": 0.5847
  },
  "topics": {
    "0": {
      "words": [
        {"word": "养殖", "weight": 0.0452},
        {"word": "鸡", "weight": 0.0389},
        ...
      ]
    },
    ...
  }
}
```

权重越高，该词对主题的代表性越强。

### 可视化结果

| 文件 | 说明 |
|------|------|
| `top_words_per_topic.png` | 每个主题的词汇分布（条形图） |
| `topic_distribution.png` | 各主题的文档数分布 |
| `topic_heatmap.png` | 文档-主题关系热力图 |
| `lda_interactive.html` | 🌐 交互式可视化（推荐打开） |

---

## 🔐 数据隐私

### 关键说明

- **1_input文件夹** - 包含原始问卷，`.gitignore` 自动排除，不上传GitHub
- **2_output文件夹** - LDA结果已脱敏处理，可安全上传
- **lda_results.json** - 只含聚合统计（主题-词汇分布），无法反向追踪原始文档

### 脱敏处理

1. 只保存主题-词汇分布（聚合数据）
2. 移除个人/公司标识词
3. 不保存文档-主题映射

---

## 🔧 工作流程

```
1_input/ (DOCX文件)
  ↓ [4_scripts/0_text_extraction.py]
文本提取
  ↓ [4_scripts/1_preprocessing.py]
分词、清洗、过滤
  ↓ [4_scripts/2_lda_model.py]
LDA模型训练
  ↓ [4_scripts/3_visualization.py]
结果可视化
  ↓
2_output/ ← 查看结果
3_log/   ← 查看日志
```

---

## 🛠️ 常见问题排查

| 问题 | 解决方案 |
|------|-------|
| 运行时出现 `UnicodeDecodeError` | 确保DOCX文件采用UTF-8编码 |
| jieba分词效果不理想 | 在 `4_scripts/1_preprocessing.py` 中添加自定义词汇表 |
| 主题太相似或太分散 | 调整 `0_config/config.yaml` 中的 `num_topics` |
| 运行速度慢 | 减少 `passes` 和 `iterations` 参数 |
| 出现内存不足错误 | 增加 `min_df` 或减少 `max_df` 来减少词汇量 |
| HTML可视化显示不正常 | 清除浏览器缓存后刷新页面 |

---

## 💡 使用示例

### 基础使用

```bash
# 1. 准备数据：将DOCX放入1_input/
# 2. 运行分析
python main.py
# 3. 打开2_output/visualizations/lda_interactive.html查看结果
```

### 调整参数进行对比

```yaml
# 0_config/config.yaml
lda:
  num_topics: 3    # 第一次：3个主题
  # num_topics: 5  # 第二次：5个主题
  # num_topics: 8  # 第三次：8个主题
```

然后多次运行 `python main.py` 对比结果。

---

## 📦 项目文件说明

**上传到GitHub** ✅
- `4_scripts/` - 所有处理脚本
- `0_config/` - 配置模板
- `2_output/lda_results.json` - 脱敏分析结果
- `2_output/visualizations/` - 可视化图表
- `docs/` - GitHub Pages文件
- README文档、requirements.txt

**被.gitignore排除** ❌  
- `1_input/` - 原始DOCX问卷数据（隐私保护）
- `3_log/` - 运行日志（自动生成）
- `__pycache__/` - Python缓存文件

---

## 📄 许可证

MIT License - 自由使用、修改、分发代码和脱敏结果

---

## 🙏  致谢与贡献

本项目作为**乡村振兴调研计划**的一部分而开发。

**项目开发**:
- 韩君怡（主导 - LDA主题分析） 🌟

**数据分析与研究**:
- 韩君怡、郝佳锐、岳文杰、吴依诺

**调查采访与研究**:
- 江昀芷、张文莹、刘秦艳、章萍萍、黎夏怡、李函洁、夏颖

**项目指导**:
- 毛善骏、曹中玉

---

## 📚 版本信息

- **⏰ 最后更新**: 2026年4月
- **🔄 当前版本**: 1.0.0
- 所有调查参与、联络、协调和企业贡献者
- **特别致谢**：韩君怡主导了LDA主题建模分析，为企业调查数据中的主题模式提供了重要的理论支撑和深入见解。

---

**调查时间**：2023年7月
**报告产出**：2023年9月
**最后更新**: 2026年4月  
**版本**: 1.0.0  

