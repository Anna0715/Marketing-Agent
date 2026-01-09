"""第三方大数据API集成"""
import requests  # pyright: ignore[reportMissingModuleSource]
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from src.utils.config import settings
from src.models.schemas import DataQueryRequest, DataQueryResponse


class ExternalDataAPI:
    """第三方大数据API客户端"""
    
    def __init__(self):
        self.base_url = settings.external_api_base_url
        self.api_key = settings.external_api_key
        self.timeout = 30
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def query_company_data(self, company_name: str, data_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """查询公司内部数据
        
        Args:
            company_name: 公司名称
            data_types: 数据类型列表，如 ['financial', 'sales', 'marketing']
        
        Returns:
            公司数据字典
        """
        if not data_types:
            data_types = ["financial", "sales", "marketing", "operations"]
        
        try:
            url = f"{self.base_url}/api/v1/company/data"
            params = {
                "company_name": company_name,
                "data_types": ",".join(data_types)
            }
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": "查询成功"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": f"API返回错误: {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"查询失败: {str(e)}"
            }
    
    def query_industry_data(self, industry: str, metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """查询行业数据
        
        Args:
            industry: 行业名称
            metrics: 指标列表，如 ['growth_rate', 'market_size', 'trends']
        
        Returns:
            行业数据字典
        """
        if not metrics:
            metrics = ["growth_rate", "market_size", "trends", "competitors"]
        
        try:
            url = f"{self.base_url}/api/v1/industry/data"
            params = {
                "industry": industry,
                "metrics": ",".join(metrics)
            }
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": "查询成功"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": f"API返回错误: {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"查询失败: {str(e)}"
            }
    
    def query_customer_history(self, customer_name: str) -> Dict[str, Any]:
        """查询客户历史数据
        
        Args:
            customer_name: 客户名称
        
        Returns:
            客户历史数据字典
        """
        try:
            url = f"{self.base_url}/api/v1/customer/history"
            params = {"customer_name": customer_name}
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": "查询成功"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": f"API返回错误: {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"查询失败: {str(e)}"
            }
    
    def generic_query(self, request: DataQueryRequest) -> DataQueryResponse:
        """通用查询接口
        
        Args:
            request: 查询请求
        
        Returns:
            查询响应
        """
        try:
            url = f"{self.base_url}/api/v1/query"
            payload = {
                "query_type": request.query_type,
                "parameters": request.parameters,
                "filters": request.filters or {}
            }
            
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return DataQueryResponse(
                    success=True,
                    data=result.get("data"),
                    message=result.get("message", "查询成功")
                )
            else:
                return DataQueryResponse(
                    success=False,
                    message=f"API返回错误: {response.status_code}"
                )
        except Exception as e:
            return DataQueryResponse(
                success=False,
                message=f"查询失败: {str(e)}"
            )
