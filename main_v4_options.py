import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_options_intelligence():
    # 自动获取当前最快模型 (Gemini 2.0 Flash)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 广域扫描：重点搜寻带代码（$TICKER）的列表数据
    query = """
    Latest top 15 unusual options activity for US small-cap stocks today. 
    Find stocks with high Call volume relative to Open Interest (Vol/OI > 5).
    Focus on tickers under $15 with massive bull sweeps.
    Extract specific stock symbols ($TICKER) for companies like biotech or AI startups.
    """
    
    print(f"📡 正在全市场扫描 10 个以上的小市值期权异动标的...")
    # 增加返回结果数量，确保 AI 有足够的原始材料
    search_data = tavily.search(query=query, search_depth="advanced", max_results=10)

    # 2. 策略 Prompt：要求强制输出代码并提供 10 个标的
    prompt = f"""
    分析数据：{search_data}

    任务：作为资深分析师，从异动名单中精选出【10 个】最具潜力的个股。
    
    硬性要求：
    - 必须输出【股票代码】（如 BTON, KALA）。如果原始信息只有公司名，请结合常识反查补齐。
    - 排除市值超过 50 亿美金的大票（如 TSLA, NVDA 等）。
    - 优先选择那些在低位横盘，但期权突然放量的标的。

    请严格按以下表格输出 10 个结果：
    | 代码 | 股价 | 异常期权 (行权价/日期) | Vol/OI 异动倍数 | 庄家动作 (扫货/防御) | 目标引力位 | 逻辑简述 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "💎"*15)
    print("🔥 小市值期权黑马雷达 (10 标的强化版) 🔥")
    print("💎"*15)
    print(response.text)

if __name__ == "__main__":
    run_options_intelligence()
