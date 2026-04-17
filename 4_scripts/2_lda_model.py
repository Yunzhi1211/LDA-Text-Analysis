"""
LDA主题分析 - LDA模型模块
训练LDA模型并进行主题分析
"""

import os
import json
import logging
from typing import List, Dict, Tuple
from pathlib import Path
import pickle

from gensim import corpora, models
from gensim.models import CoherenceModel

logger = logging.getLogger(__name__)


class LDAAnalyzer:
    """LDA主题分析类"""
    
    def __init__(self, num_topics: int = 5, random_state: int = 42):
        self.num_topics = num_topics
        self.random_state = random_state
        self.dictionary = None
        self.corpus = None
        self.lda_model = None
        self.coherence_model = None
    
    def create_dictionary(self, documents: List[List[str]]) -> corpora.Dictionary:
        logger.info("正在构建词汇表...")
        self.dictionary = corpora.Dictionary(documents)
        logger.info(f"词汇表大小: {len(self.dictionary)} 个词")
        return self.dictionary
    
    def create_corpus(self, documents: List[List[str]]) -> List[List[Tuple]]:
        if self.dictionary is None:
            raise ValueError("请先调用 create_dictionary()")
        
        logger.info("正在构建BoW语料库...")
        self.corpus = [self.dictionary.doc2bow(doc) for doc in documents]
        logger.info(f"语料库大小: {len(self.corpus)} 个文档")
        return self.corpus
    
    def train_lda(self, documents: List[List[str]], config: dict) -> models.LdaModel:
        self.create_dictionary(documents)
        self.create_corpus(documents)
        
        passes = config.get('passes', 10)
        iterations = config.get('iterations', 100)
        per_word_topics = config.get('per_word_topics', True)
        alpha = config.get('alpha', 'auto')
        eta = config.get('eta', 'auto')
        
        logger.info(f"开始训练LDA模型...")
        logger.info(f"参数: num_topics={self.num_topics}, passes={passes}")
        
        # LdaMulticore不支持alpha='auto'，使用LdaModel
        self.lda_model = models.LdaModel(
            corpus=self.corpus,
            id2word=self.dictionary,
            num_topics=self.num_topics,
            random_state=self.random_state,
            passes=passes,
            iterations=iterations,
            per_word_topics=per_word_topics,
            alpha=alpha,
            eta=eta,
            minimum_probability=0.0
        )
        
        logger.info("LDA模型训练完成")
        return self.lda_model
    
    def calculate_coherence(self, documents: List[List[str]]) -> float:
        if self.lda_model is None:
            raise ValueError("请先训练模型")
        
        logger.info("计算一致性得分...")
        self.coherence_model = CoherenceModel(
            model=self.lda_model,
            texts=documents,
            dictionary=self.dictionary,
            coherence='c_v'
        )
        coherence_score = self.coherence_model.get_coherence()
        logger.info(f"一致性得分 (C_V): {coherence_score:.4f}")
        return coherence_score
    
    def get_topics(self, num_words: int = 10) -> Dict[int, List[Tuple[str, float]]]:
        if self.lda_model is None:
            raise ValueError("请先训练模型")
        
        topics = {}
        for topic_id in range(self.num_topics):
            terms = self.lda_model.show_topic(topic_id, topn=num_words)
            topics[topic_id] = terms
            logger.info(f"主题 {topic_id}: {', '.join([w for w, _ in terms])}")
        
        return topics
    
    def get_document_topics(self, documents: List[List[str]] = None) -> List[List[Tuple[int, float]]]:
        if self.lda_model is None:
            raise ValueError("请先训练模型")
        
        if documents is None:
            corpus = self.corpus
        else:
            corpus = [self.dictionary.doc2bow(doc) for doc in documents]
        
        doc_topics = []
        for bow in corpus:
            topics = self.lda_model.get_document_topics(bow)
            doc_topics.append(topics)
        
        return doc_topics
    
    def save_model(self, model_dir: str):
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"保存模型到 {model_dir}")
        self.lda_model.save(str(model_path / "lda_model"))
        if self.dictionary:
            self.dictionary.save(str(model_path / "dictionary"))
        if self.corpus:
            with open(model_path / "corpus.pkl", 'wb') as f:
                pickle.dump(self.corpus, f)
        logger.info("模型保存完成")
    
    def load_model(self, model_dir: str):
        model_path = Path(model_dir)
        logger.info(f"从 {model_dir} 加载模型...")
        self.lda_model = models.LdaModel.load(str(model_path / "lda_model"))
        self.dictionary = corpora.Dictionary.load(str(model_path / "dictionary"))
        logger.info("模型加载完成")
    
    def export_results(self, output_file: str, num_words: int = 10):
        if self.lda_model is None:
            logger.error("模型未训练，无法导出")
            return
        
        logger.info(f"导出结果到 {output_file}")
        
        results = {
            'model_config': {
                'num_topics': self.num_topics,
                'random_state': self.random_state,
                'coherence_score': self.coherence_model.get_coherence() if self.coherence_model else None
            },
            'topics': {}
        }
        
        for topic_id in range(self.num_topics):
            terms = self.lda_model.show_topic(topic_id, topn=num_words)
            results['topics'][str(topic_id)] = {
                'words': [{'word': word, 'weight': float(weight)} for word, weight in terms]
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info("结果导出完成")


def train_lda(documents: List[List[str]], config: dict) -> LDAAnalyzer:
    analyzer = LDAAnalyzer(
        num_topics=config.get('num_topics', 5),
        random_state=config.get('random_state', 42)
    )
    
    analyzer.train_lda(documents, config)
    analyzer.calculate_coherence(documents)
    analyzer.get_topics(num_words=config.get('num_top_words', 10))
    
    return analyzer
