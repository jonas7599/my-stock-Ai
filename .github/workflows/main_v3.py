import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_ignition_hunter():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    model = genai.GenerativeModel(target_model)

    # 1. 深度搜索词：聚焦缩量横盘中的异动信号
    query = """
    US small-cap stocks: low volume consolidation with occasional spikes, 
    increasing accumulation/distribution line, rising cost basis, 
    positive news expected within 1 month, stocks near breakout from base.
    """
    print(f"📡 正在扫描【吸筹待启动】标的：监控换手率与缩量异动...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 2. 策略 Prompt：强化指标分析
    prompt = f"""
    分析以下数据：{search_data}

    你的目标是寻找“即将点火启动”的埋伏股。
    
    分析维度：
    1. 吸筹特征：股价长期横盘，但换手率缓慢上升，成交量出现零星“红柱”（吸筹）。
    2. 指标暗示：委比偏正、均线高度粘合、价格处于震荡区间上沿。
    3. 利好潜伏：寻找未来 2-4 周内有重大事件（财报、PDUFA、产品发布）的标的。

    请按表格输出：
    | 代码 | 吸筹阶段 (初期/中期/就绪) | 换手率/量能异动 | 潜伏利好 | 预估点火日期 | 埋伏参考价 | 止损参考 |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    """

    response = model.generate_content(prompt)
    print("\n" + "🎯"*15)
    print("💎 点火猎人·吸筹启动监控 💎")
    print("🎯"*15)
    print(response.text)

if __name__ == "__main__":
    run_ignition_hunter()
