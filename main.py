import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 自动获取可用模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 搜索指令：同时抓取“强势突破”和“低位埋伏”的数据
    search_query = """
    1. US top stock gainers today with massive volume breakout and news.
    2. US small-cap stocks with upcoming catalysts (FDA, earnings) showing accumulation but price hasn't jumped yet.
    """
    print(f"📡 正在扫描全市场：包含【已启动强势股】与【低位埋伏股】...")
    search_data = tavily.search(query=search_query, search_depth="advanced")

    # 2. 策略拆分 Prompt
    prompt = f"""
    分析以下实时数据：{search_data}

    请根据以下两套独立策略，分别筛选出最符合要求的股票，并以表格形式输出：

    ---
    ### 策略 A：【动能追涨型】（已启动，抓主升浪）
    筛选标准：成交量激增、收盘极强势、有重大利好。
    输出表格：代码 | 行业 | 利好解析 | 综合评分 | 操作建议(追涨/回踩买)

    ---
    ### 策略 B：【拐点埋伏型】（未启动，抓起涨点）
    筛选标准：近期有吸筹迹象（缩量横盘）、即将有重大事件（下周财报/FDA）、价格尚未暴涨。
    输出表格：代码 | 预期利好事件及日期 | 吸筹迹象描述 | 准备就绪度(1-10) | 建议埋伏区间
    """

    response = model.generate_content(prompt)
    print("\n" + "★"*20)
    print("💎 双策略选股分析报告 💎")
    print("★"*20)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
