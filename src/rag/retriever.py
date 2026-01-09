"""RAG检索器"""
from typing import List, Dict, Any, Optional
from src.rag.vector_store import VectorStore
from src.utils.config import settings


class RAGRetriever:
    """RAG检索器 - 负责从知识库中检索相关信息"""
    
    def __init__(self, vector_store: Optional[VectorStore] = None):
        """初始化检索器"""
        self.vector_store = vector_store or VectorStore()
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回的文档数量
            filters: 过滤条件（如按文档类型、标签等过滤）
            min_score: 最小相似度分数
        
        Returns:
            相关文档列表
        """
        results = self.vector_store.search(
            query=query,
            k=top_k,
            filter_dict=filters
        )
        
        # 过滤低分结果
        filtered_results = [
            r for r in results 
            if r.get("score", 0.0) >= min_score
        ]
        
        return filtered_results
    
    def retrieve_for_solution(
        self,
        customer_name: str,
        industry: Optional[str],
        requirements: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """为营销解决方案检索相关信息
        
        Args:
            customer_name: 客户名称
            industry: 行业类型
            requirements: 需求描述
            top_k: 返回的文档数量
        
        Returns:
            包含相关案例、方案和相关文档的字典
        """
        # 构建查询
        query_parts = [requirements]
        if customer_name:
            query_parts.append(f"客户 {customer_name}")
        if industry:
            query_parts.append(f"{industry} 行业")
        
        query = " ".join(query_parts)
        
        # 检索相关文档
        all_results = self.retrieve(query, top_k=top_k * 2)
        
        # 分类整理结果
        cases = []
        solutions = []
        other_docs = []
        
        for result in all_results:
            metadata = result.get("metadata", {})
            source = metadata.get("source", "")
            content = result.get("content", "")
            
            # 简单的关键词匹配分类（可以根据实际需求优化）
            if "案例" in content or "case" in source.lower():
                cases.append(result)
            elif "方案" in content or "solution" in source.lower():
                solutions.append(result)
            else:
                other_docs.append(result)
        
        return {
            "cases": cases[:top_k],
            "solutions": solutions[:top_k],
            "related_docs": other_docs[:top_k],
            "query": query,
            "total_results": len(all_results)
        }
