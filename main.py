import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 1. 自动模型匹配
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 2. 策略 A 搜索：今日强势股
    query_a = "US small-cap top gainers volume breakout today"
    data_a = tavily.search(query=query_a, search_depth="advanced")

    # 3. 策略 B 搜索：全维度利好（整合增持、收购、临床、PDUFA、SEC公告）
    # 使用精简关键词，严格控制在 400 字符内，避免 BadRequestError
    query_b = "US stocks: SEC Form 4 insider buying, 8-K major events, FDA PDUFA date, clinical results, M&A rumors"
    print(f"📡 扫描全维度利好：高管增持、并购、FDA、研发进展及 SEC 公告...")
    data_b = tavily.search(query=query_b, search_depth="advanced")

    # 4. 深度融合 Prompt
    prompt = f"""
    分析以下实时数据：
    策略A数据: {data_a}
    策略B数据: {data_b}

    请执行双策略分析，并重点挖掘【策略 B】中未启动的黑马：

    ---
    ### 🚀 策略 A：【动能爆发型】（已确认启动）
    - 聚焦：今日放量异动、价格处于高位、利好已证实。
    输出：代码 | 行业 | 利好解析 | 综合评分 | 操作建议

    ---
    ### 💎 策略 B：【拐点埋伏型】（全维度利好潜伏）
    - 必须涵盖：高管大额增持(SEC Form 4)、重大合同或并购(8-K)、二/三期临床进度、新药 PDUFA 预期。
    - 状态筛选：识别低位缩量、底座抬高、价格尚未反应利好的标的。
    输出表格：代码 | 埋伏理由 (增持/收购/临床/PDUFA/合同) | 关键日期/催化剂 | 准备度(1-10) | 建议买入区间
    """

    response = model.generate_content(prompt)
    print("\n" + "🏆"*15)
    print("💎 全利好维度·双策略深度报告 💎")
    print("🏆"*15)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
