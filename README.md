# 营销解决方案Agent系统

基于RAG（检索增强生成）的客户营销解决方案生成系统，支持多种文档格式的知识库管理和第三方数据API集成。
## 功能特性
- ✅ **RAG知识库系统**：支持PDF、PPTX、DOCX、TXT、MD、飞书文档等多种格式
- ✅ **智能文档检索**：基于向量相似度的语义检索
- ✅ **Agent智能生成**：基于LLM的营销解决方案自动生成
- ✅ **第三方数据集成**：支持查询公司内部数据和行业数据
- ✅ **RESTful API**：提供完整的API接口
## 系统架构
```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Web服务层                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 解决方案生成  │  │ 知识库管理   │  │ 数据查询API  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
│  Agent核心   │  │  RAG检索器    │  │ 第三方API    │
│              │  │              │  │              │
│ - LLM集成    │  │ - 向量检索   │  │ - 公司数据   │
│ - 工具调用   │  │ - 语义搜索   │  │ - 行业数据   │
└───────┬──────┘  └───────┬──────┘  └──────────────┘
        │                 │
        │         ┌───────▼──────┐
        │         │  向量存储     │
        │         │  (ChromaDB)   │
        │         └───────┬──────┘
        │                 │
        └─────────┬───────┘
                  │
         ┌────────▼────────┐
         │   文档加载器     │
         │  - PDF/PPTX/    │
         │    DOCX/飞书    │
         └─────────────────┘
```

## 项目结构

```
.
├── config/                  # 配置文件
│   └── config.yaml
├── src/
│   ├── agent/              # Agent核心模块
│   │   ├── agent.py       # Agent主类
│   │   └── tools.py       # Agent工具定义
│   ├── api/                # API集成
│   │   └── data_api.py    # 第三方数据API
│   ├── models/             # 数据模型
│   │   └── schemas.py     # Pydantic模型
│   ├── rag/                # RAG模块
│   │   ├── document_loader.py  # 文档加载器
│   │   ├── vector_store.py     # 向量存储
│   │   └── retriever.py        # 检索器
│   ├── utils/              # 工具函数
│   │   └── config.py      # 配置管理
│   └── knowledge_base_manager.py  # 知识库管理器
├── knowledge_base/         # 知识库文档存储目录
├── chroma_db/             # 向量数据库存储目录
├── main.py                # 主应用入口
├── requirements.txt       # 依赖包
└── README.md             # 项目文档
```

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env.example` 为 `.env` 并填写配置：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```env
# OpenAI配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# 第三方大数据API配置
API_KEY=your_api_key_here
API_BASE_URL=https://api.example.com

# 飞书配置（可选）
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret

# 向量数据库配置
CHROMA_PERSIST_DIR=./chroma_db
```

## 使用方法

### 1. 启动服务

```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 添加文档到知识库

#### 方式1：通过API上传文件

```bash
curl -X POST "http://localhost:8000/api/v1/knowledge-base/upload" \
  -F "file=@/path/to/document.pdf" \
  -F "tags=营销方案,案例"
```

#### 方式2：通过路径添加

```bash
curl -X POST "http://localhost:8000/api/v1/knowledge-base/add-path" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "./knowledge_base",
    "recursive": true,
    "tags": "营销方案"
  }'
```

### 3. 生成营销解决方案

```bash
curl -X POST "http://localhost:8000/api/v1/solution/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "ABC公司",
    "industry": "电子商务",
    "requirements": "需要提升线上销售额，目标增长30%",
    "budget": 500000,
    "additional_context": {
      "target_audience": "25-40岁都市白领",
      "product_type": "时尚服饰"
    }
  }'
```

### 4. 查询数据

```bash
# 查询公司数据
curl -X POST "http://localhost:8000/api/v1/data/company?company_name=ABC公司&data_types=financial,sales"

# 查询行业数据
curl -X POST "http://localhost:8000/api/v1/data/industry?industry=电子商务&metrics=growth_rate,market_size"
```

## API文档

启动服务后，访问以下地址查看完整的API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要组件说明

### 1. Agent核心（`src/agent/agent.py`）

- 集成LangChain的Agent框架
- 支持工具调用和记忆管理
- 基于LLM生成营销解决方案

### 2. RAG检索器（`src/rag/retriever.py`）

- 基于向量相似度的语义检索
- 支持按案例、方案等分类检索
- 可配置的检索参数

### 3. 文档加载器（`src/rag/document_loader.py`）

- 支持PDF、PPTX、DOCX、TXT、MD格式
- 支持飞书文档加载
- 自动文档类型检测

### 4. 向量存储（`src/rag/vector_store.py`）

- 基于ChromaDB的持久化存储
- 支持文档的增删改查
- 自动文本分块和向量化

### 5. 第三方API（`src/api/data_api.py`）

- 公司数据查询接口
- 行业数据查询接口
- 通用的数据查询接口

## 开发说明

### 扩展文档格式支持

在 `src/rag/document_loader.py` 中添加新的加载器类，继承 `BaseDocumentLoader`，并在 `DocumentLoaderFactory` 中注册。

### 自定义Agent工具

在 `src/agent/tools.py` 中定义新的工具类，继承 `BaseTool`，然后在 `MarketingSolutionAgent._create_tools()` 中添加。

### 集成其他LLM

修改 `src/utils/config.py` 和 `src/agent/agent.py`，替换LLM初始化代码。

## 注意事项

1. **API密钥安全**：确保不要将 `.env` 文件提交到版本控制系统
2. **向量数据库**：首次运行会自动创建ChromaDB数据库
3. **文档大小**：建议单个文档不超过50MB
4. **并发请求**：生产环境建议使用gunicorn等WSGI服务器

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。
