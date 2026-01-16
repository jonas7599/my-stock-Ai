import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_options_intelligence():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 专门搜索期权链数据和异动大单
    query = """
    US stock market: unusual options activity today, 
    highest open interest call strikes for small caps, 
    Gamma Wall and Max Pain levels for trending stocks, 
    massive bullish option sweeps Jan 2026.
    """
    print(f"📡 正在扫描期权市场：追踪大单轨迹与行权价分布...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 策略 Prompt：要求 AI 给出具体期权价位
    prompt = f"""
    分析数据：{search_data}

    作为期权策略专家，请结合期权链数据，筛选出 5 只最值得关注的个股。
    
    必须包含以下信息：
    1. 异常看涨期权（Unusual Call）的到期日和行权价。
    2. 最大持仓量（Open Interest）的压力位。
    3. 结合期权价位预测股价的“目标引力区”。

    请严格按以下表格输出：
    | 代码 | 当前价 | 异常期权大单 (行权价/到期日) | 期权看涨/看跌比 | 多头核心阻力点 | 庄家成本暗示 | 综合操盘建议 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "💎"*15)
    print("🔥 期权异动 & 庄家价位预测 (2026-01-16) 🔥")
    print("💎"*15)
    print(response.text)

if __name__ == "__main__":
    run_options_intelligence()

