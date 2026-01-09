"""知识库管理器 - 用于管理文档的导入和更新"""
import os
from pathlib import Path
from typing import List, Optional
import json

from src.rag.document_loader import DocumentLoaderFactory
from src.rag.vector_store import VectorStore
from src.models.schemas import DocumentType, DocumentMetadata
from src.utils.config import settings


class KnowledgeBaseManager:
    """知识库管理器"""
    
    def __init__(self):
        """初始化知识库管理器"""
        self.vector_store = VectorStore()
        self.loader_factory = DocumentLoaderFactory()
    
    def add_document(self, file_path: str, tags: Optional[List[str]] = None) -> DocumentMetadata:
        """添加文档到知识库
        
        Args:
            file_path: 文件路径（支持本地文件或飞书文档链接）
            tags: 文档标签
        
        Returns:
            文档元数据
        """
        # 检测文档类型
        doc_type = self.loader_factory.detect_doc_type(file_path)
        
        # 获取对应的加载器
        loader = self.loader_factory.get_loader(doc_type)
        
        # 加载文档
        documents = loader.load(file_path)
        
        # 提取元数据
        metadata = loader.extract_metadata(file_path, doc_type)
        if tags:
            metadata.tags = tags
        
        # 添加到向量存储
        self.vector_store.add_documents(
            documents=documents,
            metadata={
                "doc_id": metadata.doc_id,
                "title": metadata.title,
                "doc_type": doc_type.value,
                "tags": json.dumps(tags or []),
                **metadata.metadata
            }
        )
        
        return metadata
    
    def add_directory(self, directory_path: str, recursive: bool = True) -> List[DocumentMetadata]:
        """批量添加目录中的文档
        
        Args:
            directory_path: 目录路径
            recursive: 是否递归查找
        
        Returns:
            文档元数据列表
        """
        results = []
        path = Path(directory_path)
        
        if not path.exists():
            print(f"目录不存在: {directory_path}")
            return results
        
        # 支持的文件扩展名
        supported_extensions = {".pdf", ".pptx", ".docx", ".txt", ".md"}
        
        # 查找文件
        if recursive:
            files = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in supported_extensions]
        else:
            files = [f for f in path.iterdir() if f.is_file() and f.suffix.lower() in supported_extensions]
        
        # 批量添加
        for file_path in files:
            try:
                metadata = self.add_document(str(file_path))
                results.append(metadata)
                print(f"成功添加文档: {file_path}")
            except Exception as e:
                print(f"添加文档失败 {file_path}: {e}")
        
        return results
    
    def remove_document(self, source: str):
        """从知识库中移除文档
        
        Args:
            source: 文档源路径
        """
        self.vector_store.delete_documents(source)
        print(f"已移除文档: {source}")
    
    def get_stats(self) -> dict:
        """获取知识库统计信息"""
        return self.vector_store.get_stats()
    
    def clear_all(self):
        """清空知识库"""
        self.vector_store.clear_all()
