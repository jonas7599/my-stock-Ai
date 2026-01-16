import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_options_intelligence():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 修改后的广域搜索词：不设限具体个股，只搜“小市值+期权异动”
    # 这样能确保 Tavily 抓到诸如 Barchart 或 Unusual Whales 的公开异动列表
    query = """
    Latest unusual options activity for US small-cap and penny stocks today. 
    Focus on: 
    1. Stocks under $10 with volume/OI ratio > 5.
    2. Large call sweeps on biotech and AI small caps.
    3. Option contracts with sudden spike in Open Interest near 52-week lows.
    4. Top 10 bullish option flow tickers for low-float stocks.
    """
    
    print(f"📡 正在全市场扫描小市值期权异动：锁定‘聪明钱’正在埋伏的低位标的...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 策略 Prompt：要求 AI 识别出具体的价位逻辑
    prompt = f"""
    分析数据：{search_data}

    你现在是一个期权异动分析专家。请从海量数据中提炼出 5 只最具有“爆发潜力”的小市值个股。
    
    你的筛选标准：
    - 排除 TSLA, NVDA 等大票。
    - 寻找那些股价在低位，但期权成交量突然达到持仓量（OI）数倍的标的。
    - 重点标注那些行权价距离现价很近（ATM）且到期日极短的看涨期权。

    请按以下表格输出：
    | 股票代码 | 股价 | 异常期权单 (价位/到期日) | 异动倍数 (Vol/OI) | 庄家意图分析 (扫货/压单) | 建议观察位 | 逻辑简述 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🔥"*15)
    print("💎 小市值期权黑马雷达 (2026-01-16) 💎")
    print("🔥"*15)
    print(response.text)

if __name__ == "__main__":
    run_options_intelligence()
