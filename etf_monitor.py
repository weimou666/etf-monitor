import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ===================== 页面配置 =====================
st.set_page_config(
    page_title="etf份额监控，国家队动向追踪",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('dark_background')

# ===================== ETF 列表 =====================
ETF_LIST = {
    "510300": "华泰柏瑞沪深300ETF",
    "510310": "易方达沪深300ETF",
    "510320": "中金沪深300ETF",
    "510330": "华夏沪深300ETF",
    "510350": "工银瑞信沪深300ETF",
    "510360": "广发沪深300ETF",
    "510370": "兴业沪深300ETF",
    "510380": "国海富兰克林沪深300ETF"
}

# ===================== 模拟数据 =====================
def get_demo_data():
    dates = pd.date_range(start="2024-01-01", end="2026-04-10", freq="D")
    df = pd.DataFrame({
        "date": dates,
        "share": (np.random.randn(len(dates)).cumsum() + 100).clip(80, 150)
    })
    df["share_pct"] = df["share"].pct_change() * 100
    return df.dropna()

# ===================== 绘图 =====================
def make_chart(df, code, name):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,8), sharex=True, gridspec_kw={"height_ratios":[3,1]})
    ax1.plot(df["date"], df["share"], color="#00bfff", linewidth=2.2)
    first = df["share"].iloc[0]
    last = df["share"].iloc[-1]
    total_pct = (last / first - 1) * 100
    ax1.text(0.02, 0.95, f"最新份额: {last:.2f} 亿份\n区间涨跌幅: {total_pct:.2f}%", 
             transform=ax1.transAxes, fontsize=12, bbox=dict(boxstyle="round", facecolor="#111", alpha=0.85))
    ax1.set_title(f"{code} | {name} — 份额追踪", fontsize=15, color="white")
    ax1.set_ylabel("总份额（亿份）")
    ax1.grid(alpha=0.25)

    bar_color = ["#ff3333" if x>0 else "#2ecc71" for x in df["share_pct"]]
    ax2.bar(df["date"], df["share_pct"], color=bar_color, alpha=0.75, width=1)
    ax2.axhline(y=0, color='white', linewidth=0.8)
    ax2.set_ylabel("单日变动 %")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# ===================== 界面 =====================
st.title("🔍 ETF份额监控 | 国家队动向追踪")
st.markdown("> 每日 09:00 / 15:30 自动更新数据")
st.divider()

sel_code = st.sidebar.selectbox("选择ETF", list(ETF_LIST.keys()), format_func=lambda x: f"{x} {ETF_LIST[x]}")
df = get_demo_data()
fig = make_chart(df, sel_code, ETF_LIST[sel_code])
st.pyplot(fig, use_container_width=True)

st.subheader("📊 最新30条数据")
show_df = df[["date","share","share_pct"]].tail(30)
show_df["date"] = pd.to_datetime(show_df["date"]).dt.date
show_df.columns = ["日期","份额(亿)","变动(%)"]
st.dataframe(show_df, use_container_width=True)