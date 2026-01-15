import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 强化搜索词：强制要求具体的代码 (Ticker) 和盘后异动数据
    query = """
    US small-cap stocks with unusual volume spikes today, 
    low float stocks consolidation near breakout, 
    stocks with positive Order Flow and high Bid/Ask ratio,
    upcoming FDA catalysts or earnings in next 2 weeks.
    """
    print(f"📡 正在执行精准深度扫描：锁定【换手率异动+委比占优】个股...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 强化 Prompt：明确要求 AI 必须搜寻代码和具体数值
    prompt = f"""
    分析数据：{search_data}

    作为顶级操盘手，请寻找“即将点火启动”的个股。
    
    必须满足以下硬性条件：
    - 必须输出明确的【股票代码】。
    - 处于缩量横盘后的第一个放量信号。
    - 板块属于当前热点（AI、低空经济、生物医药等）。

    请严格按此表格输出，若数据不全请根据市场经验预估：
    | 代码 | 行业 | 换手率/量能异动 | 潜伏利好 (FDA/财报/合同) | 预估点火窗口 | 建议埋伏区间 | 止损位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🎯"*15)
    print("💎 点火猎人·精准启动监控 💎")
    print("🎯"*15)
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
