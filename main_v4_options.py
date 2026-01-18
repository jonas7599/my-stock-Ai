import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 初始化
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_next_friday():
    """自动计算下周五的日期，用于期权到期日搜索"""
    today = datetime.date.today()
    days_ahead = 4 - today.weekday() # 4 是周五
    if days_ahead <= 0: # 如果今天就是周五或周末，计算下下周五
        days_ahead += 7
    return (today + datetime.timedelta(days_ahead)).strftime("%b %d %Y")

def run_options_led_stock_sniper():
    # 自动获取模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 动态生成搜索日期
    expiry_date = get_next_friday()
    
    # 2. 精准定义：中盘高弹性股，锁定 OKLO/SMCI 风格
    # 强调：Market Cap $2B-$50B，排除权重股 (Mega-caps)
    query = (
        f"NASDAQ NYSE liquid mid-cap stocks unusual call volume {expiry_date} expiration, "
        f"market cap between 2B and 50B USD, Vol/OI > 5, "
        f"stocks like OKLO, SMCI, RKLB, PLTR style high-momentum growth, "
        f"exclude TSLA NVDA AAPL MSFT."
    )
    
    print(f"📡 正在锁定【中盘高弹性美股】期权异动 (目标到期日: {expiry_date})...")
    
    try:
        search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

        # 检查搜索结果是否为空
        if not search_data.get('results'):
            print("⚠️ 今日未发现符合条件的期权异动信号。")
            return

        # 3. 策略 Prompt 优化
        prompt = f"""
        分析以下实时数据：{search_data}

        任务：定位未来 10 天内有爆发潜力的【中盘高弹性美股】。
        
        🚫 强制排除：
        - 市值过小 (<1B) 且无期权流动性的票。
        - 权重蓝筹股 (市值 > 2000B)：如 TSLA, NVDA, AAPL, MSFT 等。
        - 纯粹的非美市场代码 (ASX, LSE 等)。

        ✅ 目标画像：
        - 市值区间：20 亿 - 500 亿美元。
        - 风格：类似 OKLO, SMCI, MSTR, RKLB 等高波动、高杠杆效应的成长股。
        - 信号：重点关注 {expiry_date} 到期的异常 Call 单。

        如果没有符合上述条件的股票，请直接回答“今日无符合条件的弹性标的”。
        
        如果发现信号，请输出表格：
        | 代码 | 市值估计 | 当前价 | 异常期权 (行权价/{expiry_date}) | 异动倍数 | 爆发催化剂 | 信心指数 |
        """

        response = model.generate_content(prompt)
        
        # 4. 结果输出
        report_title = f"🔥 美股中盘爆发雷达 ({expiry_date} 狙击窗口) 🔥"
        print("\n" + "🎯"*15)
        print(report_title)
        print("🎯"*15)
        
        output = response.text.strip()
        if len(output) < 10 or "无符合条件" in output:
            print(f"报告日期: {datetime.date.today()}\n结论: 暂未发现符合条件的机构大单信号。")
        else:
            print(output)

    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    run_options_led_stock_sniper()
