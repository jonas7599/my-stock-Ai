import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 1. 自动寻找可用模型 (解决 404 问题的终极方案)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # 优先选 flash，没有就选第一个可用的
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    print(f"系统自动匹配模型: {target_model}")

    # 2. 抓取数据
    query = "US small-cap stocks with massive volume breakout and hardcore positive news today"
    print("正在搜集实时市场数据...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 生成报告
    model = genai.GenerativeModel(target_model)
    prompt = f"""
    分析以下实时数据：{search_data}
    
    严格按照以下【四大过滤准则】筛选：
    1. 成交量巨量突破。
    2. 收盘接近全天最高位。
    3. 盘后交易强劲。
    4. 必须有“硬核正面利好”（如财报大增、FDA批准、重大合同）。
    
    输出格式：Markdown 表格（股票代码 | 硬核利好解析 | 综合评分 | 操作建议）
    """
    
    response = model.generate_content(prompt)
    print("\n" + "="*30 + "\nAI 选股分析报告\n" + "="*30)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
