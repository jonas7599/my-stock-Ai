import os
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化（确保你的 Secrets 中已配置这些 Key）
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_short_term_burst_sniper():
    # 自动选择最强的 Flash 模型以保证分析速度
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 2. 扩谱搜索：锁定未来 2-10 天内的【所有】硬核催化剂
    query = """
    High-impact stock catalysts scheduled for Jan 16-26, 2026:
    1. FDA PDUFA dates (e.g., Aquestive AQST Jan 31, Tenpoint Jan 28) and clinical trial readouts.
    2. Significant contract awards from Dept of Defense or Big Tech (similar to OKLO/SHIELD awards).
    3. Small-cap stocks with Short Interest > 20% showing unusual call sweeps today.
    4. SEC Form 4 insider buying (> $100k) in companies trading near support levels.
    5. Stocks with massive Vol/OI spikes on next Friday's expiration (Jan 23, 2026).
    """
    
    print(f"📡 正在捕捉 2-10 天内的全能利好信号：排除干扰，锁定波段爆发点...")
    search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

    # 3. 策略 Prompt：要求 AI 像操盘手一样筛选“最稳”的爆发票
    prompt = f"""
    分析以下实时市场数据：{search_data}

    作为顶级短线波段专家，请精选 8-10 只【下周有极高爆发概率】的个股。
    
    筛选准则（硬核）：
    - 时效性：利好事件必须在未来 2-10 天内发生。
    - 异动性：期权成交量（Vol）必须远大于持仓量（OI），且到期日就在下周。
    - 稳健型：模仿 OKLO 启动前，优先选择低位横盘、未被大幅拉升的标的。
    - 催化剂：包括但不限于 FDA、重大合同、空头挤压、内幕大额买入、财报预增。

    请严格按此表格输出：
    | 代码 | 当前价 | 催化剂类型 (合同/FDA/挤压/内幕/财报) | 爆发日 (2-10天内) | 期权异动 (价位/下周到期) | 爆发概率 (1-5星) | 波段目标位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🚀"*15)
    print("🔥 全能利好·短期爆发雷达 (波段精选) 🔥")
    print("🚀"*15)
    print(response.text)

if __name__ == "__main__":
    run_short_term_burst_sniper()
