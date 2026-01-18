import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 初始化
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_next_friday():
    """计算下周五到期日"""
    today = datetime.date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0: days_ahead += 7
    return (today + datetime.timedelta(days_ahead)).strftime("%b %d %Y")

def run_options_led_stock_sniper():
    # 直接指定模型，防止 Actions 环境下 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    expiry_date = get_next_friday()
    
    # 搜索逻辑：价格死锁 $100 以下，锁定 NASDAQ/NYSE 期权异动
    query = (
        f"US stocks NASDAQ NYSE unusual call options volume {expiry_date} expiration, "
        f"stock price under $100 USD, Vol/OI > 5, "
        f"focus on OKLO, SMCI, RKLB, IONQ, LUNR."
    )
    
    print(f"📡 正在扫描 $100 以下美股异动 (目标合约: {expiry_date})...")
    
    try:
        search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

        prompt = f"""
        分析数据：{search_data}

        任务：找出符合条件的爆发股。
        
        🚫 强制过滤：
        1. 股价必须在 $5 到 $100 之间（超过 $100 直接剔除）。
        2. 必须是美股 Ticker。

        ✅ 核心重点：
        - 筛选 {expiry_date} 到期的异常 Call 单。
        - 寻找未来 10 天内的硬核利好（合同、数据发布、并购）。

        输出表格：
        | 代码 | 股价 | 市值 | 异动期权({expiry_date}) | Vol/OI | 爆发逻辑 | 信心指数 |
        | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
        """

        response = model.generate_content(prompt)
        print("\n" + "🎯"*15)
        print(f"🔥 美股期权异动雷达 (价格上限: $100) 🔥")
        print("🎯"*15)
        print(response.text.strip())

    except Exception as e:
        print(f"❌ 运行故障: {e}")

if __name__ == "__main__":
    run_options_led_stock_sniper()
