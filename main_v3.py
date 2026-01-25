import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化（从 GitHub Secrets 获取）
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 自动获取最新模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 动态日期逻辑：确保扫描的是最新交易日，解决“死守周五”问题
    today = datetime.date.today()
    # 如果是周末，自动找上周五；平日则找当天或前一天
    target_date = today if today.weekday() < 5 else today - datetime.timedelta(days=today.weekday() - 4)
    date_str = target_date.strftime("%Y-%m-%d")

    # 2. 修改后的【全行业】搜索指令：严禁限定行业，严禁提及具体股票
    query = f"""
    Comprehensive US stock market scan for {date_str}:
    1. Identify all small-cap stocks ($1-$10) from ANY industry with unusual volume spikes.
    2. Find tickers breaking out from a 2-week consolidation base with high relative volume.
    3. Look for stocks with significant after-hours price action or major news (8-K, earnings).
    Focus on the top 10 most significant accumulation breakouts across the entire market.
    """

    print(f"📡 正在执行全行业扫描 (分析日期: {date_str})...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 强化 Prompt：明确要求“全行业”，严禁“模式化”，严禁幻觉
    prompt = f"""
    分析以下实时数据: {search_data}
    
    任务：从全行业中找出 5-10 只【真实存在】且在 {date_str} 表现出“吸筹结束、准备启动”特征的美股。
    
    ### 严格执行原则：
    1. 覆盖全行业：严禁只关注特定板块（如矿产或科技）。只要符合异动标准，全行业均可入选。
    2. 拒绝幻觉：代码必须真实存在且能搜到 {date_str} 的真实成交数据。严禁编造不存在的代码！
    3. 拒绝预设模式：不要参考任何历史案例，只根据【当前数据】中的量价异动、获利筹码和新闻催化剂进行判断。
    4. 数量要求：找出表现最强、逻辑最硬的 5-10 个标的。
    
    请严格按以下格式输出（严禁在正文外加废话）：
    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)

    print(f"\n🎯 全行业点火猎人·实时扫描报告 ({date_str}) 🎯")
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
