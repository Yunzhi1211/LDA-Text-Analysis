@echo off
chcp 65001 >nul
REM LDA Analysis - 快速启动脚本 (Windows)

echo.
echo ========================================
echo   LDA 主题分析 - 快速启动
echo ========================================
echo.

REM 使用Python 3.13（3.14太新，部分库不兼容）
set PYTHON=C:\Users\lenovo\AppData\Local\Programs\Python\Python313\python.exe
set PIP=C:\Users\lenovo\AppData\Local\Programs\Python\Python313\Scripts\pip.exe

REM 检查Python
"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python 3.13，请先安装
    pause
    exit /b 1
)

REM 安装依赖
echo [1] 安装依赖包...
"%PIP%" install -q -r 0_config\requirements.txt

REM 清除Python缓存（确保用最新代码）
if exist 4_scripts\__pycache__ rd /s /q 4_scripts\__pycache__

REM 检查input文件夹
if not exist 1_input (
    echo [!] 创建1_input文件夹...
    mkdir 1_input
    echo [!] 请将DOCX文件放入 1_input\ 文件夹
)

REM 运行分析
echo.
echo [2] 开始分析...
echo.
"%PYTHON%" main.py

echo.
echo ========================================
echo   分析完成！
echo ========================================
echo 结果位置: 2_output/
echo   - 模型: 2_output/lda_model/
echo   - 结果: 2_output/lda_results.json
echo   - 图表: 2_output/visualizations/
echo   - 日志: 3_log/
echo.
echo 查看交互式可视化: 使用浏览器打开
echo   2_output/visualizations/lda_interactive.html
echo.
pause
