import os
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_options_intelligence():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 组合搜索：锁定具体价位、最大痛点和庄家建仓位置
    # 增加对 BTON, KALA 等你关注标的的针对性扫描
    query = """
    Latest unusual options activity for small-cap stocks: 
    1. Highest Open Interest call/put strikes for BTON, KALA, SOWG.
    2. Unusual bull sweeps and deep-in-the-money call buying today.
    3. Option Max Pain levels and Gamma walls for upcoming Jan 2026 expirations.
    4. Market maker hedging levels for trending tickers.
    """
    print(f"📡 正在抓取期权市场核心价位：搜索大单路径、最大痛点及多头防御区...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 强化 Prompt：强制 AI 计算“引力区”
    prompt = f"""
    分析数据：{search_data}

    作为顶级期权交易员，请解码庄家在期权市场留下的痕迹。
    
    重点输出：
    - 哪些行权价（Strike）正在被大量扫货？
    - 股价的“磁铁区”：最大持仓量（OI）聚集在哪里？
    - 压力位：看涨期权（Call）密集的防御线。

    请严格按此表格输出：
    | 代码 | 当前价预测 | 核心行权价(到期日) | 期权信号类型 (大单/扫货/OI集中) | 多头引力区 (目标价) | 空头防线 (强压力) | 庄家成本暗示 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🔥"*15)
    print("💎 期权链价位预测 & 庄家动向 💎")
    print("🔥"*15)
    print(response.text)

if __name__ == "__main__":
    run_options_intelligence()
