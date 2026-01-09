"""Agent工具定义"""
import json
from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool  # pyright: ignore[reportMissingImports]
from pydantic import Field

from src.rag.retriever import RAGRetriever
from src.api.data_api import ExternalDataAPI


class KnowledgeBaseSearchTool(BaseTool):
    """知识库搜索工具"""
    name = "knowledge_base_search"
    description = """用于搜索知识库中的营销解决方案、客户案例等相关文档。
    输入应该是一个清晰的搜索查询，描述你正在寻找的信息类型。"""
    
    retriever: RAGRetriever = Field(exclude=True)
    
    def _run(self, query: str) -> str:
        """执行搜索"""
        results = self.retriever.retrieve(query, top_k=5)
        
        if not results:
            return "未找到相关信息。"
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            content = result.get("content", "")[:500]  # 限制长度
            metadata = result.get("metadata", {})
            source = metadata.get("source", "未知来源")
            score = result.get("score", 0.0)
            
            formatted_results.append(
                f"[结果 {i}] (相似度: {score:.3f})\n"
                f"来源: {source}\n"
                f"内容: {content}...\n"
            )
        
        return "\n".join(formatted_results)
    
    async def _arun(self, query: str) -> str:
        """异步执行搜索"""
        return self._run(query)


class CaseRetrievalTool(BaseTool):
    """客户案例检索工具"""
    name = "retrieve_customer_cases"
    description = """从知识库中检索相关的客户案例。
    输入应该包含客户名称、行业类型或需求描述。"""
    
    retriever: RAGRetriever = Field(exclude=True)
    
    def _run(self, customer_name: str, industry: Optional[str] = None, requirements: Optional[str] = None) -> str:
        """执行案例检索"""
        query_parts = []
        if customer_name:
            query_parts.append(f"客户 {customer_name}")
        if industry:
            query_parts.append(f"{industry} 行业")
        if requirements:
            query_parts.append(requirements)
        
        query = " ".join(query_parts)
        
        results = self.retriever.retrieve_for_solution(
            customer_name=customer_name,
            industry=industry,
            requirements=requirements or "",
            top_k=3
        )
        
        cases = results.get("cases", [])
        if not cases:
            return "未找到相关客户案例。"
        
        formatted_cases = []
        for i, case in enumerate(cases, 1):
            content = case.get("content", "")[:800]
            metadata = case.get("metadata", {})
            source = metadata.get("source", "未知来源")
            
            formatted_cases.append(
                f"[案例 {i}]\n"
                f"来源: {source}\n"
                f"内容: {content}...\n"
            )
        
        return "\n".join(formatted_cases)
    
    async def _arun(self, customer_name: str, industry: Optional[str] = None, requirements: Optional[str] = None) -> str:
        """异步执行检索"""
        return self._run(customer_name, industry, requirements)


class CompanyDataQueryTool(BaseTool):
    """公司数据查询工具"""
    name = "query_company_data"
    description = """查询公司内部数据，包括财务、销售、营销等数据。
    输入应该是公司名称和需要查询的数据类型。"""
    
    data_api: ExternalDataAPI = Field(exclude=True)
    
    def _run(self, company_name: str, data_types: Optional[str] = None) -> str:
        """执行数据查询"""
        types_list = data_types.split(",") if data_types else None
        
        result = self.data_api.query_company_data(
            company_name=company_name,
            data_types=types_list
        )
        
        if result["success"]:
            data = result["data"]
            return f"公司数据查询成功:\n{json.dumps(data, ensure_ascii=False, indent=2)}"
        else:
            return f"查询失败: {result['message']}"
    
    async def _arun(self, company_name: str, data_types: Optional[str] = None) -> str:
        """异步执行查询"""
        return self._run(company_name, data_types)


class IndustryDataQueryTool(BaseTool):
    """行业数据查询工具"""
    name = "query_industry_data"
    description = """查询行业数据，包括增长率、市场规模、趋势等。
    输入应该是行业名称和需要查询的指标。"""
    
    data_api: ExternalDataAPI = Field(exclude=True)
    
    def _run(self, industry: str, metrics: Optional[str] = None) -> str:
        """执行行业数据查询"""
        metrics_list = metrics.split(",") if metrics else None
        
        result = self.data_api.query_industry_data(
            industry=industry,
            metrics=metrics_list
        )
        
        if result["success"]:
            data = result["data"]
            return f"行业数据查询成功:\n{json.dumps(data, ensure_ascii=False, indent=2)}"
        else:
            return f"查询失败: {result['message']}"
    
    async def _arun(self, industry: str, metrics: Optional[str] = None) -> str:
        """异步执行查询"""
        return self._run(industry, metrics)
