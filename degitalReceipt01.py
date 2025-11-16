import streamlit as st
from datetime import date
import pandas as pd

st.set_page_config(
    page_title="簡単デジタル領収書生成",
    layout="centered"
)

st.title("簡単デジタル領収書生成")

# --- 入力フォーム ---
st.subheader("入力フォーム")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("宛名", "山田太郎")
    amount = st.number_input("金額 (円)", value=1000, min_value=1)
with col2:
    issue_date = st.date_input("発行日", date.today())
    note = st.text_input("但し書き", "〇〇代として")

st.markdown("---")

# --- 領収書風の表示 ---
if st.button("領収書を表示"):
    amount_str = f"¥{amount:,}"

    st.subheader("🧾 デジタル領収書（スクリーンショット用）")

    with st.container(border=True):
        st.markdown(
            """
            <div style='text-align: center; border-bottom: 3px double black; padding-bottom: 10px; margin-bottom: 20px;'>
                <h1 style='margin: 0; font-size: 36px;'>領収書</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(f"**宛名:** {name} 様", unsafe_allow_html=True)

        # ここを修正: background-color を削除、または transparent に設定
        st.markdown(
            f"""
            <div style='text-align: center; border: 4px solid #333; padding: 15px; margin: 20px 0;'> 
                <span style='font-size: 48px; font-weight: bold;'>{amount_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        df = pd.DataFrame({
            '項目': ['日付', '但し書き', '発行元'],
            '内容': [
                issue_date.strftime('%Y年%m月%d日'),
                note,
                "（あなたの会社名など）"
            ]
        })
        st.dataframe(df, hide_index=True, use_container_width=True,
                     column_config={"項目": st.column_config.Column(width="small")})

        # 金額を強調表示 (HTMLで装飾)
        st.markdown(
            f"""
                    <div style='text-align: center; border: 4px solid #333; padding: 15px; margin: 20px 0;'> 
                        <span style='font-size: 48px; font-weight: bold;'>{amount_str}</span>
                    </div>
                    """,  # ★この閉じの"""が不足している可能性があります
            unsafe_allow_html=True
        )