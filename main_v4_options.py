import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_next_friday():
    today = datetime.date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0: days_ahead += 7
    return (today + datetime.timedelta(days_ahead)).strftime("%b %d %Y")

def run_options_led_stock_sniper():
    model = genai.GenerativeModel('gemini-1.5-flash')
    expiry_date = get_next_friday()
    
    # 核心策略：价格硬限 $100 以下，不限市值，锁定近期到期 Call 异动
    query = (
        f"US stocks NASDAQ NYSE unusual call options volume for {expiry_date} expiration, "
        f"current stock price under $100 USD, Vol/OI > 5, "
        f"focus on high momentum stocks like OKLO, SMCI, RKLB, IONQ, LUNR, "
        f"exclude expensive stocks over $100."
    )
    
    print(f"📡 正在扫描 $100 以下美股期权异动 (目标日: {expiry_date})...")
    
    try:
        search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

        prompt = f"""
        分析数据：{search_data}

        任务：筛选符合条件的爆发潜力股。
        
        ⛔ 强制排除：
        1. 股价高于 $100 的任何股票。
        2. 非美股代码。

        ✅ 筛选准则：
        - 价格：$5 - $100 之间。
        - 信号：重点筛选 {expiry_date} 到期的异常 Call 单。
        - 催化剂：寻找未来 10 天内的利好事件。

        输出表格：
        | 代码 | 股价 | 市值 | 期权异动({expiry_date}) | Vol/OI | 核心逻辑 | 信心指数 |
        | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
        """

        response = model.generate_content(prompt)
        output = response.text.strip()

        print("\n" + "🎯"*15)
        print(f"🔥 美股期权异动雷达 (价格限额: <$100) 🔥")
        print("🎯"*15)
        
        if "无符合" in output or len(output) < 20:
            print(f"结论: 今日未发现 $100 以下符合期权爆发条件的标的。")
        else:
            print(output)

    except Exception as e:
        print(f"❌ 运行故障: {e}")

if __name__ == "__main__":
    run_options_led_stock_sniper()
