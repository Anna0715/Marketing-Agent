#!/bin/bash

# 营销解决方案Agent系统启动脚本

echo "=========================================="
echo "营销解决方案Agent系统"
echo "=========================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在，请从 env.example 复制并配置"
    echo "运行: cp env.example .env"
fi

# 创建必要的目录
mkdir -p knowledge_base
mkdir -p uploads
mkdir -p chroma_db

# 启动服务
echo ""
echo "启动服务..."
echo "API文档地址: http://localhost:8000/docs"
echo "按 Ctrl+C 停止服务"
echo ""

python main.py
