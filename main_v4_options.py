import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_options_led_stock_sniper():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 精简搜索词：只搜小市值期权异动 + 短期催化剂
    query = "Small-cap stocks unusual call volume Jan 23 2026 expiration, Vol/OI ratio > 5, upcoming FDA catalysts Jan 2026, major contract wins small caps."
    
    print(f"📡 正在通过期权大单轨迹扫描【下周爆发】正股...")
    search_data = tavily.search(query=query, search_depth="advanced", max_results=15)

    # 2. 策略 Prompt：强制要求 AI 用期权逻辑选正股
    prompt = f"""
    分析数据：{search_data}

    你现在的身份是：利用期权异动定位正股机会的专家。请选出 8 只下周（10天内）具备爆发潜力的股票。
    
    🚨 过滤规则：
    - 禁出名单：TSLA, NVDA, AAPL, QQQ, SPY, IWM (不碰大盘和指数)。
    - 硬核门槛：市值 < 500亿，必须有下周到期的异常看涨大单。
    - 安全性：排除负面新闻缠身的票 (如 NVAX)。

    请输出表格：
    | 代码 | 当前价 | 期权异动 (行权价/下周到期) | Vol/OI 倍数 | 核心爆发原因 (FDA/合同/挤压) | 稳妥度 (1-5星) | 目标位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🎯"*15)
    print("🔥 期权异动导航：波段爆发正股清单 (10天窗口) 🔥")
    print("🎯"*15)
    print(response.text)

if __name__ == "__main__":
    run_options_led_stock_sniper()
