import os
import datetime
import google.generativeai as genai
from tavily import TavilyClient

# 1. 初始化（从 GitHub Secrets 获取）
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 修复模型调用：直接指定版本号，确保 gemini-1.5-flash 可用
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 动态日期逻辑
    today = datetime.date.today()
    target_date = today if today.weekday() < 5 else today - datetime.timedelta(days=today.weekday() - 4)
    date_str = target_date.strftime("%Y-%m-%d")

    # 2. 核心：修复 Query 过长问题 (精简至关键词，不超过400字符)
    # 策略逻辑：全行业、小市值($1-$50)、横盘缩量、能量潮吸筹、近期利好
    query = f"US small-cap stocks $1-$50 Market Cap <$2B tight consolidation VCP accumulation breakout news {date_str}"

    print(f"🚀 正在执行全行业策略扫描 (分析日期: {date_str})...")
    
    # 搜索数据
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 强化 Prompt：将复杂的筛选逻辑放在 AI 分析阶段，不占用搜索长度
    prompt = f"""
    分析以下实时数据：{search_data}

    任务：从全行业中筛选出 5 只【真实存在】且表现出“吸筹结束、利好放量”特征的小市值美股。

    ### 筛选硬指标：
    1. **横盘吸筹**：股价过去 2-4 周窄幅震荡，成交量在横盘末端出现“口袋支点”（涨时放量，跌时缩量）。
    2. **异动特征**：成交量明显高于 50 日均值，但股价尚未完全飞离箱体。
    3. **市值/价格**：市值 < 20 亿美金，股价在 $1 - $50 之间。
    4. **利好驱动**：必须有具体的近期消息（如合同、财报预增、行业催化）。

    ### 严格格式要求（严禁废话，直接出表）：
    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    # 生成分析结果
    response = model.generate_content(prompt)

    print(f"\n🎯 全行业点火猎人·实时扫描报告 ({date_str}) 🎯")
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
