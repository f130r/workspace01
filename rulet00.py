import streamlit as st
import random
import time

st.title("ルーレットアプリ（アニメーション付き）")

# 項目入力
options = st.text_area("項目をカンマで入力", "リンゴ,バナナ,オレンジ").split(",")

# 回すボタン
if st.button("回す"):
    options = [o.strip() for o in options if o.strip()]
    if not options:
        st.warning("項目を入力してください")
    else:
        placeholder = st.empty()
        # アニメーション回数
        for _ in range(20):
            current = random.choice(options)
            placeholder.markdown(f"**{current}**")
            time.sleep(0.1)  # 0.1秒ごとに切り替え
        # 最終結果
        result = random.choice(options)
        placeholder.markdown(f"🎉 **結果: {result}** 🎉")
