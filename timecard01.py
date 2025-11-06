import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re

FILE = "timecard.csv"   # CSV名

# ───── CSVが存在しなければ作成 ─────
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["date", "start", "end"])
    df.to_csv(FILE, index=False)

# ───── CSV読み込み ─────
df = pd.read_csv(FILE, dtype=str)

# 全て空の列は削除（過去に空列が残っていた場合）
df = df.dropna(axis=1, how="all")

# 必要な列だけ作成
for col in ["date", "start", "end"]:
    if col not in df.columns:
        df[col] = ""

# 不正な時刻を空文字に置換（HH:MM:SS以外）
for col in ["start", "end"]:
    df[col] = df[col].fillna("")
    df[col] = df[col].apply(lambda x: x if re.match(r"^\d{2}:\d{2}:\d{2}$", str(x)) else "")

# 今日の日付と現在時刻
today = datetime.now().strftime("%Y-%m-%d")
now_time = datetime.now().strftime("%H:%M:%S")

# ───── Streamlit 設定 ─────
st.set_page_config(page_title="タイムカード", layout="centered")
st.title("🕒 タイムカード")

# 表示用 DataFrame はコピーで作成（空列追加を防ぐ）
df_display = df[["date","start","end"]].copy().rename(
    columns={"date":"日付","start":"出勤","end":"退勤"}
)

# ───── 出勤・退勤・クリアボタン ─────
col1, col2, col3 = st.columns(3)

with col1:
    clock_in_pressed = st.button("出勤")
with col2:
    clock_out_pressed = st.button("退勤")
with col3:
    clear_today_pressed = st.button("今日の記録をクリア")

# 出勤処理
if clock_in_pressed:
    today_row = df[df["date"] == today]
    if today_row.empty:
        new = pd.DataFrame({"date": [today], "start": [now_time], "end": [""]})
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success(f"出勤: {now_time}")
    else:
        st.warning("今日の出勤は既に記録されています")

# 退勤処理
if clock_out_pressed:
    today_row = df[df["date"] == today]
    if today_row.empty:
        st.warning("まず出勤を記録してください")
    else:
        end_value = today_row.iloc[0]["end"]
        if end_value == "":
            df.loc[df["date"] == today, "end"] = now_time
            df.to_csv(FILE, index=False)
            st.success(f"退勤: {now_time}")
        else:
            st.warning("既に退勤済みです")

# 今日の記録クリア
if clear_today_pressed:
    df = df[df["date"] != today]
    df.to_csv(FILE, index=False)
    st.info("今日の記録をクリアしました")

# ───── 個別削除 ─────
st.subheader("🗑 個別削除")
dates = df["date"].tolist()
selected_date = st.selectbox("削除する日付を選択", options=["選択してください"] + dates)
if st.button("選択した日付を削除"):
    if selected_date != "選択してください":
        df = df[df["date"] != selected_date]
        df.to_csv(FILE, index=False)
        st.success(f"{selected_date} の記録を削除しました")

# ───── 全消去 ─────
if st.button("全記録を削除"):
    df = df[0:0]  # 空の DataFrame にする
    df.to_csv(FILE, index=False)
    st.warning("全ての記録を削除しました")

# ───── 表示・編集 ─────
st.subheader("📄 記録・編集")
df_display = df.rename(columns={"date": "日付", "start": "出勤", "end": "退勤"})
edited_df = st.data_editor(
    df_display,
    num_rows="dynamic",  # 行の追加・削除可
)

if st.button("編集内容を保存"):
    # 保存時に元の列名に戻す
    save_df = edited_df.rename(columns={"日付": "date", "出勤": "start", "退勤": "end"})
    # 時刻の正規化
    for col in ["start", "end"]:
        save_df[col] = save_df[col].apply(lambda x: x if re.match(r"^\d{2}:\d{2}:\d{2}$", str(x)) else "")
    save_df.to_csv(FILE, index=False)
    st.success("編集内容を保存しました")

# 表全体のフォントサイズを大きくする
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
