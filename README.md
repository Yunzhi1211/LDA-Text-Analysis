[English](README.md) | [简体中文](README_zh.md)

# LDA Topic Analysis

> Automated Latent Dirichlet Allocation (LDA) Topic Mining System for Enterprise Survey Data

## 📋 Project Overview

This project performs **LDA topic analysis** on large-scale survey questionnaire text data to automatically discover hidden topics. It features complete reproducibility, easy scalability, and privacy protection.

### ✨ Key Features

- ✅ **Fully Automated** - End-to-end automation from DOCX extraction to result visualization
- ✅ **Completely Reproducible** - Fixed random seed ensures consistent results
- ✅ **Easily Scalable** - Others can rerun with their own data
- ✅ **Privacy Protected** - Raw data not uploaded to GitHub, only anonymized results published
- ✅ **Multiple Visualizations** - Word distribution, topic chart, heatmap, word cloud, interactive HTML
- ✅ **Flexible Configuration** - All parameters customizable

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies (First Time)

```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

### 2️⃣ Prepare Data

Place DOCX files in the `1_input/` folder:

```
1_input/
├── file1.docx
├── file2.docx
└── ...
```

### 3️⃣ Run Analysis

```bash
python main.py
```

### 4️⃣ View Results

```
2_output/
├── lda_results.json              # LDA analysis results
├── lda_model/                    # Trained model
└── visualizations/               # All charts and HTML
    ├── top_words_per_topic.png
    ├── topic_distribution.png
    ├── topic_heatmap.png
    └── lda_interactive.html      # Open this file to view visualization
```

### 💻 View Online Interactive Visualization

**[Click here to view the LDA interactive visualization online](https://yunzhi1211.github.io/LDA-Text-Analysis/lda_results.html)**

The interactive HTML hosted on GitHub Pages allows you to:
- 🔍 Explore topics interactively
- 📊 View term-topic relationships
- 🎯 Click on topics to see relevant terms

---

## 📁 Project Structure

```
.
├── 0_config/
│   ├── config.yaml                # ⚙️ Configuration file (customizable)
│   └── requirements.txt           # 📦 Dependencies
├── 1_input/                       # 📥 Input data (Git ignored)
├── 2_output/                      # 📤 Output results
│   ├── lda_results.json
│   ├── lda_model/
│   └── visualizations/
├── 3_log/                         # 📝 Run logs (auto-generated per run)
├── 4_scripts/                     # 🔧 Processing scripts
│   ├── 0_text_extraction.py       # Text extraction
│   ├── 1_preprocessing.py         # Data preprocessing
│   ├── 2_lda_model.py            # LDA modeling
│   └── 3_visualization.py         # Visualization
├── main.py                        # Main program
├── run.bat                        # Windows launcher
├── run.sh                         # Linux/Mac launcher
├── .gitignore                     # Git configuration
└── README.md                      # This file
```

---

## ⚙️ Configuration

Edit `0_config/config.yaml` to adjust parameters:

### Core Parameters

```yaml
lda:
  num_topics: 5              # 👈 Number of topics (adjust based on data)
  passes: 10                 # Training passes (more = more accurate but slower)
  iterations: 100            # Iterations per pass
  random_state: 42           # Random seed (ensures reproducibility)
```

### Preprocessing Parameters

```yaml
preprocessing:
  min_word_length: 2         # Minimum word length
  max_df: 0.85               # Maximum document frequency (filter common words)
  min_df: 2                  # Minimum occurrence frequency (filter rare words)
```

### Tuning Recommendations

| Situation | Adjustment |
|-----------|------------|
| Topics too similar | Decrease `num_topics` |
| Topics too dispersed | Increase `num_topics` |
| Running too slow | Decrease `passes` or `iterations` |
| Out of memory | Increase `min_df` or decrease `max_df` |

---

## 📊 Output Files

### `lda_results.json` - Core Results

```json
{
  "model_config": {
    "num_topics": 5,
    "coherence_score": 0.5847
  },
  "topics": {
    "0": {
      "words": [
        {"word": "breeding", "weight": 0.0452},
        {"word": "chicken", "weight": 0.0389},
        ...
      ]
    },
    ...
  }
}
```

Higher weight indicates stronger representation of the word in that topic.

### Visualization Results

| File | Description |
|------|-------------|
| `top_words_per_topic.png` | Word distribution per topic (bar chart) |
| `topic_distribution.png` | Document distribution across topics |
| `topic_heatmap.png` | Document-topic relationship heatmap |
| `lda_interactive.html` | 🌐 Interactive visualization (recommended) |

---

## 🔐 Data Privacy

### Key Points

- **1_input folder** - Contains raw questionnaires, automatically excluded by `.gitignore`, not uploaded to GitHub
- **2_output folder** - LDA results anonymized, safe to upload
- **lda_results.json** - Contains only aggregated statistics (topic-word distribution), cannot be traced back to original documents

### Anonymization Process

1. Save only topic-word distribution (aggregated data)
2. Remove personal/company identifiers
3. Do not save document-topic mapping

---

## 🔧 Workflow

```
1_input/ (DOCX files)
  ↓ [4_scripts/0_text_extraction.py]
Text extraction
  ↓ [4_scripts/1_preprocessing.py]
Tokenization, cleaning, filtering
  ↓ [4_scripts/2_lda_model.py]
LDA model training
  ↓ [4_scripts/3_visualization.py]
Results visualization
  ↓
2_output/ ← View results
3_log/   ← View logs
```

---

## 🛠️ FAQ

### Q1: Error "UnicodeDecodeError"

**Solution**: Check DOCX file encoding, ensure it's UTF-8 format

### Q2: Poor jieba tokenization

**Solution**: Add custom vocabulary in 4_scripts/1_preprocessing.py:

```python
import jieba
jieba.load_userdict('my_dict.txt')  # Custom vocabulary
```

### Q3: Too many/few topics

**Solution**: Adjust `num_topics` in `0_config/config.yaml`

### Q4: Slow execution

**Solution**: Reduce `passes` and `iterations` parameters

### Q5: Out of memory

**Solution**: Increase `min_df` or decrease `max_df` to reduce vocabulary size

---

## 💡 Usage Examples

### Basic Usage

```bash
# 1. Prepare data: Place DOCX files in 1_input/
# 2. Run analysis
python main.py
# 3. Open 2_output/visualizations/lda_interactive.html to view results
```

### Compare with Different Parameters

```yaml
# 0_config/config.yaml
lda:
  num_topics: 3    # First run: 3 topics
  # num_topics: 5  # Second run: 5 topics
  # num_topics: 8  # Third run: 8 topics
```

Then run `python main.py` multiple times to compare results.

---


```

### Files to Include on GitHub

✅ `src/` - All code  
✅ `0_config/` - Configuration template  
✅ `2_output/lda_results.json` - Anonymized results  
✅ `2_output/visualizations/` - Charts  
✅ README.md, requirements.txt  

❌ `1_input/` - Raw data (privacy)  
❌ `lda_analysis.log` - Runtime log  

---

## 📄 License

MIT License - Free to use, modify, and distribute code and anonymized results

---

## 👥 Contributors

### Core Team

This project was developed as part of the **Rural Revitalization Research Initiative**. Key contributions:

| Role | Contributors |
|:---|:---|
| **LDA Topic Analysis** (Lead Contributor) | **Han Junyi** 🌟 |
| Data Analysis & Research | Han Junyi, Hao Jiarui, Yue Wenjie, Wu Yinuo |
| Investigation & Interviews | Jiang Yunzhi, Zhang Wenying, Liu Qinyan, Zhang Pingping, Li Xiayi, Li Hanjie, Xia Ying |
| Publicity & Support | Jiang Mengyu, Cao Yuting, Tan Tingting, Li Yuexing, Deng Yunran |


### Acknowledgements

- **Advisors**: Mao Shanjun, Cao Zhongyu
- To all survey participants, liaisons, coordinators, and contributing enterprises.
- **Special Acknowledgement**: **Han Junyi*** led the LDA topic modeling analysis, providing critical theoretical support and in-depth insights into the topic patterns within the enterprise survey data.

---

**Survey Period**: July 2023  
**Report Completion**: September 2023  
**Last Updated**: April 2026  
**Version**: 1.0.0 

---
