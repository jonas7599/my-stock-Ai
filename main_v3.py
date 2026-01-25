# 1. 初始化
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    # 自动获取最新模型
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 动态日期逻辑
    today = datetime.date.today()
    target_date = today if today.weekday() < 5 else today - datetime.timedelta(days=today.weekday() - 4)
    date_str = target_date.strftime("%Y-%m-%d")

    # 2. 核心策略搜索指令：聚焦“横盘 + 吸筹特征 + 催化剂”
    # 重点在于搜寻：1. 缩量横盘 2. 价格未动但OBV/成交量异动 3. 伴随利好公告
    query = f"""
    Find 10 US small-cap stocks ($1-$50, Market Cap < $2B) on {date_str} that meet:
    1. 2-4 weeks of horizontal consolidation/flat base (VCP pattern).
    2. Signs of institutional accumulation: OBV rising or "Pocket Pivot" volume spikes while price remains in a tight range.
    3. Recent positive catalysts: FDA, partnership, new contracts, or earnings beat within last 48 hours.
    Search across ALL sectors. Return tickers with price and specific volume activity.
    """

    print(f"🚀 正在执行全行业策略扫描 (分析日期: {date_str})...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 强化 Prompt：植入吸筹识别逻辑与严格格式化要求
    prompt = f"""
    你是一名顶级美股策略分析师，擅长捕捉“机构吸筹后的首波启动”。
    分析以下实时数据：{search_data}

    ### 筛选任务：
    从全行业中选出 5 只最符合【吸筹结束、准备启动】特征的标的。
    
    ### 核心策略指标：
    1. **横盘整理**：股价在过去 2-4 周波动极小，形成紧凑的“地基”。
    2. **机构吸筹**：成交量在横盘末端出现非对称增长（涨时放量，跌时极度缩量），即“口袋支点”。
    3. **市值/价格**：市值 < 20亿美金，价格介于 $1 - $50 之间。
    4. **利好驱动**：必须有具体的近期新闻（8-K表、合同、产品进展）作为引爆点。

    ### 严格执行原则：
    1. **全行业覆盖**：不限于科技或生物医药，只要逻辑硬，全行业均可。
    2. **拒绝幻觉**：代码必须真实，逻辑必须基于数据中的成交量异动。
    3. **禁止废话**：严禁开头总结，直接以 Markdown 表格形式输出。

    请按以下格式输出：
    | 代码 | 所属行业 | 当前价格 | 成交异动特征 | 启动逻辑简述 | 关键支撑/阻力 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)

    print(f"\n🎯 全行业点火猎人·实时扫描报告 ({date_str}) 🎯")
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
