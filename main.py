import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API，从 GitHub Secrets 读取密钥
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

tavily = TavilyClient(api_key=TAVILY_KEY)
genai.configure(api_key=GEMINI_KEY)

def run_analysis():
    # 搜索指令：锁定美股小盘股异动
    query = "US small-cap stocks with massive volume breakout and hardcore positive news today"
    print("正在抓取实时市场数据...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 修复 404 错误：使用最稳定的模型版本名称
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    分析以下实时数据：{search_data}
    
    请严格按照以下标准筛选股票：
    1. 成交量巨大突破（对比近期均量）。
    2. 收盘接近全天最高。
    3. 盘后延续强势。
    4. 必须有“硬核利好”（财报超预期、FDA审批、重大合同）。
    
    请以 Markdown 表格输出：股票代码 | 硬核利好解析 | 关键数据评分(1-10) | 操作建议
    """
    
    response = model.generate_content(prompt)
    print("\n" + "="*30)
    print("AI 选股分析报告")
    print("="*30)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
