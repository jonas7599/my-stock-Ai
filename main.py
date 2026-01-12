import os
import google.generativeai as genai
from tavily import TavilyClient

# 初始化 API
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_analysis():
    # 1. 自动兼容模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = next((m for m in available_models if 'flash' in m.lower()), available_models[0])
    
    # 2. 增强搜索指令：覆盖全行业，寻找异动和硬核新闻
    # 搜索词增加了对生物医药(FDA)、科技、能源等热门领域的关键词覆盖
    query = "US stock market top gainers today, massive volume breakout, small-cap stocks with FDA approval, tech contracts, or earnings beat"
    print(f"正在使用模型 {target_model} 扫描全行业热门板块...")
    search_data = tavily.search(query=query, search_depth="advanced")

    # 3. 优化 Prompt：要求 AI 必须识别板块并按你的“四大准则”筛选
    model = genai.GenerativeModel(target_model)
    prompt = f"""
    你是专业的资深交易员。请分析以下实时搜索数据：
    {search_data}

    你的任务是找出今天美股市场中表现最强劲的【小盘股】，必须严格符合以下指标：
    1. 巨量突破：成交量远高于近期平均。
    2. 价格强势：收盘接近当日最高价，且盘后无大幅回落。
    3. 硬核利好：必须有实际的利好驱动（如：FDA通过、财报大超预期、重大合作协议、资产收购）。

    请按【所属板块】对结果进行归类。输出格式为 Markdown 表格：
    股票代码 | 所属板块 | 硬核利好解析 | 关键指标(量/价) | 综合评分(1-10) | 操作建议
    """
    
    response = model.generate_content(prompt)
    print("\n" + "="*40)
    print("🚀 全行业热门板块选股报告 🚀")
    print("="*40)
    print(response.text)

if __name__ == "__main__":
    run_analysis()
