import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API 密钥
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_momentum_prediction():
    # 自动获取当前最强的 Flash 模型（Gemini 2.5 或 1.5）
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 精准搜索：锁定板块轮动、收盘极强势和盘后异动
    query = """
    US stock market top gainers with strong momentum, closing at daily highs, 
    massive volume breakout, and significant after-hours price action. 
    Focus on leading sectors like AI, Energy, or Biotech.
    """
    print(f"📡 正在扫描【次日连涨·五虎将】...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 深度分析 Prompt：要求输出三级止盈与止损
    prompt = f"""
    分析以下实时市场数据：{search_data}

    你的目标是筛选出 5 只预计在【次日及短期内】具有极强上涨惯性的股票。
    
    筛选标准：
    1. 形态：处于上升通道，今日收盘接近全天最高位。
    2. 量能：成交量显著放大（吸筹），盘后依然走强。
    3. 逻辑：处于当前资金热捧的板块，或有未消化的重大利好。

    请严格按以下表格格式输出：
    | 代码 | 行业板块 | 建议入场区间 | 短期目标(1-3d) | 中期目标(1-2w) | 后期/格局位 | 关键止损位 | 连涨逻辑解析 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """
    
    response = model.generate_content(prompt)
    
    print("\n" + "🔥"*15)
    print(f"💎 次日连涨·五虎将预测 (分析时间: 2026-01-15) 💎")
    print("🔥"*15)
    print(response.text)

if __name__ == "__main__":
    run_momentum_prediction()
