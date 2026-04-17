#!/bin/bash
# LDA Analysis - 快速启动脚本 (Linux/Mac)

echo ""
echo "========================================"
echo "  LDA 主题分析 - 快速启动"
echo "========================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python 3，请先安装"
    exit 1
fi

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "[1] 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "[2] 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "[3] 安装依赖包..."
pip install -q -r requirements.txt

# 检查input文件夹
if [ ! -d "input" ]; then
    echo "[!] 创建input文件夹..."
    mkdir input
    echo "[!] 请将DOCX文件放入 input/ 文件夹"
fi

# 运行分析
echo ""
echo "[4] 开始分析..."
echo ""
python main.py

echo ""
echo "========================================"
echo "  分析完成！"
echo "========================================"
echo "结果位置: output/"
echo "  - 模型: output/lda_model/"
echo "  - 结果: output/lda_results.json"
echo "  - 图表: output/visualizations/"
echo ""
echo "查看交互式可视化（在浏览器打开）:"
echo "  output/visualizations/lda_interactive.html"
echo ""
