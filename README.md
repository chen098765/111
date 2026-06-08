# 实训报告自动批改系统

## 项目简介

本系统用于自动批改学生提交的实训报告，通过与教师提供的参考答案进行比对，自动评分并生成详细的批改报告。

## 功能特性

- 📄 支持 .docx 和 .pdf 格式的报告读取
- 🔍 智能比对报告内容（文字和图片）
- 📊 多维度自动评分（结构完整性、准确性、匹配度等）
- 💬 自动生成个性化评语和改进建议
- 📑 支持 JSON 和 HTML 格式的批改报告输出
- 📁 支持批量处理多个报告
- 🌐 提供 Streamlit Web 界面

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 目录结构

```
report_grader/
├── config/
│   └── scoring_rules.json    # 评分规则配置文件
├── modules/
│   ├── document_reader.py    # 文档读取模块
│   ├── comparator.py         # 内容比对模块
│   ├── scorer.py             # 评分模块
│   └── report_generator.py   # 报告生成模块
├── output/                   # 输出目录
├── templates/                # 模板目录
├── main.py                   # 命令行入口
├── app.py                    # Web 界面入口
└── requirements.txt          # 依赖列表
```

## 使用方法

### 命令行模式

#### 单文件批改
```bash
python main.py --reference reference.docx --student student.docx --format html
```

#### 批量批改
```bash
python main.py --reference reference.docx --folder ./reports/ --format html
```

### Web 界面模式

```bash
streamlit run app.py
```

然后在浏览器中访问显示的地址（通常是 http://localhost:8501）。

## 评分规则

系统从以下六个维度进行评分，总分100分：

| 维度 | 分值 | 说明 |
|------|------|------|
| 结构完整性 | 10分 | 章节是否完整 |
| 关键步骤准确性 | 30分 | 步骤和代码描述准确性 |
| 结果匹配度 | 25分 | 与参考答案的整体匹配程度 |
| 问题分析深度 | 20分 | 反思和分析内容质量 |
| 图片质量 | 10分 | 图片数量和质量 |
| 格式规范 | 5分 | 格式是否规范 |

### 配置评分规则

编辑 `config/scoring_rules.json` 文件可以调整各维度的权重：

```json
{
    "weights": {
        "structure": 10,
        "accuracy": 30,
        "matching": 25,
        "analysis": 20,
        "images": 10,
        "format": 5
    },
    "image_threshold": 0.8,
    "similarity_threshold": 0.6
}
```

## 输出格式

### JSON 格式
包含完整的评分数据和比对结果，便于程序化处理。

### HTML 格式
可视化的批改报告，包含评分条、章节比对、评语等。

## 注意事项

1. 系统支持离线运行，无需网络连接
2. PDF 文件的图片提取功能有限，建议使用 docx 格式以获得更好的图片分析效果
3. 首次运行时会自动下载 NLTK 相关数据

## 技术栈

- Python 3.8+
- python-docx (docx 文件处理)
- PyPDF2 (PDF 文件处理)
- scikit-learn (文本相似度计算)
- nltk (自然语言处理)
- streamlit (Web 界面)

## 许可证

MIT License