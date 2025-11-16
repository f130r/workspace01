import streamlit as st
from datetime import date
import pandas as pd

st.set_page_config(
    page_title="簡単デジタル領収書生成",
    layout="centered"
)

st.title("デジタル領収書作成")

# --- セッションステートの初期化 ---
# 'show_receipt'がTrueなら領収書表示、Falseならフォーム表示
if 'show_receipt' not in st.session_state:
    st.session_state.show_receipt = False
if 'receipt_data' not in st.session_state:
    st.session_state.receipt_data = {}

# --- フォーム表示の状態 ---
if not st.session_state.show_receipt:
    st.subheader("入力フォーム")
    with st.form("receipt_form"):  # フォームウィジェットを使って、入力確定時にボタンを押す
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("宛名", "山田太郎")
            amount = st.number_input("金額 (円)", value=1000, min_value=1)
        with col2:
            issue_date = st.date_input("発行日", date.today())
            note = st.text_input("但し書き", "〇〇代として")

        # ボタンのテキストを修正: 以前は "領収書を表示" だったが、フォーム確定用なので "作成" に近い表現に
        submitted = st.form_submit_button("領収書を作成")

        if submitted:
            # フォームが送信されたら、データを保存して領収書表示状態へ
            st.session_state.receipt_data = {
                "name": name,
                "amount": amount,
                "issue_date": issue_date,
                "note": note
            }
            st.session_state.show_receipt = True
            st.rerun()  # ★ここを st.rerun() に修正

    st.markdown("---")

# --- 領収書表示の状態 ---
else:
    # 保存されたデータを使って領収書を表示
    data = st.session_state.receipt_data
    name = data["name"]
    amount = data["amount"]
    issue_date = data["issue_date"]
    note = data["note"]

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
        st.rerun()  # ★ここも st.rerun() に修正