import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_short_term_burst_sniper():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 精简搜索词：必须低于 400 字符以防 API 报错
    # 聚焦：下周到期期权、Vol/OI异动、10天内利好(FDA/合同/挤压)
    query = "US stocks unusual options Jan 2026, high Vol/OI ratio small cap, upcoming FDA PDUFA Jan 16-26, short squeeze tickers, new large government contract awards."
    
    print(f"📡 正在捕捉 2-10 天内爆发信号 (已修复 API 长度限制)... ")
    # search_depth="advanced" 消耗 2 积分，但数据更准
    search_data = tavily.search(query=query, search_depth="advanced", max_results=15)

    # 2. 策略 Prompt：要求 AI 严格筛选短期确定性
    prompt = f"""
    分析数据：{search_data}

    你现在是短线狙击手。请精选 8 只【10天内必有大动作】的稳妥标的。
    
    筛选准则：
    - 催化剂：利好（FDA、财报、合同、挤压）必须在 2-10 天内兑现。
    - 异动：只选下周五到期且 Vol/OI > 5 的期权。
    - 形态：寻找 OKLO 式“低位横盘+突然点火”模型。

    输出表格：
    | 代码 | 当前价 | 催化剂 (类型/日期) | 爆发期权 (价位/下周到期) | Vol/OI 异动 | 稳妥度 (1-5星) | 目标位 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🚀"*15)
    print("🔥 短线波段·全能爆发雷达 (修复版) 🔥")
    print("🚀"*15)
    print(response.text)

if __name__ == "__main__":
    run_short_term_burst_sniper()
