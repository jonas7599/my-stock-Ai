import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 搜索指令：锁定美股小盘股异动
    query = "US small-cap stocks with massive volume breakout and hardcore positive news today"
    print("正在搜集数据...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 使用最稳定的模型名称，防止找不到模型
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    分析以下实时数据：{search_data}
    
    请严格按照用户要求的【四大过滤标准】筛选股票：
    1. 成交量巨量突破。
    2. 收盘接近全天最高。
    3. 盘后延续强势。
    4. 必须有“硬核利好”（财报、FDA、合同）。
    
    请以表格输出：股票代码 | 利好解析 | 评分 | 操作建议
    """
    
    response = model.generate_content(prompt)
    print("\n" + "="*30)
    print("AI 选股分析报告")
    print("="*30)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
