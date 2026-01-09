"""向量存储管理"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb  
from chromadb.config import Settings as ChromaSettings  
from langchain_openai import OpenAIEmbeddings  
from langchain_community.vectorstores import Chroma 
from langchain_text_splitters import RecursiveCharacterTextSplitter 

from src.utils.config import settings
from src.models.schemas import DocumentType


class VectorStore:
    """向量存储管理器"""
    
    def __init__(self):
        """初始化向量存储"""
        # 初始化embedding模型
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_base_url
        )
        
        # 初始化Chroma客户端
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # 初始化LangChain的向量存储
        self.vector_store = Chroma(
            client=self.client,
            collection_name=settings.collection_name,
            embedding_function=self.embeddings
        )
        
        # 文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
        )
    
    def add_documents(self, documents: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None):
        """添加文档到向量存储
        
        Args:
            documents: 文档列表，每个文档包含content和metadata
            metadata: 额外的元数据
        """
        texts = []
        metadatas = []
        ids = []
        
        for idx, doc in enumerate(documents):
            content = doc.get("content", "")
            doc_metadata = doc.get("metadata", {})
            
            # 如果内容太长，进行分割
            if len(content) > settings.chunk_size:
                splits = self.text_splitter.split_text(content)
                for split_idx, split_text in enumerate(splits):
                    texts.append(split_text)
                    metadatas.append({
                        **doc_metadata,
                        **(metadata or {}),
                        "split_index": split_idx
                    })
                    ids.append(f"{doc_metadata.get('source', 'doc')}_{idx}_{split_idx}")
            else:
                texts.append(content)
                metadatas.append({
                    **doc_metadata,
                    **(metadata or {})
                })
                ids.append(f"{doc_metadata.get('source', 'doc')}_{idx}")
        
        # 批量添加到向量存储
        if texts:
            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"成功添加 {len(texts)} 个文档块到向量存储")
    
    def search(self, query: str, k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """搜索相关文档
        
        Args:
            query: 查询文本
            k: 返回的文档数量
            filter_dict: 过滤条件
        
        Returns:
            相关文档列表，包含content、metadata和score
        """
        # 使用LangChain的相似度搜索
        if filter_dict:
            docs_with_scores = self.vector_store.similarity_search_with_score(
                query, k=k, filter=filter_dict
            )
        else:
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
        
        results = []
        for doc, score in docs_with_scores:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })
        
        return results
    
    def delete_documents(self, source: str):
        """根据源文件路径删除文档"""
        try:
            # 获取所有匹配的文档ID
            results = self.collection.get(where={"source": source})
            if results and results.get("ids"):
                self.collection.delete(ids=results["ids"])
                print(f"成功删除源文件 {source} 的所有文档块")
        except Exception as e:
            print(f"删除文档时出错: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取向量存储统计信息"""
        count = self.collection.count()
        return {
            "total_documents": count,
            "collection_name": settings.collection_name,
            "embedding_model": settings.embedding_model
        }
    
    def clear_all(self):
        """清空所有向量存储数据"""
        try:
            self.client.delete_collection(name=settings.collection_name)
            self.collection = self.client.create_collection(
                name=settings.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            self.vector_store = Chroma(
                client=self.client,
                collection_name=settings.collection_name,
                embedding_function=self.embeddings
            )
            print("已清空向量存储")
        except Exception as e:
            print(f"清空向量存储时出错: {e}")
