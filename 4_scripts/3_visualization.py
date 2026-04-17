"""
LDA主题分析 - 可视化模块
生成LDA分析结果的各种图表（美观版）
"""

import logging
from pathlib import Path
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

try:
    import pyLDAvis
    import pyLDAvis.gensim_models as gensimvis
except ImportError:
    pyLDAvis = None
    gensimvis = None

logger = logging.getLogger(__name__)
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def generate_topic_names(lda_model, num_topics: int) -> Dict[int, str]:
    """根据每个主题的前几个关键词自动生成主题名称"""
    topic_names = {}
    for topic_id in range(num_topics):
        terms = lda_model.show_topic(topic_id, topn=3)
        keywords = [t[0] for t in terms]
        topic_names[topic_id] = f"主题{topic_id}: {'/'.join(keywords)}"
    return topic_names


class LDAVisualizer:
    """LDA结果可视化类"""
    
    def __init__(self, output_dir: str = "2_output/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.topic_names = {}
        logger.info(f"可视化输出目录: {self.output_dir}")
    
    def set_topic_names(self, lda_model, num_topics: int):
        self.topic_names = generate_topic_names(lda_model, num_topics)
    
    def plot_top_words(self, lda_model, num_words: int = 10, figsize: tuple = (16, 10)):
        """绘制每个主题的顶部词汇（美化版）"""
        logger.info("绘制主题词汇图表...")
        
        num_topics = lda_model.num_topics
        num_cols = min(num_topics, 3)
        num_rows = (num_topics + num_cols - 1) // num_cols
        
        color_palettes = [
            '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
            '#1ABC9C', '#E67E22', '#34495E', '#16A085', '#C0392B'
        ]
        
        fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
        fig.suptitle('LDA主题分析 - 各主题关键词及权重', fontsize=18, fontweight='bold', y=1.02)
        
        if num_rows == 1 and num_cols == 1:
            axes = np.array([axes])
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
        
        for topic_id in range(num_topics):
            ax = axes[topic_id]
            terms = lda_model.show_topic(topic_id, topn=num_words)
            words = [t[0] for t in terms][::-1]
            weights = [t[1] for t in terms][::-1]
            
            base_color = color_palettes[topic_id % len(color_palettes)]
            bars = ax.barh(words, weights, color=base_color, alpha=0.85,
                          edgecolor='white', linewidth=0.5, height=0.7)
            
            for bar, w in zip(bars, weights):
                ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                       f'{w:.3f}', va='center', fontsize=8, color='#555')
            
            topic_name = self.topic_names.get(topic_id, f'主题 {topic_id}')
            ax.set_title(topic_name, fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel('权重', fontsize=9)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='y', labelsize=10)
            ax.tick_params(axis='x', labelsize=8)
        
        for i in range(num_topics, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        output_path = self.output_dir / "top_words_per_topic.png"
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        logger.info(f"保存: {output_path}")
        plt.close()
    
    def plot_topic_distribution(self, doc_topics: List[List[Tuple[int, float]]],
                                 figsize: tuple = (14, 6)):
        """绘制文档主题分布（美化版，柱状图+饼图）"""
        logger.info("绘制主题分布直方图...")
        
        dominant_topics = []
        for doc in doc_topics:
            if doc:
                best = max(doc, key=lambda x: x[1])
                dominant_topics.append(best[0])
        
        topic_ids = sorted(set(dominant_topics))
        counts = [dominant_topics.count(t) for t in topic_ids]
        
        color_palettes = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
                          '#1ABC9C', '#E67E22', '#34495E', '#16A085', '#C0392B']
        colors = [color_palettes[t % len(color_palettes)] for t in topic_ids]
        labels = [self.topic_names.get(t, f'主题{t}') for t in topic_ids]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle('文档主题分布概览', fontsize=16, fontweight='bold')
        
        # 柱状图
        bars = ax1.bar(range(len(topic_ids)), counts, color=colors, alpha=0.85,
                       edgecolor='white', linewidth=1.5, width=0.6)
        ax1.set_xticks(range(len(topic_ids)))
        ax1.set_xticklabels(labels, rotation=20, ha='right', fontsize=9)
        ax1.set_ylabel('文档数量', fontsize=11)
        ax1.set_title('各主题文档数量', fontsize=13, fontweight='bold')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(count), ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 饼图
        wedges, texts, autotexts = ax2.pie(
            counts, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, pctdistance=0.75, textprops={'fontsize': 9}
        )
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        ax2.set_title('主题占比', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.output_dir / "topic_distribution.png"
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        logger.info(f"保存: {output_path}")
        plt.close()
    
    def plot_topic_heatmap(self, lda_model, doc_topics: List[List[Tuple[int, float]]],
                           doc_names: List[str] = None, figsize: tuple = (14, 12)):
        """绘制文档-主题热力图（美化版，带数值标注和文档名）"""
        logger.info("绘制文档-主题热力图...")
        
        num_topics = lda_model.num_topics
        num_docs = min(len(doc_topics), 35)
        
        matrix = np.zeros((num_docs, num_topics))
        for doc_id in range(num_docs):
            for topic_id, weight in doc_topics[doc_id]:
                matrix[doc_id, int(topic_id)] = weight
        
        fig, ax = plt.subplots(figsize=figsize)
        
        im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', interpolation='nearest',
                       vmin=0, vmax=1)
        
        # 标注数值
        for i in range(num_docs):
            for j in range(num_topics):
                val = matrix[i, j]
                if val > 0.01:
                    text_color = 'white' if val > 0.5 else 'black'
                    ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                           fontsize=7, color=text_color, fontweight='bold')
        
        topic_labels = [self.topic_names.get(i, f'T{i}') for i in range(num_topics)]
        ax.set_xticks(range(num_topics))
        ax.set_xticklabels(topic_labels, rotation=30, ha='right', fontsize=9)
        
        if doc_names:
            ax.set_yticks(range(num_docs))
            ax.set_yticklabels([f'Doc {i+1}' for i in range(num_docs)], fontsize=7)
        else:
            ax.set_yticks(range(num_docs))
            ax.set_yticklabels([f'Doc {i+1}' for i in range(num_docs)], fontsize=7)
        
        ax.set_title('文档-主题权重热力图', fontsize=16, fontweight='bold', pad=15)
        
        cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label('主题权重', fontsize=11)
        
        plt.tight_layout()
        output_path = self.output_dir / "topic_heatmap.png"
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        logger.info(f"保存: {output_path}")
        plt.close()
    
    def generate_interactive_html(self, lda_model, dictionary, corpus, output_file: str = None):
        """生成交互式HTML可视化"""
        if gensimvis is None or pyLDAvis is None:
            logger.warning("pyLDAvis未安装，跳过交互式可视化")
            return
        
        logger.info("生成交互式HTML可视化...")
        try:
            vis = gensimvis.prepare(lda_model, corpus, dictionary, mds='mmds')
            if output_file is None:
                output_file = str(self.output_dir / "lda_interactive.html")
            pyLDAvis.save_html(vis, str(output_file))
            logger.info(f"保存交互式可视化: {output_file}")
        except AttributeError:
            # pyLDAvis版本兼容：尝试旧版API
            try:
                from pyLDAvis import save_html
                save_html(vis, str(output_file))
                logger.info(f"保存交互式可视化: {output_file}")
            except Exception as e2:
                logger.error(f"生成交互式可视化失败: {e2}", exc_info=True)
        except Exception as e:
            logger.error(f"生成交互式可视化失败: {e}", exc_info=True)


def visualize_results(lda_model, dictionary, corpus, doc_topics,
                     doc_names: list = None,
                     coherence_score: float = None, output_dir: str = "2_output/visualizations"):
    """便捷函数：一键生成所有可视化"""
    visualizer = LDAVisualizer(output_dir)
    visualizer.set_topic_names(lda_model, lda_model.num_topics)
    visualizer.plot_top_words(lda_model)
    visualizer.plot_topic_distribution(doc_topics)
    visualizer.plot_topic_heatmap(lda_model, doc_topics, doc_names=doc_names)
    visualizer.generate_interactive_html(lda_model, dictionary, corpus)
    logger.info("所有可视化生成完成")
