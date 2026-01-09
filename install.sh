#!/bin/bash

# 营销解决方案Agent系统 - 依赖安装脚本

echo "=========================================="
echo "安装项目依赖包"
echo "=========================================="
echo ""

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3.8+"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "检测到 Python 版本: $python_version"
echo ""

# 检查是否使用虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    echo "未检测到虚拟环境，建议使用虚拟环境安装"
    read -p "是否创建虚拟环境? (y/n): " create_venv
    
    if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
        echo "创建虚拟环境..."
        python3 -m venv venv
        
        if [ $? -eq 0 ]; then
            echo "激活虚拟环境..."
            source venv/bin/activate
            echo "虚拟环境已激活"
        else
            echo "警告: 虚拟环境创建失败，将使用系统Python环境"
        fi
    fi
else
    echo "当前已在虚拟环境中: $VIRTUAL_ENV"
fi

echo ""
echo "升级 pip..."
python3 -m pip install --upgrade pip --quiet

echo ""
echo "安装依赖包..."
echo "这可能需要几分钟时间..."
echo ""

# 尝试安装
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 依赖包安装成功！"
    echo "=========================================="
    echo ""
    echo "下一步："
    echo "1. 配置环境变量: cp env.example .env"
    echo "2. 编辑 .env 文件，填写你的 API 密钥"
    echo "3. 启动服务: python main.py"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ 依赖包安装失败"
    echo "=========================================="
    echo ""
    echo "可能的解决方案："
    echo "1. 使用虚拟环境: python3 -m venv venv && source venv/bin/activate"
    echo "2. 使用管理员权限: sudo pip install -r requirements.txt"
    echo "3. 手动安装关键包: pip install langchain langchain-openai chromadb fastapi"
    echo ""
    exit 1
fi
