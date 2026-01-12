import os
import google.generativeai as genai
from tavily import TavilyClient

# 自动从 GitHub Secrets 读取你存好的 Key
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 搜索指令：锁定美股小盘股 + 成交量突破 + 硬核利好
    query = "US small-cap stocks with massive volume breakout and hardcore positive news today"
    print("正在抓取实时市场数据...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 调用 Gemini 1.5 Flash 模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    你是一位专业的选股专家。请分析以下实时数据：
    {search_data}

    严格筛选符合以下【四大准则】的股票：
    1. 巨大的成交量突破（对比近期均量）。
    2. 收盘价格处于当日高位。
    3. 盘后交易表现强劲。
    4. 必须有“硬核利好”（如FDA批准、重大合同、财报大超预期）。

    请以 Markdown 表格形式输出：
    股票代码 | 硬核利好解析 | 关键数据(量价) | 综合评分(1-10) | 操作建议
    """
    
    response = model.generate_content(prompt)
    print("\n--- 选股机器人分析报告 ---")
    print(response.text)

if __name__ == "__main__":
    run_analysis()
