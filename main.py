import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 1. 自动获取并兼容可用的 Gemini 模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 2. 策略 A 搜索：今日已爆发的强势股（维持原有的动能抓取）
    query_a = "US small-cap stocks top gainers today, volume breakout, positive earnings surprise or FDA approval news"
    data_a = tavily.search(query=query_a, search_depth="advanced")

    # 3. 策略 B 搜索：深度融合扫描（实时利好 + AI 建议的 SEC/临床细节）
    # 结合了：高管增持(SEC Form 4)、重大公告(8-K)、临床Phase 2/3、收购预期、新药PDUFA日期
    query_b = """
    Search for US small-cap stocks with:
    1. Recent SEC Form 4 insider buying (large amounts) or Form 8-K major event filings.
    2. Upcoming FDA PDUFA dates or Phase 2/3 clinical trial result announcements in the next 3 months.
    3. New product launch plans, major tech/defense contract awards, or M&A rumors/agreements.
    4. Analyst upgrades based on fundamental 'inflection points' or R&D breakthroughs.
    5. Stocks showing 'accumulation' patterns: price consolidation with occasional volume spikes.
    """
    print(f"📡 正在执行【全维度深度扫描】：结合 SEC 文件、临床进度、高管增持及并购预期...")
    data_b = tavily.search(query=query_b, search_depth="advanced")

    # 4. 融合版分析 Prompt
    prompt = f"""
    你现在是一名顶级机构量化分析师。请结合以下【实时新闻】与【深度公告数据】进行交叉分析：
    策略A原始数据: {data_a}
    策略B原始数据: {data_b}

    请输出两份专业报告，要求涵盖金融、生物医药、硬科技等全行业：

    ---
    ### 🚀 策略 A：【动能爆发型】（今日已确认启动）
    - 要求：量价齐升，利好已公开化，抓取主升浪持续性。
    输出表格：代码 | 行业 | 爆发催化剂 (财报/FDA/合同) | 综合评分 | 操作建议

    ---
    ### 💎 策略 B：【拐点埋伏型】（未爆发/筹码收集期）
    - 融合要求：必须包含“高管增持数据(SEC)”、“临床阶段详情”、“预计利好日期”或“收购预期”。
    - 状态：识别缩量横盘或底座抬高形态，单价未脱离成本区。
    输出表格：代码 | 埋伏理由 (增持细节/临床进度/收购传闻) | 关键催化剂日期 | 准备就绪度(1-10) | 建议埋伏区间
    """

    response = model.generate_content(prompt)
    print("\n" + "⚡"*20)
    print("🏆 全维度【动能+潜伏】深度分析报告 🏆")
    print("⚡"*20)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
