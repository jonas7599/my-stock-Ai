import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API，从 GitHub Secrets 读取密钥
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

tavily = TavilyClient(api_key=TAVILY_KEY)
genai.configure(api_key=GEMINI_KEY)

def run_analysis():
    # 搜索指令：锁定美股小盘股 + 成交量突破 + 硬核利好
    query = "US small-cap stocks with massive volume breakout and hardcore positive news today"
    print("正在抓取实时市场数据...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 修正后的模型名称：使用最新的 flash 稳定版
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    你是一位专业的量化交易专家。请根据以下实时数据进行筛选：
    {search_data}

    你的筛选必须严格遵守以下【四大指标】：
    1. 巨大的成交量突破（对比近期均量）。
    2. 收盘位置处于当日高位。
    3. 盘后表现强劲。
    4. 必须有“硬核正面利好”（如财报超预期、重大合同、FDA审批等）。

    请以 Markdown 表格形式输出：
    股票代码 | 成交量异动 | 收盘/盘后状态 | 硬核利好解析 | 综合评分(1-10)
    """
    
    response = model.generate_content(prompt)
    print("\n--- AI 选股分析报告 ---")
    print(response.text)

if __name__ == "__main__":
    run_analysis()
