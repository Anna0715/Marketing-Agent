"""数据模型定义"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    """文档类型枚举"""
    PDF = "pdf"
    PPTX = "pptx"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"
    FEISHU = "feishu"


class SolutionRequest(BaseModel):
    """营销解决方案请求"""
    customer_name: str = Field(..., description="客户名称")
    industry: Optional[str] = Field(None, description="行业类型")
    requirements: str = Field(..., description="客户需求描述")
    budget: Optional[float] = Field(None, description="预算范围")
    additional_context: Optional[Dict[str, Any]] = Field(None, description="额外上下文信息")


class SolutionResponse(BaseModel):
    """营销解决方案响应"""
    solution_id: str = Field(..., description="方案ID")
    customer_name: str = Field(..., description="客户名称")
    solution_content: str = Field(..., description="解决方案内容")
    referenced_cases: List[str] = Field(default=[], description="参考的案例ID列表")
    referenced_docs: List[str] = Field(default=[], description="参考的文档列表")
    data_sources: List[str] = Field(default=[], description="数据来源")
    generated_at: datetime = Field(default_factory=datetime.now, description="生成时间")
    confidence_score: Optional[float] = Field(None, description="置信度分数")


class DocumentMetadata(BaseModel):
    """文档元数据"""
    doc_id: str
    title: str
    doc_type: DocumentType
    upload_time: datetime
    file_path: str
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class DataQueryRequest(BaseModel):
    """数据查询请求"""
    query_type: str = Field(..., description="查询类型")
    parameters: Dict[str, Any] = Field(..., description="查询参数")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")


class DataQueryResponse(BaseModel):
    """数据查询响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    query_time: datetime = Field(default_factory=datetime.now)
