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

    # 2. 策略 A 搜索：今日已爆发强势股
    query_a = "US small-cap top gainers today volume breakout positive news"
    data_a = tavily.search(query=query_a, search_depth="advanced")

    # 3. 策略 B 搜索：全维度深度潜伏（拆分为短句，避免字符过长报错）
    # 涵盖：增持(Form 4)、收购、研发成果(Phase 2/3)、新药发售(PDUFA)、重大合同
    query_b = "US stocks: SEC Form 4 insider buying, M&A rumors, Phase 2/3 clinical results, PDUFA dates, major contract awards"
    print(f"📡 正在执行全维度扫描：增持、收购、研发成果及新药发售...")
    data_b = tavily.search(query=query_b, search_depth="advanced")

    # 4. 融合版分析 Prompt
    prompt = f"""
    分析以下实时抓取的数据：
    策略A数据: {data_a}
    策略B数据: {data_b}

    请按照【动能爆发型】和【拐点埋伏型】输出两份报告，覆盖全行业：

    ---
    ### 🚀 策略 A：【动能爆发型】（已爆发）
    - 要求：量价齐升，利好已证实。
    输出表格：代码 | 行业 | 爆发催化剂 | 综合评分 | 操作建议

    ---
    ### 💎 策略 B：【拐点埋伏型】（未爆发/筹码收集期）
    - 必须包含：高管增持细节、临床进度(Phase 2/3)、预计利好日期或收购传闻。
    - 状态：识别低位缩量横盘或底座抬高形态。
    输出表格：代码 | 埋伏理由 (增持/收购/研发/新药/合同) | 关键日期/催化剂 | 准备就绪度(1-10) | 建议埋伏区间
    """

    response = model.generate_content(prompt)
    print("\n" + "⚡"*15)
    print("🏆 全维度【动能+潜伏】深度报告 🏆")
    print("⚡"*15)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
