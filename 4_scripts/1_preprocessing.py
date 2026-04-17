"""
LDA主题分析 - 数据预处理模块
分词、清洗、去停用词等
"""

import jieba
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


# 内置停用词表（中文常见停用词）
DEFAULT_STOPWORDS = {
    '的', '一', '是', '在', '不', '了', '有', '和', '人', '这',
    '中', '大', '为', '上', '个', '国', '我', '以', '要', '他',
    '时', '来', '用', '们', '生', '到', '作', '地', '于', '出',
    '就', '分', '对', '成', '会', '可', '主', '发', '年', '动',
    '同', '工', '也', '能', '下', '过', '民', '前', '面', '所',
    '多', '经', '起', '模', '每', '而', '已', '进', '着', '日',
    '被', '本', '后', '里', '最', '现', '文', '次', '开', '没',
    '还', '机', '全', '其', '第', '一', '着', '向', '着', '好',
    '看', '得', '那', '种', '此', '道', '则', '何', '方', '都',
    '等', '等等', '、', '。', '，', '；', '：', '？', '！',
    '（', '）', '『', '』', '「', '」', '《', '》', ''', ''',
    '"', '"', '·', '…', '—', '～', '·', 'nbsp',
}


class ChinesePreprocessor:
    """中文文本预处理类"""
    
    def __init__(self, min_word_length: int = 2, max_df: float = 0.85,
                 min_df: int = 2, stopwords: set = None):
        self.min_word_length = min_word_length
        self.max_df = max_df
        self.min_df = min_df
        self.stopwords = stopwords or DEFAULT_STOPWORDS
        self.word_freq = {}
        self.total_docs = 0
        self.doc_freq = {}
    
    def tokenize(self, text: str) -> List[str]:
        words = jieba.cut(text)
        return list(words)
    
    def clean_token(self, token: str) -> bool:
        if len(token) < self.min_word_length:
            return False
        if token in self.stopwords:
            return False
        if token.isdigit() or token.isspace():
            return False
        return True
    
    def preprocess_text(self, text: str) -> List[str]:
        tokens = self.tokenize(text)
        cleaned = [t for t in tokens if self.clean_token(t)]
        return cleaned
    
    def preprocess_documents(self, documents: Dict[str, str]) -> List[List[str]]:
        processed_docs = []
        self.total_docs = len(documents)
        
        logger.info(f"开始预处理 {self.total_docs} 个文档...")
        
        for idx, (filename, text) in enumerate(documents.items(), 1):
            cleaned_words = self.preprocess_text(text)
            processed_docs.append(cleaned_words)
            
            unique_words = set(cleaned_words)
            for word in unique_words:
                self.doc_freq[word] = self.doc_freq.get(word, 0) + 1
            
            logger.info(f"[{idx}/{self.total_docs}] 处理完成: {filename}")
        
        return processed_docs
    
    def filter_by_frequency(self, documents: List[List[str]]) -> List[List[str]]:
        logger.info("根据文档频率进行过滤...")
        
        max_threshold = int(self.max_df * self.total_docs)
        
        filtered_docs = []
        for doc_words in documents:
            filtered = [
                w for w in doc_words
                if self.min_df <= self.doc_freq.get(w, 0) <= max_threshold
            ]
            filtered_docs.append(filtered)
        
        logger.info(f"过滤完成")
        return filtered_docs


def preprocess_documents(raw_texts: Dict[str, str], config: dict) -> List[List[str]]:
    preprocessor = ChinesePreprocessor(
        min_word_length=config.get('min_word_length', 2),
        max_df=config.get('max_df', 0.85),
        min_df=config.get('min_df', 2)
    )
    
    processed = preprocessor.preprocess_documents(raw_texts)
    filtered = preprocessor.filter_by_frequency(processed)
    
    return filtered
