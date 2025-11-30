import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# 初期化
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "○"

def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    return None

def click_cell(i):
    if st.session_state.board[i] == "":
        st.session_state.board[i] = st.session_state.turn
        st.session_state.turn = "×" if st.session_state.turn == "○" else "○"

st.title("⭕❌ マルバツゲーム")

# CSSでボタンサイズ・文字サイズ・余白を調整
button_style = """
<style>
div.stButton > button {
    width: 100px !important;
    height: 100px !important;
    font-size: 60px !important;  /* クリック後の文字を大きく */
    padding: 0 !important;
    margin: 0 !important;       /* ボタン間の余白をゼロに */
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# マス表示
for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        idx = row * 3 + col
        if cols[col].button(st.session_state.board[idx] or " ", key=idx):
            click_cell(idx)

# 勝敗判定
winner = check_winner(st.session_state.board)
if winner:
    st.success(f"🎉 勝者：{winner}")
elif "" not in st.session_state.board:
    st.info("引き分けです！")

# リセット
if st.button("リセット"):
    st.session_state.board = [""] * 9
    st.session_state.turn = "○"
