import os
import datetime
from google import genai
from tavily import TavilyClient

# 初始化新版客户端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_next_friday():
    """自动获取最近的周五合约日期"""
    today = datetime.date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0: days_ahead += 7
    return (today + datetime.timedelta(days_ahead)).strftime("%b %d %Y")

def run_options_led_stock_sniper():
    expiry_date = get_next_friday()
    
    # 搜索策略：股价硬限 $100 以下，锁定异动标的
    query = (
        f"US stocks NASDAQ NYSE unusual call options volume for {expiry_date} expiration, "
        f"current price under $100 USD, Vol/OI > 5, "
        f"focus on OKLO, SMCI, RKLB, IONQ, LUNR."
    )
    
    print(f"📡 正在扫描 $100 以下美股异动 (目标合约: {expiry_date})...")
    
    try:
        # 获取实时数据
        search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

        # 任务指令：排除所有高价股，锁定爆发逻辑
        prompt = f"""
        分析数据：{search_data}

        任务：找出符合条件的爆发股。
        
        ⛔ 强制过滤：
        1. 股价必须在 $5 到 $100 之间（超过 $100 直接剔除）。
        2. 必须是美股 Ticker。

        ✅ 核心重点：
        - 筛选 {expiry_date} 到期的异常 Call 单。
        - 寻找未来 10 天内有硬核催化剂（合同、并购、FDA）的标的。

        输出表格：
        | 代码 | 股价 | 市值 | 异动期权({expiry_date}) | Vol/OI | 爆发逻辑 | 信心指数 |
        | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
        """

        # 调用新版 API
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        print("\n" + "🎯"*15)
        print(f"🔥 美股期权异动雷达 (价格上限: $100) 🔥")
        print("🎯"*15)
        print(response.text.strip())

    except Exception as e:
        print(f"❌ 运行失败: {str(e)}")

if __name__ == "__main__":
    run_options_led_stock_sniper()
