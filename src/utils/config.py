"""配置管理"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import yaml

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """应用配置"""
    
    # OpenAI配置
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    # 第三方API配置
    external_api_key: str = os.getenv("API_KEY", "")
    external_api_base_url: str = os.getenv("API_BASE_URL", "https://api.example.com")
    
    # 飞书配置
    feishu_app_id: Optional[str] = os.getenv("FEISHU_APP_ID")
    feishu_app_secret: Optional[str] = os.getenv("FEISHU_APP_SECRET")
    
    # 向量数据库配置
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    
    # RAG配置
    chunk_size: int = 1000
    chunk_overlap: int = 200
    embedding_model: str = "text-embedding-ada-002"
    collection_name: str = "marketing_solutions"
    
    # Agent配置
    agent_model: str = "gpt-4"
    agent_temperature: float = 0.7
    agent_max_tokens: int = 2000
    
    # 知识库路径
    knowledge_base_path: Path = Path("./knowledge_base")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()

# 确保知识库目录存在
settings.knowledge_base_path.mkdir(parents=True, exist_ok=True)
Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
