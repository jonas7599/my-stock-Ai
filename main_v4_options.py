import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_options_led_stock_sniper():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 精准搜索词：强制限定美股 (NASDAQ/NYSE)，彻底排除 ASX 等非美市场
    # 锁定：1月23日到期的异常 Call，小市值，以及下周的硬核利好
    query = "NASDAQ NYSE small-cap stocks unusual call volume Jan 23 2026 expiration, Vol/OI > 10, US stocks only upcoming FDA contract catalysts."
    
    print(f"📡 正在锁定美股市场（NASDAQ/NYSE）的期权异动标的...")
    search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

    # 2. 策略 Prompt：加入“美股唯一”指令和“负面过滤”
    prompt = f"""
    分析数据：{search_data}

    你现在的任务是：通过美股期权大单轨迹，定位下周（10天内）有爆发潜力的【美股正股】代码。
    
    🚫 强制剔除：
    - 非美国上市股票：绝对不要 ASX, LSE, TSX 等非美股代码。
    - 指数/大盘股：不要 QQQ, SPY, TSLA, NVDA 等。
    - 严重负面股：排除像 NVAX 这种被大行全线看空的票。

    ✅ 筛选准则：
    - 代码：仅限美股 Ticker。
    - 信号：必须有下周五（1月23日）到期的异常看涨单。
    - 催化剂：未来 10 天内有硬核利好（FDA、合同、增持）。

    输出表格：
    | 代码 | 当前价 | 下周爆发期权 (行权价) | Vol/OI 倍数 | 核心爆发原因 | 稳妥度 (1-5星) | 目标位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🎯"*15)
    print("🔥 美股波段爆发雷达 (10天狙击窗口) 🔥")
    print("🎯"*15)
    print(response.text)

if __name__ == "__main__":
    run_options_led_stock_sniper()
