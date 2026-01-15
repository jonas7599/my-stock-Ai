import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_momentum_strategy():
    # 自动获取 Gemini 模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 针对“次日连涨”的特定搜索词：锁定板块轮动和收盘强势股
    query = """
    US stock market sector rotation today, 
    top stocks closing at daily high with massive volume,
    stocks with strong after-hours gains and follow-through momentum
    """
    print(f"📡 正在扫描【次日连涨】潜力标的...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 核心 Prompt：要求 AI 识别上升通道和板块热度
    prompt = f"""
    分析以下实时数据：{search_data}

    你的目标是筛选出 5 只预计在【下一个交易日】大概率继续上涨的股票。
    必须符合以下“连涨”逻辑：
    1. 板块热度：处于当前资金轮动的热门板块（如 AI、能源、或特定利好行业）。
    2. 技术形态：处于清晰的上升通道，且今日收盘价接近全天最高位（无上影线）。
    3. 资金惯性：今日成交量异常放大，且盘后交易依然保持强势。
    4. 催化剂：有尚未完全消化的重大利好。

    输出格式：Markdown 表格
    股票代码 | 所属板块 | 连涨逻辑 (形态/利好/量价) | 压力位测算 | 推荐系数 (1-10)
    """

    response = model.generate_content(prompt)
    print("\n" + "🔥"*15)
    print("💎 次日连涨·五虎将预测 💎")
    print("🔥"*15)
    print(response.text)

if __name__ == "__main__":
    run_momentum_strategy()
