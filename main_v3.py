import os
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化 API 密钥
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 自动获取当前最强模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 2. 增强搜索词：强制要求具体的代码 (Ticker) 和盘后异动数据
    # 针对你之前遇到的“只有公司名”问题，这里明确了搜索范围
    query = """
    US stock market today: 
    1. Small-cap stocks with unusual volume spikes and high accumulation.
    2. Specific stock tickers for breakout from consolidation base.
    3. Biotech stocks with FDA PDUFA dates in Jan/Feb 2026.
    4. Low float stocks with significant after-hours price action.
    """
    
    print(f"📡 正在执行深度扫描：锁定【低位吸筹+潜在爆发】标的...")
    # 使用高级搜索以获取更详细的市场信息
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 强化 Prompt：明确要求填充代码和硬性交易指标
    prompt = f"""
    分析以下实时数据：{search_data}

    你的任务是找出 5 只正处于“启动前夜”的股票。
    
    筛选标准：
    - 筹码锁定：股价在窄幅区间波动超过 2 周。
    - 启动信号：换手率开始缓慢放大，委比买盘明显增强。
    - 逻辑：有未公开或即将到来的重大催化剂（如 8-K 文件、FDA 审批、财报预增）。

    请严格按以下表格输出（如果数据缺失，请根据搜索内容中的线索给出最合理的预估）：
    | 代码 | 行业板块 | 吸筹阶段 (初期/末期) | 换手/量能特征 | 关键催化剂 (日期) | 埋伏参考价 | 止损参考 | 逻辑简述 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    
    print("\n" + "🎯"*15)
    print("💎 点火猎人·吸筹启动监控 (分析时间: 2026-01-15) 💎")
    print("🎯"*15)
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
