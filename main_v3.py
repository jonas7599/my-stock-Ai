import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 自动模型匹配（修复 404 错误）
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

    # 动态日期
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # 策略 A：今日强势股 (精简关键词，避免 400 字符报错)
    query_a = f"US small-cap top gainers volume breakout {date_str}"
    data_a = tavily.search(query=query_a, search_depth="advanced")

    # 策略 B：全维度利好（横盘吸筹+催化剂）
    # 使用精简关键词：SEC增持、FDA、M&A、新合同
    query_b = f"US stocks SEC Form 4 insider buying FDA PDUFA clinical M&A news {date_str}"
    print(f"🚀 正在扫描全维度利好: 高管增持、并购、FDA、研发进展及 SEC 公告...")
    data_b = tavily.search(query=query_b, search_depth="advanced")

    # 4. 深度融合 Prompt (严格执行横盘吸筹逻辑)
    prompt = f"""
    分析以下实时数据：
    策略A数据: {data_a}
    策略B数据: {data_b}

    请执行双策略分析，并重点挖掘【策略 B】中未启动的黑马标的。

    ### 筛选硬指标：
    1. **小市值策略**：股价 $1-$50，市值 < 20亿美金。
    2. **横盘吸筹态势**：识别低位缩量、底座抬高、价格尚未反应利好的标的。
    3. **必选覆盖**：高管大额增持(Form 4)、重大合同或并购(8-K)、二/三期临床进度。

    请严格按以下格式输出表格（不要任何开场白）：

    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    # 生成分析结果
    response = model.generate_content(prompt)

    print("\n" + "💎"*15)
    print("💎 全利好维度·双策略深度报告 💎")
    print("💎"*15)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
