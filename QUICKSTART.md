# 快速开始指南

## 前置要求

- Python 3.8+
- OpenAI API密钥（或其他兼容的LLM API）
- 第三方大数据API访问权限（可选）

## 5分钟快速启动

### 1. 克隆/下载项目

```bash
cd /path/to/project
```

### 2. 配置环境变量

```bash
cp env.example .env
```

编辑 `.env` 文件，至少配置：

```env
OPENAI_API_KEY=your_api_key_here
```

### 3. 安装依赖

```bash
# 使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

或使用启动脚本：

```bash
chmod +x start.sh
./start.sh
```

### 4. 添加文档到知识库（可选）

```bash
# 将PDF、PPTX、DOCX等文档放入 knowledge_base 目录
cp your_documents/* knowledge_base/

# 或通过Python脚本添加
python -c "
from src.knowledge_base_manager import KnowledgeBaseManager
kb = KnowledgeBaseManager()
kb.add_directory('./knowledge_base', recursive=True)
"
```

### 5. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

### 6. 访问API文档

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 第一个API调用

### 生成营销解决方案

```bash
curl -X POST "http://localhost:8000/api/v1/solution/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "ABC公司",
    "industry": "电子商务",
    "requirements": "提升线上销售额30%",
    "budget": 500000
  }'
```

### 上传文档

```bash
curl -X POST "http://localhost:8000/api/v1/knowledge-base/upload" \
  -F "file=@your_document.pdf" \
  -F "tags=营销方案,案例"
```

## 常见问题

### Q: 如何更换LLM模型？

A: 修改 `.env` 文件中的 `OPENAI_BASE_URL` 和配置，或修改 `src/utils/config.py` 中的LLM初始化代码。

### Q: 如何支持其他文档格式？

A: 在 `src/rag/document_loader.py` 中添加新的加载器类。

### Q: 向量数据库存储在哪里？

A: 默认存储在 `./chroma_db` 目录，可在 `.env` 中配置 `CHROMA_PERSIST_DIR`。

### Q: 如何配置第三方数据API？

A: 修改 `src/api/data_api.py` 中的API端点和方法，或实现自定义的数据查询逻辑。

## 下一步

- 阅读 [README.md](README.md) 了解完整功能
- 查看 [ARCHITECTURE.md](ARCHITECTURE.md) 了解架构设计
- 运行 `python example_usage.py` 查看使用示例
