import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化 API 密钥
# 保持你原来的获取方式，确保在 GitHub Secrets 中已配置
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 自动获取最新模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # --- 关键修改：动态日期逻辑，解决你看到的“总出现周五”问题 ---
    # 自动获取当前日期。如果是周末，搜索指令会引导向最近的交易日（周五）
    today_date = datetime.date.today().strftime("%Y-%m-%d")

    # 2. 增强搜索词：强制要求具体的代码（Ticker）和真实成交量数据
    # 修正了搜索维度，让 AI 必须基于当天的真实市场异动来回答
    query = f"""
    US stock market activity and unusual volume spikes for {today_date}:
    1. Small-cap stocks ($1-$10) with highest relative volume and tight 2-week consolidation.
    2. Verifiable stock tickers breaking out from accumulation bases.
    3. Low float stocks with significant price action and real-time 8-K or mining news.
    Strictly focus on NYSE/NASDAQ real companies with current price/volume data.
    """

    print(f"🚀 正在执行深度扫描: 锁定【低位吸筹+潜在爆发】标的 (分析日期: {today_date})...")
    
    # 使用高级搜索获取详细信息
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 强化 Prompt：明确要求填充代码和硬性交易指标，杜绝虚假信息
    # 这里的逻辑对标你截图中的 TGB 模型：高筹码获利比、放量突破
    prompt = f"""
    分析以下实时市场数据: {search_data}

    你的任务是找出 5 只真正处于“启动前夜”的真实美股。

    ### 严格执行准则（负责任的修改）：
    1. **拒绝幻觉**：严禁编造代码（如 AIXD, LFLT, NVTX 均为错误示例）。如果搜索数据中没有确切的今日股价，严禁输出。
    2. **对标 TGB 模型**：优先选择筹码高度集中（获利比例 > 80%）、经历 2 周以上窄幅横盘、且今日成交量异常放大的标的。
    3. **动态验证**：所有数据必须对应 {today_date} 或最近交易日的真实值。
    4. **质量优先**：如果不符合标准的股票不足 5 只，只输出真实的即可。

    请严格按以下表格格式输出：
    | 代码 | 行业板块 | 吸筹阶段 (初期/末期) | 换手/量能特征 | 关键催化剂 | 埋伏参考价 | 止损参考 | 逻辑简述 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    # 获取 AI 生成内容
    response = model.generate_content(prompt)

    print("\n" + "🎯" * 15)
    print(f"💎 点火猎人·吸筹启动监控 (分析时间: {today_date}) 💎")
    print("🎯" * 15)
    print(response.text)

if __name__ == "__main__":
    run_accumulation_hunter = run_ignition_hunter # 兼容性处理
    run_ignition_hunter()
