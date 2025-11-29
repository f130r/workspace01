import streamlit as st
import pandas as pd

st.title("時間割アプリ")

# 時限と曜日
days = ["月", "火", "水", "木", "金"]
periods = ["1限", "2限", "3限", "4限", "5限"]

# 空の時間割
timetable = pd.DataFrame("", index=periods, columns=days)

st.write("時間割を入力してください：")

# 入力フォーム
for p in periods:
    cols = st.columns(len(days))
    for i, d in enumerate(days):
        timetable.loc[p, d] = cols[i].text_input(f"{d} {p}", "")

st.write("## あなたの時間割")
st.dataframe(timetable)
