import streamlit as st
from datetime import datetime  # ★修正: date から datetime に変更
import pandas as pd

st.set_page_config(
    page_title="簡単デジタル領収書生成",
    layout="centered"
)

st.title("デジタル領収書作成")

# --- セッションステートの初期化 ---
if 'show_receipt' not in st.session_state:
    st.session_state.show_receipt = False
if 'receipt_data' not in st.session_state:
    st.session_state.receipt_data = {}

# --- フォーム表示の状態 ---
if not st.session_state.show_receipt:
    st.subheader("入力フォーム")
    with st.form("receipt_form"):

        # ★修正: 宛名・発行日・但し書きを削除し、金額のみにする
        amount = st.number_input("金額 (円)", value=1000, min_value=1)

        submitted = st.form_submit_button("領収書を作成")

        if submitted:
            # ★修正: 現在の日時を保存
            current_datetime = datetime.now()

            st.session_state.receipt_data = {
                "amount": amount,
                "issue_datetime": current_datetime,  # issue_date を issue_datetime に変更
            }
            st.session_state.show_receipt = True
            st.rerun()

    st.markdown("---")

# --- 領収書表示の状態 ---
else:
    # 保存されたデータを使って領収書を表示
    data = st.session_state.receipt_data
    amount = data["amount"]
    issue_datetime = data["issue_datetime"]  # issue_date を issue_datetime に変更

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

        # ★修正: 宛名表示を削除

        st.markdown(
            f"""
            <div style='text-align: center; border: 4px solid #333; padding: 15px; margin: 20px 0;'> 
                <span style='font-size: 48px; font-weight: bold;'>{amount_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        df = pd.DataFrame({
            # ★修正: 但し書きを削除
            '項目': ['日付', '発行元'],
            '内容': [
                # ★修正: 日付と時刻を表示
                issue_datetime.strftime('%Y年%m月%d日 %H:%M:%S'),
                "（あなたの会社名など）"
            ]
        })
        st.dataframe(df, hide_index=True, use_container_width=True,
                     column_config={"項目": st.column_config.Column(width="small")})

        st.markdown(
            """
            <div style='text-align: right; margin-top: 20px;'>
                **上記金額、正に領収いたしました。**
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "💡 **保存方法:** この領収書は画像ではないため、PCやスマートフォンのスクリーンショット機能を使って保存してください。")

    # フォームに戻るボタン
    if st.button("入力フォームに戻る"):
        st.session_state.show_receipt = False
        st.rerun()