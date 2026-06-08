# AI 使用日志

## 记录说明

本文件记录了开发实训报告自动批改系统过程中，向 Trae AI 助手提问的关键问答记录。

---

## 问答记录

### 1. 如何读取 docx 和 pdf 文件并提取文本和图片？

**提问内容：**
我需要开发一个实训报告批改系统，需要读取 docx 和 pdf 格式的文件，提取文本内容和图片信息。请提供 Python 代码示例。

**生成的代码片段：**
```python
import docx
from docx import Document
from PyPDF2 import PdfReader

def read_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    return text

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = '\n'.join([page.extract_text() for page in reader.pages])
    return text
```

**理解与修改过程：**
基础代码实现了文本读取，但缺少图片处理功能。我需要扩展代码以提取 docx 中的图片信息（数量、尺寸、格式），并完善返回的数据结构。最终实现了 `DocumentReader` 类，支持文本和图片信息的提取。

---

### 2. 如何计算两段中文文本的相似度？

**提问内容：**
如何使用 Python 计算两段中文文本的相似度？需要考虑停用词处理和 TF-IDF 向量化。

**生成的代码片段：**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('chinese'))

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
```

**理解与修改过程：**
代码提供了基本的相似度计算方法。我需要添加文本预处理步骤（分词、去除标点），并处理空文本等边界情况。同时需要确保 NLTK 数据的自动下载。

---

### 3. 如何实现报告章节的自动识别？

**提问内容：**
如何从实训报告中自动识别常见章节（如实训目的、实训步骤、实验结果等）？

**生成的代码片段：**
```python
def extract_chapters(text):
    chapters = {}
    chapter_keywords = {
        '实训目的': ['实训目的', '实验目的', '目的'],
        '实训步骤': ['实训步骤', '实验步骤', '步骤'],
        '实验结果': ['实验结果', '结果', '数据分析'],
        '问题反思': ['问题反思', '反思', '问题分析'],
        '心得体会': ['心得体会', '总结', '体会']
    }
    
    lines = text.split('\n')
    current_chapter = None
    current_content = []
    
    for line in lines:
        for chapter_name, keywords in chapter_keywords.items():
            if any(keyword in line for keyword in keywords):
                if current_chapter:
                    chapters[current_chapter] = '\n'.join(current_content)
                current_chapter = chapter_name
                current_content = [line]
                break
        else:
            if current_chapter:
                current_content.append(line)
    
    if current_chapter:
        chapters[current_chapter] = '\n'.join(current_content)
    
    return chapters
```

**理解与修改过程：**
代码实现了基本的章节识别功能。我需要优化关键词匹配逻辑，增加更多关键词，并且处理章节标题的特殊情况（如标题行较短）。同时需要记录哪些章节存在或缺失，用于后续评分。

---

### 4. 如何设计评分系统和权重配置？

**提问内容：**
请设计一个多维度评分系统，支持权重配置，包含结构完整性、准确性、匹配度等维度。

**生成的代码片段：**
```python
class ReportScorer:
    def __init__(self, weights=None):
        self.weights = weights or {
            'structure': 10,
            'accuracy': 30,
            'matching': 25,
            'analysis': 20,
            'images': 10,
            'format': 5
        }
    
    def score(self, comparison_result):
        scores = {}
        scores['structure'] = self._score_structure(comparison_result)
        scores['accuracy'] = self._score_accuracy(comparison_result)
        scores['matching'] = self._score_matching(comparison_result)
        scores['analysis'] = self._score_analysis(comparison_result)
        scores['images'] = self._score_images(comparison_result)
        scores['format'] = self._score_format(comparison_result)
        
        total = sum(scores[k] * (self.weights[k]/100) for k in scores)
        return {'scores': scores, 'total': total}
```

**理解与修改过程：**
代码提供了评分系统的框架。我需要实现每个维度的具体评分逻辑，支持从 JSON 配置文件加载权重，并添加个性化评语生成功能。

---

### 5. 如何生成 HTML 格式的报告？

**提问内容：**
如何生成美观的 HTML 格式批改报告，包含评分条、章节比对结果和评语？

**生成的代码片段：**
```python
def generate_html_report(data):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>批改报告</title>
        <style>
            .score-bar {{ background: #eee; height: 30px; border-radius: 15px; }}
            .score-fill {{ height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); }}
        </style>
    </head>
    <body>
        <h1>实训报告批改结果</h1>
        <div class="score-bar">
            <div class="score-fill" style="width: {data['total']}%"></div>
        </div>
        <p>总分: {data['total']}/100</p>
        <div>{data['feedback']}</div>
    </body>
    </html>
    """
    return html
```

**理解与修改过程：**
代码提供了基本的 HTML 模板。我需要扩展模板，添加分项得分表格、章节比对详情、图片统计等内容，并优化样式设计。同时需要支持 JSON 和 HTML 两种输出格式。

---

## 总结

通过与 Trae AI 的5次关键问答，我成功实现了：

1. **文档读取模块**：支持 docx 和 pdf 格式的文本和图片提取
2. **内容比对模块**：使用 TF-IDF 和余弦相似度进行文本比对
3. **章节识别功能**：自动识别实训报告的常见章节结构
4. **评分系统**：多维度评分，支持权重配置
5. **报告生成**：支持 JSON 和 HTML 两种输出格式

在实现过程中，我根据实际需求对 AI 生成的代码进行了扩展和优化，确保系统功能完整、稳定可靠。