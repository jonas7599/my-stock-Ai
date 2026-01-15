import os
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化 API 密钥 (确保你在 GitHub Secrets 中已设置)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_momentum_prediction():
    # 自动获取当前最强的 Flash 模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 2. 精准搜索：锁定板块轮动、强势收盘、SEC公告及盘后异动
    # 关键词涵盖：高管增持(SEC Form 4)、重大合同(8-K)、临床Phase 2/3、新药PDUFA日期
    query = """
    US stock market today: top gainers with massive volume, closing at highs, 
    strong after-hours movers, SEC Form 4 insider buying, major 8-K filings, 
    and upcoming FDA PDUFA or clinical trial results Jan 2026.
    """
    print(f"📡 正在执行全维度扫描：锁定【次日连涨·五虎将】并测算点位...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 深度分析 Prompt：强制输出三级买卖点表格
    prompt = f"""
    分析以下实时市场数据：{search_data}

    作为顶级券商量化师，请筛选出 5 只预计在【次日及短期内】具有极强上涨惯性的股票。
    
    筛选逻辑：
    - 形态：处于上升通道，今日收盘接近最高位，盘后继续走强。
    - 筹码：有高管大额增持、重组并购传闻或重大研发突破。
    - 动能：属于当前 AI、能源、或医药等资金流入最猛的板块。

    请严格按以下 Markdown 表格格式输出：
    | 代码 | 所属行业 | 建议入场区间 | 短期卖出点(1-3d) | 中期卖出点(1-2w) | 后期/格局位 | 关键止损位 | 连涨核心逻辑 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    
    注意：点位需基于当前股价、支撑位与压力位进行测算。
    """
    
    response = model.generate_content(prompt)
    
    print("\n" + "🔥"*15)
    print(f"💎 次日连涨·五虎将深度报告 (2026-01-15) 💎")
    print("🔥"*15)
    print(response.text)

if __name__ == "__main__":
    run_momentum_prediction()
