import streamlit as st
from datetime import datetime
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

        # 宛名・発行日・但し書きを削除し、金額のみにする
        amount = st.number_input("金額 (円)", value=1000, min_value=1)

        submitted = st.form_submit_button("領収書を作成")

        if submitted:
            # 現在の日時を保存
            current_datetime = datetime.now()

            st.session_state.receipt_data = {
                "amount": amount,
                "issue_datetime": current_datetime,
            }
            st.session_state.show_receipt = True
            st.rerun()

    st.markdown("---")

# --- 領収書表示の状態 ---
else:
    # 保存されたデータを使って領収書を表示
    data = st.session_state.receipt_data
    amount = data["amount"]
    issue_datetime = data["issue_datetime"]

    amount_str = f"¥{amount:,}"

    # データを文字列として整形
    issue_date_str = issue_datetime.strftime('%Y年%m月%d日 %H:%M:%S')
    company_name = "（あなたの会社名など）"

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

        st.markdown(
            f"""
            <div style='text-align: center; border: 4px solid #333; padding: 15px; margin: 20px 0;'> 
                <span style='font-size: 48px; font-weight: bold;'>{amount_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ★修正箇所: 日時と発行元を大きく表示（HTML/Markdownで直接表示）
        st.markdown(
            f"""
            <div style='margin-bottom: 10px; padding-left: 5px;'>
                <span style='font-size: 18px;'>日付: </span><span style='font-size: 24px; font-weight: bold;'>{issue_date_str}</span><br>
                <span style='font-size: 18px;'>発行元: </span><span style='font-size: 24px; font-weight: bold;'>{company_name}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ★修正箇所: 冗長なMarkdownテーブルを削除
        # 以前のコードにあった | 項目 | 金額 | のテーブルを削除

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