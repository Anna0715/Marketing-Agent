"""Agent核心实现"""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]
from langchain.agents import create_agent  # pyright: ignore[reportMissingImports]
from langchain.memory import ConversationBufferMemory  # pyright: ignore[reportMissingImports]
from langchain_core.messages import HumanMessage, SystemMessage  # pyright: ignore[reportMissingImports]

from src.agent.tools import (
    KnowledgeBaseSearchTool,
    CaseRetrievalTool,
    CompanyDataQueryTool,
    IndustryDataQueryTool
)
from src.rag.retriever import RAGRetriever
from src.api.data_api import ExternalDataAPI
from src.models.schemas import SolutionRequest, SolutionResponse
from src.utils.config import settings


class MarketingSolutionAgent:
    """营销解决方案Agent"""
    
    def __init__(
        self,
        retriever: Optional[RAGRetriever] = None,
        data_api: Optional[ExternalDataAPI] = None
    ):
        """初始化Agent"""
        self.retriever = retriever or RAGRetriever()
        self.data_api = data_api or ExternalDataAPI()
        
        # 初始化LLM
        self.llm = ChatOpenAI(
            model_name=settings.agent_model,
            temperature=settings.agent_temperature,
            max_tokens=settings.agent_max_tokens,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_base_url
        )
        
        # 初始化工具
        self.tools = self._create_tools()
        
        # 初始化Agent
        self.agent = self._create_agent()
    
    def _create_tools(self) -> List:
        """创建工具列表"""
        return [
            KnowledgeBaseSearchTool(retriever=self.retriever),
            CaseRetrievalTool(retriever=self.retriever),
            CompanyDataQueryTool(data_api=self.data_api),
            IndustryDataQueryTool(data_api=self.data_api),
        ]
    
    def _create_agent(self):
        """创建Agent实例"""
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Agent系统提示词
        system_message = """你是一个专业的营销解决方案专家，擅长为客户制定个性化的营销方案。

你的任务是：
1. 理解客户的需求和背景
2. 从知识库中检索相关的营销解决方案和客户案例
3. 查询公司内部数据作为辅助参考
4. 基于检索到的信息和数据，生成专业的营销解决方案

请确保：
- 方案内容具体、可执行
- 参考并引用相关的客户案例
- 利用数据支撑你的建议
- 方案结构清晰，包括目标、策略、执行计划和预期效果"""
        
        # 在 langchain 1.x 中使用 create_agent
        # 将工具绑定到 LLM
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        # 创建 agent（返回一个 graph）
        agent_graph = create_agent(
            model=llm_with_tools,
            tools=self.tools,
            system_prompt=system_message,
            debug=True
        )
        
        return agent_graph
    
    def generate_solution(self, request: SolutionRequest) -> SolutionResponse:
        """生成营销解决方案
        
        Args:
            request: 解决方案请求
        
        Returns:
            解决方案响应
        """
        # 构建查询提示
        query_parts = [
            f"客户名称: {request.customer_name}",
            f"需求描述: {request.requirements}"
        ]
        
        if request.industry:
            query_parts.append(f"行业类型: {request.industry}")
        if request.budget:
            query_parts.append(f"预算范围: {request.budget}")
        
        if request.additional_context:
            for key, value in request.additional_context.items():
                query_parts.append(f"{key}: {value}")
        
        query = "\n".join(query_parts)
        
        # 首先检索相关知识库信息
        retrieval_results = self.retriever.retrieve_for_solution(
            customer_name=request.customer_name,
            industry=request.industry,
            requirements=request.requirements,
            top_k=5
        )
        
        # 构建Agent的输入提示
        agent_prompt = f"""请为以下客户制定营销解决方案：

{query}

我已经检索到以下相关信息供参考：

相关案例：
{self._format_results(retrieval_results.get('cases', []))}

相关方案：
{self._format_results(retrieval_results.get('solutions', []))}

请：
1. 如果客户公司有内部数据，请先查询公司数据
2. 如果提供了行业信息，请查询行业数据
3. 基于所有信息，生成一个完整的营销解决方案

方案应该包括：
- 客户背景分析
- 目标设定
- 营销策略
- 执行计划
- 预期效果
- 参考案例说明"""
        
        # 调用Agent生成方案
        try:
            # 在 langchain 1.x 中，agent 是一个 graph，需要使用 invoke
            if hasattr(self.agent, 'invoke'):
                result = self.agent.invoke({"messages": [HumanMessage(content=agent_prompt)]})
                solution_content = result.get("messages", [])[-1].content if isinstance(result, dict) else str(result)
            elif hasattr(self.agent, 'run'):
                solution_content = self.agent.run(agent_prompt)
            else:
                # 回退到直接使用 LLM
                messages = [SystemMessage(content="你是一个专业的营销解决方案专家。"), HumanMessage(content=agent_prompt)]
                response = self.llm.invoke(messages)
                solution_content = response.content if hasattr(response, 'content') else str(response)
            
            # 提取参考的案例和文档
            referenced_cases = [
                r.get("metadata", {}).get("source", "")
                for r in retrieval_results.get("cases", [])
            ]
            referenced_docs = [
                r.get("metadata", {}).get("source", "")
                for r in retrieval_results.get("related_docs", [])
            ]
            
            # 生成解决方案响应
            solution_id = str(uuid.uuid4())
            response = SolutionResponse(
                solution_id=solution_id,
                customer_name=request.customer_name,
                solution_content=solution_content,
                referenced_cases=referenced_cases[:5],  # 限制数量
                referenced_docs=referenced_docs[:5],
                data_sources=["knowledge_base", "external_api"],
                generated_at=datetime.now()
            )
            
            return response
            
        except Exception as e:
            # 如果Agent执行失败，返回错误信息
            return SolutionResponse(
                solution_id=str(uuid.uuid4()),
                customer_name=request.customer_name,
                solution_content=f"生成解决方案时出错: {str(e)}",
                generated_at=datetime.now()
            )
    
    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        """格式化检索结果"""
        if not results:
            return "无相关信息"
        
        formatted = []
        for i, result in enumerate(results, 1):
            content = result.get("content", "")[:300]
            metadata = result.get("metadata", {})
            source = metadata.get("source", "未知来源")
            formatted.append(f"[{i}] {source}: {content}...")
        
        return "\n".join(formatted)
