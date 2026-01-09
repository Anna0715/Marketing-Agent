"""主应用入口"""
import uvicorn 
from fastapi import FastAPI, HTTPException, UploadFile, File, Form  
from fastapi.middleware.cors import CORSMiddleware  
from typing import Optional, List
from pathlib import Path
import os
from src.agent.agent import MarketingSolutionAgent
from src.knowledge_base_manager import KnowledgeBaseManager
from src.models.schemas import (
    SolutionRequest,
    SolutionResponse,
    DataQueryRequest,
    DataQueryResponse
)
from src.api.data_api import ExternalDataAPI

# 创建FastAPI应用
app = FastAPI(
    title="营销解决方案Agent API",
    description="基于RAG的客户营销解决方案生成系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化全局组件
agent = MarketingSolutionAgent()
kb_manager = KnowledgeBaseManager()
data_api = ExternalDataAPI()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "营销解决方案Agent API",
        "version": "1.0.0",
        "endpoints": {
            "生成解决方案": "/api/v1/solution/generate",
            "上传文档": "/api/v1/knowledge-base/upload",
            "查询数据": "/api/v1/data/query",
            "知识库统计": "/api/v1/knowledge-base/stats"
        }
    }


@app.post("/api/v1/solution/generate", response_model=SolutionResponse)
async def generate_solution(request: SolutionRequest):
    """生成营销解决方案
    
    Args:
        request: 解决方案请求
    
    Returns:
        解决方案响应
    """
    try:
        solution = agent.generate_solution(request)
        return solution
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成解决方案失败: {str(e)}")


@app.post("/api/v1/knowledge-base/upload")
async def upload_document(
    file: UploadFile = File(...),
    tags: Optional[str] = Form(None)
):
    """上传文档到知识库
    
    Args:
        file: 上传的文件
        tags: 文档标签（逗号分隔）
    
    Returns:
        上传结果
    """
    try:
        # 保存临时文件
        upload_dir = Path("./uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 解析标签
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else None
        
        # 添加到知识库
        metadata = kb_manager.add_document(str(file_path), tags=tag_list)
        
        # 删除临时文件
        os.remove(file_path)
        
        return {
            "success": True,
            "message": "文档上传成功",
            "metadata": metadata.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传文档失败: {str(e)}")


@app.post("/api/v1/knowledge-base/add-path")
async def add_document_path(
    path: str,
    tags: Optional[str] = None,
    recursive: bool = True
):
    """通过路径添加文档到知识库
    
    Args:
        path: 文档路径或目录路径
        tags: 文档标签（逗号分隔）
        recursive: 是否递归查找（仅目录时有效）
    
    Returns:
        添加结果
    """
    try:
        path_obj = Path(path)
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else None
        
        if path_obj.is_file():
            # 单个文件
            metadata = kb_manager.add_document(path, tags=tag_list)
            return {
                "success": True,
                "message": "文档添加成功",
                "metadata": [metadata.dict()]
            }
        elif path_obj.is_dir():
            # 目录
            results = kb_manager.add_directory(path, recursive=recursive)
            return {
                "success": True,
                "message": f"成功添加 {len(results)} 个文档",
                "metadata": [m.dict() for m in results]
            }
        else:
            raise HTTPException(status_code=400, detail="路径不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加文档失败: {str(e)}")


@app.delete("/api/v1/knowledge-base/remove")
async def remove_document(source: str):
    """从知识库中移除文档
    
    Args:
        source: 文档源路径
    """
    try:
        kb_manager.remove_document(source)
        return {"success": True, "message": "文档已移除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"移除文档失败: {str(e)}")


@app.get("/api/v1/knowledge-base/stats")
async def get_knowledge_base_stats():
    """获取知识库统计信息"""
    try:
        stats = kb_manager.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


@app.post("/api/v1/data/query", response_model=DataQueryResponse)
async def query_data(request: DataQueryRequest):
    """查询第三方数据API
    
    Args:
        request: 数据查询请求
    
    Returns:
        查询响应
    """
    try:
        response = data_api.generic_query(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询数据失败: {str(e)}")


@app.post("/api/v1/data/company")
async def query_company_data(
    company_name: str,
    data_types: Optional[str] = None
):
    """查询公司数据
    
    Args:
        company_name: 公司名称
        data_types: 数据类型（逗号分隔）
    """
    try:
        types_list = [t.strip() for t in data_types.split(",")] if data_types else None
        result = data_api.query_company_data(company_name, data_types=types_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询公司数据失败: {str(e)}")


@app.post("/api/v1/data/industry")
async def query_industry_data(
    industry: str,
    metrics: Optional[str] = None
):
    """查询行业数据
    
    Args:
        industry: 行业名称
        metrics: 指标（逗号分隔）
    """
    try:
        metrics_list = [m.strip() for m in metrics.split(",")] if metrics else None
        result = data_api.query_industry_data(industry, metrics=metrics_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询行业数据失败: {str(e)}")


if __name__ == "__main__":
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
