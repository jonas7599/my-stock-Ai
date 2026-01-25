import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 严格使用你要求的原有模型
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 动态日期逻辑
    today = datetime.date.today()
    target_date = today if today.weekday() < 5 else today - datetime.timedelta(days=today.weekday() - 4)
    date_str = target_date.strftime("%Y-%m-%d")

    # 2. 优化后的搜索指令 (控制在400字符以内，解决报错)
    # 聚焦：小市值、横盘、异动、利好
    query = f"US small-cap stocks $1-$50 Market Cap <$2B consolidation breakout unusual volume positive news catalyst {date_str}"

    print(f"🚀 正在执行全行业策略扫描 (分析日期: {date_str})...")
    try:
        search_data = tavily.search(query=query, search_depth="advanced")
    except Exception as e:
        print(f"搜索出错: {e}")
        return

    # 3. 策略分析 Prompt (在此处定义完整的吸筹启动逻辑)
    prompt = f"""
    分析数据：{search_data}
    任务：筛选 5 只符合“吸筹结束、利好放量”的小市值美股（$1-$50，市值<$2B）。

    ### 筛选准则：
    1. **横盘吸筹**：股价过去 2-4 周窄幅波动，成交量在横盘末端温和放大。
    2. **异动点火**：当日或盘前有明显突破迹象，成交量高于均值。
    3. **利好驱动**：必须关联具体的近期利好（如 FDA、新合同、财报优于预期）。
    4. **全行业**：涵盖所有板块，寻找逻辑最硬的标度。

    ### 输出要求：
    - 严禁废话，直接输出表格。
    - 格式必须严格如下：

    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    # 生成分析结果
    response = model.generate_content(prompt)

    # 4. 打印报告
    print(f"\n🎯 全行业点火猎人·实时扫描报告 ({date_str}) 🎯")
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
