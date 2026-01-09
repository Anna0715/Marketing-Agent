# 安装指南

## 自动安装（推荐）

### macOS/Linux

```bash
chmod +x install.sh
./install.sh
```

### Windows

双击运行 `install.bat` 或在命令行执行：

```cmd
install.bat
```

## 手动安装

### 1. 创建虚拟环境（推荐）

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. 升级pip

```bash
pip install --upgrade pip
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 分步安装（如果遇到问题）

如果一次性安装失败，可以分批安装：

```bash
# 1. 核心框架
pip install langchain langchain-openai langchain-community chromadb

# 2. 文档处理
pip install pypdf2 python-pptx python-docx openpyxl lxml

# 3. Web框架
pip install fastapi uvicorn pydantic pydantic-settings

# 4. 工具库
pip install python-dotenv requests aiohttp

# 5. 数据处理
pip install numpy pandas

# 6. LLM支持
pip install openai

# 7. 其他工具
pip install tiktoken tenacity
```

## 验证安装

运行以下命令验证关键包是否安装成功：

```bash
python -c "import langchain, chromadb, fastapi; print('安装成功！')"
```

## 常见问题

### Q: 权限错误

**解决方案：**
- 使用虚拟环境（推荐）
- 使用 `--user` 参数: `pip install -r requirements.txt --user`
- 使用管理员权限（不推荐）

### Q: 网络连接问题

**解决方案：**
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 某些包安装失败

**解决方案：**
- 移除有问题的包版本号，使用最新版本
- 单独安装失败的包: `pip install 包名`
- 检查Python版本是否满足要求（需要3.8+）

### Q: ChromaDB安装失败

**解决方案：**
```bash
# 可能需要系统依赖
# macOS
brew install cmake

# Ubuntu/Debian
sudo apt-get install cmake

# 然后再安装
pip install chromadb
```

## 最小化安装

如果只需要核心功能，可以只安装必需的包：

```bash
pip install langchain langchain-openai chromadb fastapi uvicorn pydantic pydantic-settings python-dotenv requests openai pypdf2 python-pptx
```

## 开发环境安装

开发时可能还需要：

```bash
pip install pytest black flake8 mypy
```
