import os
import datetime
import time
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
    
    # 策略核心：股价硬限 $100 以下，不限市值
    query = (
        f"US stocks NASDAQ NYSE unusual call options volume for {expiry_date} expiration, "
        f"stock price under $100 USD, Vol/OI > 5, "
        f"focus on high momentum names like OKLO, SMCI, RKLB, IONQ."
    )
    
    print(f"📡 正在扫描 $100 以下美股异动 (目标日: {expiry_date})...")
    
    try:
        # 1. 搜索数据
        search_data = tavily.search(query=query, search_depth="advanced", max_results=20)

        # 2. 加入防撞保护：在调用 AI 前强制休息 5 秒，防止 429 报错
        time.sleep(5)

        # 3. 任务指令：仅看价格，排除废话
        prompt = f"""
        数据：{search_data}
        任务：找出符合条件的爆发股。
        
        ⛔ 限制：
        1. 股价必须低于 $100。超过 $100 的一律剔除（如目前的 NVDA, MSTR 等）。
        2. 代码必须是美股代码。

        ✅ 核心：
        - 筛选 {expiry_date} 到期的异常 Call 单。
        - 寻找未来 10 天内的强力催化剂。

        输出格式：
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
        # 如果遇到 429 频率限制报错，提供清晰提示
        if "429" in str(e):
            print("❌ 错误：触发了 API 频率限制 (429)。请等一分钟后再试，或降低 GitHub Actions 的运行频率。")
        else:
            print(f"❌ 运行故障: {str(e)}")

if __name__ == "__main__":
    run_options_led_stock_sniper()
