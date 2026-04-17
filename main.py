"""
LDA主题分析 - 主程序
完整的流程：文本提取 -> 预处理 -> LDA训练 -> 可视化
"""

import os
import sys
import logging
from pathlib import Path
import pickle
import yaml
import importlib

# 导入自定义模块（使用importlib因为模块名以数字开头）
sys.path.insert(0, str(Path(__file__).parent))

# 动态导入数字前缀的模块
text_extraction = importlib.import_module('4_scripts.0_text_extraction')
preprocessing = importlib.import_module('4_scripts.1_preprocessing')
lda_model = importlib.import_module('4_scripts.2_lda_model')
visualization = importlib.import_module('4_scripts.3_visualization')

extract_texts = text_extraction.extract_texts
preprocess_documents = preprocessing.preprocess_documents
train_lda = lda_model.train_lda
visualize_results = visualization.visualize_results


# 配置日志（输出到3_log文件夹，每次运行覆盖上一次）
log_dir = Path(__file__).parent / '3_log'
log_dir.mkdir(parents=True, exist_ok=True)
log_filename = log_dir / 'lda_latest.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(log_filename), mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_file: str = "0_config/config.yaml") -> dict:
    """
    加载配置文件
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        配置字典
    """
    logger.info(f"加载配置文件: {config_file}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def create_directories(config: dict):
    """
    创建必要的输出目录
    
    Args:
        config: 配置字典
    """
    dirs = [
        config['paths']['output_dir'],
        config['paths']['model_dir'],
        config['paths']['viz_dir']
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"目录就绪: {dir_path}")


def main():
    """
    主程序入口
    """
    logger.info("=" * 60)
    logger.info("开始LDA主题分析")
    logger.info("=" * 60)
    
    try:
        # ========== 第1步：加载配置 ==========
        config = load_config()
        create_directories(config)
        
        # ========== 第2步：文本提取 ==========
        logger.info("\n[第1步] 正在提取文本...")
        input_dir = config['paths']['input_dir']
        
        if not Path(input_dir).exists():
            logger.error(f"输入目录不存在: {input_dir}")
            logger.error("请将DOCX文件放入input文件夹")
            return
        
        raw_texts = extract_texts(input_dir)
        logger.info(f"✓ 成功提取 {len(raw_texts)} 个文档")
        
        if not raw_texts:
            logger.error("未能提取任何文本，请检查input文件夹")
            return
        
        # ========== 第3步：数据预处理 ==========
        logger.info("\n[第2步] 正在预处理数据...")
        processed_docs = preprocess_documents(raw_texts, config['preprocessing'])
        logger.info(f"✓ 数据预处理完成")
        
        # 保存处理后的文本
        output_dir = config['paths']['output_dir']
        processed_file = Path(output_dir) / "processed_texts.pkl"
        with open(processed_file, 'wb') as f:
            pickle.dump(processed_docs, f)
        logger.info(f"✓ 已保存处理后的文本: {processed_file}")
        
        # ========== 第4步：训练LDA模型 ==========
        logger.info("\n[第3步] 正在训练LDA模型...")
        analyzer = train_lda(processed_docs, config['lda'])
        logger.info(f"✓ LDA模型训练完成")
        
        # ========== 第5步：获取分析结果 ==========
        logger.info("\n[第4步] 正在分析主题...")
        doc_topics = analyzer.get_document_topics()
        logger.info(f"✓ 主题分析完成")
        
        # ========== 第6步：保存模型 ==========
        logger.info("\n[第5步] 正在保存模型...")
        if config['output']['save_model']:
            analyzer.save_model(config['paths']['model_dir'])
            logger.info(f"✓ 模型已保存到: {config['paths']['model_dir']}")
        
        # ========== 第7步：导出结果 ==========
        logger.info("\n[第6步] 正在导出结果...")
        if config['output']['save_results_json']:
            results_file = Path(output_dir) / "lda_results.json"
            analyzer.export_results(str(results_file), num_words=config['visualization']['num_top_words'])
            logger.info(f"✓ 结果已导出到: {results_file}")
        
        # ========== 第8步：生成可视化 ==========
        logger.info("\n[第7步] 正在生成可视化...")
        if analyzer.coherence_model:
            coherence_score = analyzer.coherence_model.get_coherence()
        else:
            coherence_score = None
        
        doc_names = list(raw_texts.keys())
        visualize_results(
            lda_model=analyzer.lda_model,
            dictionary=analyzer.dictionary,
            corpus=analyzer.corpus,
            doc_topics=doc_topics,
            doc_names=doc_names,
            coherence_score=coherence_score,
            output_dir=config['paths']['viz_dir']
        )
        logger.info(f"✓ 可视化已保存到: {config['paths']['viz_dir']}")
        
        # ========== 完成 ==========
        logger.info("\n" + "=" * 60)
        logger.info("✓ LDA分析完全完成！")
        logger.info("=" * 60)
        logger.info("输出文件:")
        logger.info(f"  - 模型: {config['paths']['model_dir']}")
        logger.info(f"  - 结果: {Path(output_dir) / 'lda_results.json'}")
        logger.info(f"  - 图表: {config['paths']['viz_dir']}")
        logger.info("=" * 60 + "\n")
        
    except Exception as e:
        logger.error(f"程序出错: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
