import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta  # timedeltaをインポート
import os
import re
import pytz

FILE = "timecard.csv"  # CSV名


# ───── 勤務時間計算関数 ─────
def calculate_work_hours(start_str, end_str):
    """ 'HH:MM:SS'形式の文字列から勤務時間を計算し、'HH:MM'形式の文字列で返す """
    if not (start_str and end_str):
        return ""
    try:
        # 時刻文字列をtimeオブジェクトに変換
        start_time = datetime.strptime(start_str, "%H:%M:%S").time()
        end_time = datetime.strptime(end_str, "%H:%M:%S").time()

        # 簡易計算のため、日付を固定（同じ日として扱う）
        start_dt = datetime.combine(datetime.min.date(), start_time)
        end_dt = datetime.combine(datetime.min.date(), end_time)

        # 退勤が出勤より前（日付を跨いだ場合）は、退勤時刻に1日加算
        if end_dt < start_dt:
            end_dt += timedelta(days=1)

        work_duration = end_dt - start_dt

        # 勤務時間をHH:MM形式に変換
        total_seconds = int(work_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return f"{hours:02d}:{minutes:02d}"
    except ValueError:
        return ""


# ───── CSVが存在しなければ作成 ─────
if not os.path.exists(FILE):
    # 'hours'列も追加
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

# ───── 勤務時間（hours）列の追加・更新 ─────
df["hours"] = [
    calculate_work_hours(start, end)
    for start, end in zip(df["start"], df["end"])
]

# ───── 日本時間（JST）で現在時刻を取得 ─────
JST = pytz.timezone('Asia/Tokyo')
now_jst = datetime.now(JST)

today = now_jst.strftime("%Y-%m-%d")
now_time = now_jst.strftime("%H:%M:%S")
# ──────────────────────────────────────

# ───── Streamlit 設定 ─────
st.set_page_config(page_title="タイムカード", layout="centered")
st.title("🕒 タイムカード")

# 表示用 DataFrame はコピーで作成（空列追加を防ぐ）
df_display = df[["date", "start", "end", "hours"]].copy().rename(  # ★ 'hours'を追加
    columns={"date": "日付", "start": "出勤", "end": "退勤", "hours": "勤務時間"}  # ★ 列名を更新
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
    # ... (出勤処理は変更なし) ...
    today_row = df[df["date"] == today]
    if today_row.empty:
        new = pd.DataFrame({"date": [today], "start": [now_time], "end": [""]})
        df = pd.concat([df, new], ignore_index=True)

        # リスト内包表記で勤務時間を再計算 (新規追加時は空だがロジック統一)
        df["hours"] = [
            calculate_work_hours(start, end)
            for start, end in zip(df["start"], df["end"])
        ]

        df.to_csv(FILE, index=False)
        st.success(f"出勤: {now_time}")
    else:
        st.warning("今日の出勤は既に記録されています")

# 退勤処理 (★★ このブロック全体を置き換えてください ★★)
if clock_out_pressed:
    today_row = df[df["date"] == today]

    if today_row.empty:
        # 1. 今日の出勤記録がない場合
        st.warning("まず出勤を記録してください")
    else:
        # 2. 今日の出勤記録がある場合

        # DataFrameから退勤時刻の値を取得
        # end_valueはここで確実に定義される
        end_value = today_row.iloc[0]["end"]

        if end_value == "":
            # 2-a. 退勤が未記録の場合
            df.loc[df["date"] == today, "end"] = now_time

            # リスト内包表記で勤務時間を再計算
            df["hours"] = [
                calculate_work_hours(start, end)
                for start, end in zip(df["start"], df["end"])
            ]

            df.to_csv(FILE, index=False)
            st.success(f"退勤: {now_time}")
        else:
            # 2-b. 既に退勤済みの場合
            st.warning("既に退勤済みです")

# 今日の記録クリア
if clear_today_pressed:
    # ... (クリア処理は変更なし) ...
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
# ★ 表示する列を 'hours'も含めて定義
df_display = df.rename(columns={"date": "日付", "start": "出勤", "end": "退勤", "hours": "勤務時間"})
edited_df = st.data_editor(
    df_display,
    num_rows="dynamic",  # 行の追加・削除可
)

if st.button("編集内容を保存"):
    # 保存時に元の列名に戻す
    save_df = edited_df.rename(columns={"日付": "date", "出勤": "start", "退勤": "end", "勤務時間": "hours"})

    # 時刻の正規化
    for col in ["start", "end"]:
        save_df[col] = save_df[col].apply(lambda x: x if re.match(r"^\d{2}:\d{2}:\d{2}$", str(x)) else "")

    # 編集後のデータフレームで勤務時間を再計算（手動編集に対応）
    save_df["hours"] = save_df.apply(
        lambda row: calculate_work_hours(row["start"], row["end"]),
        axis=1
    )

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