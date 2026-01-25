import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化（从环境变量读取 KEY，确保安全性）
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 保持使用你要求的现有模型
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 动态日期逻辑：确保扫描的是最新交易日
    today = datetime.date.today()
    target_date = today if today.weekday() < 5 else today - datetime.timedelta(days=today.weekday() - 4)
    date_str = target_date.strftime("%Y-%m-%d")

    # 2. 策略搜索指令 (Query)：
    # 严格按照：全行业、小市值($1-$50)、横盘整理(Consolidation)、吸筹异动(Accumulation/Volume spike)、利好新闻
    query = f"""
    Comprehensive US stock market scan for {date_str}:
    1. Focus on small-cap stocks ($1-$50, Market Cap < $2B) from ANY industry.
    2. Identify tickers in a tight 2-4 week consolidation base with declining volume (VCP).
    3. Spot signs of stealth accumulation: OBV rising or volume spikes (>2x avg) while price is relatively flat.
    4. Must have major recent news (FDA, contracts, earnings, partnerships) within 48h.
    List the top 10 potential breakout candidates.
    """

    print(f"🚀 正在执行全行业策略扫描 (分析日期: {date_str})...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 策略分析指令 (Prompt)：
    # 强制 AI 按照“吸筹逻辑”进行二次过滤，并按你要求的格式输出
    prompt = f"""
    分析以下实时数据：{search_data}

    任务：从全行业中找出 5 只【真实存在】且在 {date_str} 表现出“吸筹结束、准备启动”特征的美股。

    ### 筛选核心逻辑：
    1. **横盘整理**：股价近期波动极小，处于窄幅箱体。
    2. **吸筹特征**：价格还未暴涨，但成交量已经出现明显异动（机构悄悄进场）。
    3. **市值/价格**：市值小于 20 亿美金，股价在 $1 到 $50 之间。
    4. **利好催化**：必须有具体的利好新闻（如合同、财报、产品进展等）。

    ### 严格执行原则：
    1. 覆盖全行业：不要只盯着科技股，关注工业、能源、消费等所有板块。
    2. 拒绝幻觉：代码必须真实存在。
    3. 格式要求：严禁任何解释性文字，直接输出以下表格。

    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    # 生成分析结果
    response = model.generate_content(prompt)

    # 4. 输出结果
    print(f"\n🎯 全行业点火猎人·实时扫描报告 ({date_str}) 🎯")
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
