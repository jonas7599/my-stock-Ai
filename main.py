import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 自动获取并兼容可用的 Gemini 模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 策略 A 搜索：捕捉今日已爆发的强势股（动能追涨）
    query_a = "US small-cap stocks top gainers today, massive volume breakout, breakout after earnings or FDA approval"
    data_a = tavily.search(query=query_a, search_depth="advanced")

    # 2. 策略 B 搜索：全维度利好埋伏（新药/研发/增持/收购/合同）
    # 关键词涵盖：高管增持(insider buying)、收购(acquisition)、新药发售(product launch)、研发成果(clinical trial results)、重大合同(major contract)
    query_b = """
    US small-cap stocks with: 
    1. Significant insider buying or stock buyback.
    2. Upcoming FDA PDUFA dates or major clinical trial phase 2/3 results.
    3. New product launch or major government/tech contract awards.
    4. Merger and acquisition (M&A) rumors or definitive agreements.
    5. Stocks with low-volume consolidation before major catalysts.
    """
    print(f"📡 正在深度扫描全行业利好：包含研发成果、新药发售、高管增持及收购预期...")
    data_b = tavily.search(query=query_b, search_depth="advanced")

    # 3. 策略拆分分析 Prompt
    prompt = f"""
    你是顶级量化分析师。请分析以下实时抓取的数据：
    策略A数据: {data_a}
    策略B数据: {data_b}

    请根据以下两套独立策略进行筛选，并确保覆盖金融、医药、科技、半导体等全行业：

    ---
    ### 策略 A：【动能追涨型】（已爆发，看持续性）
    标准：今日放量突破、价格处于高位、利好已证实。
    输出：代码 | 所属行业 | 硬核利好解析 | 综合评分 | 操作建议

    ---
    ### 策略 B：【拐点埋伏型】（未爆发，看潜伏价值）
    标准：
    - 信号：高管大额增持、公司收购预期、即将到来的新药发售、研发成果发布或大额合同。
    - 状态：缩量横盘或底座抬高，价格尚未暴涨。
    输出：代码 | 埋伏理由 (增持/收购/研发/新药/合同) | 关键日期/催化剂 | 准备就绪度(1-10) | 建议买入区间
    """

    response = model.generate_content(prompt)
    print("\n" + "🚀"*15)
    print("💎 全维度硬核利好双策略分析报告 💎")
    print("🚀"*15)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
