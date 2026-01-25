import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化 API 密钥 (确保你在 GitHub Secrets 中已设置)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 自动模型匹配：解决 models/gemini-1.5-flash 404 报错问题
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
        model = genai.GenerativeModel(target_model)
    except Exception:
        model = genai.GenerativeModel('gemini-1.5-flash')

    # 获取动态日期
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # 2. 策略 A 搜索：今日强势股 (精简关键词，避免 400 字符报错)
    query_a = f"US small-cap top gainers volume breakout {date_str}"
    data_a = tavily.search(query=query_a, search_depth="advanced")

    # 3. 策略 B 搜索：全维度利好 (寻找横盘吸筹黑马)
    # 聚焦关键词：高管增持、SEC 合同、FDA 进展、并购传闻
    query_b = f"US stocks SEC Form 4 insider buying, 8-K major contracts, FDA PDUFA date, M&A rumors {date_str}"
    print(f"🚀 正在扫描：高管增持、重大合同、研发进展及 SEC 异动公告...")
    data_b = tavily.search(query=query_b, search_depth="advanced")

    # 4. 深度融合 Prompt：严格执行横盘吸筹筛选逻辑
    prompt = f"""
    分析以下实时数据：
    策略A数据 (已启动): {data_a}
    策略B数据 (潜在黑马): {data_b}

    任务：请从数据中挖掘 5 只符合“吸筹结束、利好待发”特征的小市值美股（$1-$50，市值<$20亿）。

    ### 筛选硬指标：
    1. **横盘缩量态势**：重点识别过去 2-4 周价格极度紧致（横盘）、成交量枯竭后开始温和放量的标的。
    2. **未启动利好**：筛选有利好（如大额增持、新合同、临床数据）但价格尚未暴涨的黑马。
    3. **全行业覆盖**：不限行业，严禁幻觉。

    ### 严格输出格式（严禁任何开场白，直接输出表格）：
    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    # 生成分析结果
    response = model.generate_content(prompt)

    print("\n" + "💎"*15)
    print(f"💎 全利好维度·双策略深度报告 ({date_str}) 💎")
    print("💎"*15)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
