import streamlit as st
import pandas as pd
from datetime import datetime
import os


FILE = "timecard.csv"   # CSV名（存在しなくてもOK）

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["date", "start", "end"])
    df.to_csv(FILE, index=False)

st.set_page_config(page_title="タイムカード", layout="centered")
st.title("🕒 タイムカード")

df = pd.read_csv(FILE, dtype=str)

today = datetime.now().strftime("%Y-%m-%d")
now_time = datetime.now().strftime("%H:%M:%S")

if "end" not in df.columns:
    df["end"] = ""


# ───── 出勤 ─────
if st.button("出勤"):
    today_row = df[df["date"] == today]

    if today_row.empty:
        new = pd.DataFrame({"date": [today], "start": [now_time], "end": [""]})
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success(f"出勤: {now_time}")
    else:
        st.warning("今日の出勤は既に記録されています")


# ───── 退勤 ─────
if st.button("退勤"):
    today_row = df[df["date"] == today]

    if today_row.empty:
        st.warning("まず出勤を記録してください")
    else:
        end_value = today_row.iloc[0]["end"]
        if end_value in ["", None] or pd.isna(end_value):
            df.loc[df["date"] == today, "end"] = now_time
            df.to_csv(FILE, index=False)
            st.success(f"退勤: {now_time}")
        else:
            st.warning("既に退勤済みです")


# ───── 出勤・退勤をクリア ─────
if st.button("記録をクリア"):
    df = df[df["date"] != today]
    df.to_csv(FILE, index=False)
    st.info("今日の記録をクリアしました")


# ───── 表示 ─────
# start/end → 出勤/退勤 に列名変更
df_display = df.rename(columns={"date": "日付", "start": "出勤", "end": "退勤"})

# 表を大きく見やすく設定
st.subheader("📄 記録")
st.dataframe(
    df_display,
    use_container_width=True,
    height=400
)

# 表全体のフォントを大きくする（CSS）
st.markdown(
    """
    <style>
    .stDataFrame tbody, .stDataFrame th, .stDataFrame td {
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
