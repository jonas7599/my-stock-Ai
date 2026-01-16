import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API 密钥
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_short_term_burst_sniper():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 扩谱搜索：锁定未来 2-10 天内的【所有】硬核催化剂
    query = """
    Identify US stocks with high-impact catalysts scheduled between Jan 16 - Jan 26, 2026:
    1. FDA PDUFA action dates (e.g., Aquestive AQST PDUFA Jan 31, Tenpoint Jan 28).
    2. Major government contract awards (e.g., MDA SHIELD contracts) or Big Tech partnership leaks.
    3. High Short Interest stocks (SI > 20%) with new bullish news or massive volume.
    4. Significant SEC Form 4 insider buys (> $100k) occurring at support levels.
    5. Options activity: Stocks with Vol/OI ratio > 10 on nearest Friday expiration.
    """
    
    print(f"📡 正在捕捉 2-10 天内的全能利好信号：排除干扰，锁定波段爆发点...")
    search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

    # 2. 策略 Prompt：强化“稳妥爆发”逻辑
    prompt = f"""
    分析数据：{search_data}

    作为顶级短线交易员，请精选 8-10 只【下周有极高爆发概率】的稳妥个股。
    
    筛选准则（硬核）：
    - 时效性：利好事件必须在未来 2-10 天内发生。
    - 异动性：期权成交量（Vol）必须远大于持仓量（OI），且到期日就在下周。
    - 稳健型：模仿 OKLO 启动前，优先选择低位横盘、未被大幅拉升、有强支撑的标的。
    - 催化剂类型：包括 FDA 审批、重大合同、空头挤压、内幕买入、财报预增。

    请严格按此表格输出：
    | 代码 | 当前价 | 催化剂类型 (合同/FDA/挤压/内幕/财报) | 爆发窗口 (日期) | 期权异动 (价位/下周到期) | 爆发概率 (1-5星) | 目标位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🚀"*15)
    print("🔥 全能利好·短期爆发雷达 (波段精选) 🔥")
    print("🚀"*15)
    print(response.text)

if __name__ == "__main__":
    run_short_term_burst_sniper()
