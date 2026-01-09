"""使用示例脚本"""
import asyncio
import json
from pathlib import Path

from src.agent.agent import MarketingSolutionAgent
from src.knowledge_base_manager import KnowledgeBaseManager
from src.models.schemas import SolutionRequest


def example_1_add_documents():
    """示例1: 添加文档到知识库"""
    print("=" * 50)
    print("示例1: 添加文档到知识库")
    print("=" * 50)
    
    kb_manager = KnowledgeBaseManager()
    
    # 添加单个文档
    # 注意：需要替换为实际的文件路径
    # doc_path = "./knowledge_base/example.pdf"
    # if Path(doc_path).exists():
    #     metadata = kb_manager.add_document(doc_path, tags=["营销方案", "案例"])
    #     print(f"成功添加文档: {metadata.doc_id}")
    #     print(f"标题: {metadata.title}")
    #     print(f"类型: {metadata.doc_type}")
    
    # 批量添加目录中的文档
    kb_dir = Path("./knowledge_base")
    if kb_dir.exists():
        results = kb_manager.add_directory(str(kb_dir), recursive=True)
        print(f"\n成功添加 {len(results)} 个文档")
        for result in results[:3]:  # 只显示前3个
            print(f"  - {result.title} ({result.doc_type})")
    
    # 获取统计信息
    stats = kb_manager.get_stats()
    print(f"\n知识库统计:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def example_2_generate_solution():
    """示例2: 生成营销解决方案"""
    print("\n" + "=" * 50)
    print("示例2: 生成营销解决方案")
    print("=" * 50)
    
    agent = MarketingSolutionAgent()
    
    # 构建请求
    request = SolutionRequest(
        customer_name="ABC科技公司",
        industry="电子商务",
        requirements="需要提升线上销售额，目标增长30%，重点提升品牌知名度和用户转化率",
        budget=500000,
        additional_context={
            "target_audience": "25-40岁都市白领",
            "product_type": "时尚服饰",
            "current_channels": ["线上商城", "社交媒体"]
        }
    )
    
    print(f"客户: {request.customer_name}")
    print(f"行业: {request.industry}")
    print(f"需求: {request.requirements}")
    print("\n正在生成解决方案...")
    
    # 生成解决方案
    try:
        solution = agent.generate_solution(request)
        
        print(f"\n解决方案ID: {solution.solution_id}")
        print(f"\n解决方案内容:")
        print("-" * 50)
        print(solution.solution_content)
        print("-" * 50)
        
        if solution.referenced_cases:
            print(f"\n参考案例 ({len(solution.referenced_cases)} 个):")
            for case in solution.referenced_cases[:3]:
                print(f"  - {case}")
        
        if solution.referenced_docs:
            print(f"\n参考文档 ({len(solution.referenced_docs)} 个):")
            for doc in solution.referenced_docs[:3]:
                print(f"  - {doc}")
        
        print(f"\n生成时间: {solution.generated_at}")
        
    except Exception as e:
        print(f"生成解决方案时出错: {e}")
        print("提示: 请确保已配置OpenAI API密钥，并已添加文档到知识库")


def example_3_query_data():
    """示例3: 查询第三方数据"""
    print("\n" + "=" * 50)
    print("示例3: 查询第三方数据")
    print("=" * 50)
    
    from src.api.data_api import ExternalDataAPI
    
    data_api = ExternalDataAPI()
    
    # 查询公司数据
    print("查询公司数据...")
    result = data_api.query_company_data(
        company_name="ABC科技公司",
        data_types=["financial", "sales", "marketing"]
    )
    
    if result["success"]:
        print("查询成功!")
        print(json.dumps(result["data"], indent=2, ensure_ascii=False))
    else:
        print(f"查询失败: {result['message']}")
        print("提示: 请确保已配置第三方API密钥，或使用模拟数据进行测试")
    
    # 查询行业数据
    print("\n查询行业数据...")
    result = data_api.query_industry_data(
        industry="电子商务",
        metrics=["growth_rate", "market_size"]
    )
    
    if result["success"]:
        print("查询成功!")
        print(json.dumps(result["data"], indent=2, ensure_ascii=False))
    else:
        print(f"查询失败: {result['message']}")


def example_4_knowledge_base_search():
    """示例4: 知识库检索"""
    print("\n" + "=" * 50)
    print("示例4: 知识库检索")
    print("=" * 50)
    
    from src.rag.retriever import RAGRetriever
    
    retriever = RAGRetriever()
    
    # 搜索查询
    query = "提升线上销售额的营销策略"
    print(f"查询: {query}\n")
    
    results = retriever.retrieve(query, top_k=3)
    
    if results:
        print(f"找到 {len(results)} 个相关文档:\n")
        for i, result in enumerate(results, 1):
            content = result.get("content", "")[:200]
            score = result.get("score", 0.0)
            source = result.get("metadata", {}).get("source", "未知")
            
            print(f"[结果 {i}] 相似度: {score:.3f}")
            print(f"来源: {source}")
            print(f"内容: {content}...\n")
    else:
        print("未找到相关文档")
        print("提示: 请先添加文档到知识库")


def main():
    """主函数"""
    print("营销解决方案Agent系统 - 使用示例\n")
    
    # 运行示例
    try:
        # 示例1: 添加文档
        example_1_add_documents()
        
        # 示例2: 生成解决方案
        # example_2_generate_solution()
        
        # 示例3: 查询数据
        # example_3_query_data()
        
        # 示例4: 知识库检索
        # example_4_knowledge_base_search()
        
    except KeyboardInterrupt:
        print("\n\n示例被用户中断")
    except Exception as e:
        print(f"\n运行示例时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
