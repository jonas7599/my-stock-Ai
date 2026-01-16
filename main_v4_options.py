import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_short_term_burst_sniper():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 广谱利好扫描：加入空头挤压、内幕增持、重大合同、突发收购传闻等
    query = """
    US stock market high-conviction catalysts Jan 16-26, 2026:
    1. Upcoming FDA PDUFA, clinical data readouts, or patent approvals.
    2. Anticipated earnings pre-announcements or massive contract awards (Government/Big Tech).
    3. High short-interest stocks (SI > 20%) with new positive news or volume spikes.
    4. SEC Form 4 significant insider buying in small-cap companies this week.
    5. Stocks consolidating near support with massive short-term call sweeps (expiring next 10 days).
    """
    
    print(f"📡 正在全方位扫描“硬核利好”：锁定 2-10 天内具备爆发基因的波段标的...")
    search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

    # 2. 策略 Prompt：要求 AI 给出“爆发逻辑”和“稳妥程度”
    prompt = f"""
    分析数据：{search_data}

    作为职业波段交易员，请从数据中提取 8-10 只具备【下周爆发潜力】的个股。
    
    筛选准则（硬核）：
    - 催化剂时效：利好必须在未来 2-10 天内兑现或发酵。
    - 资金面：期权成交量（Vol）必须远大于持仓量（OI），且到期日极短。
    - 排除项：排除涨幅已超过 50% 的追高票，寻找 OKLO 式的“横盘+突发异动”模型。

    请严格按此表格输出：
    | 代码 | 当前价 | 催化剂类型 (合同/FDA/财报/空头挤压/内幕) | 关键日期 | 期权异动 (价位/下周到期) | 爆发概率 (1-5星) | 目标位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🚀"*15)
    print("🔥 全能利好·短期爆发雷达 (波段精选) 🔥")
    print("🚀"*15)
    print(response.text)

if __name__ == "__main__":
    run_short_term_burst_sniper()
