import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# 初期化
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "○"


def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 横
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 縦
        [0, 4, 8], [2, 4, 6]              # 斜め
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

winner = check_winner(st.session_state.board)

# --- UI 改善ポイント ---
# ・マス間の余白なし → オセロみたいに詰まって見える
# ・フォントサイズを大きく → 視認性アップ
button_style = """
    <style>
    div.stButton > button {
        width: 80px;
        height: 80px;
        font-size: 45px;
        padding: 0;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# --- マス表示 (3x3) ---
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if st.button(st.session_state.board[i] or " ", key=i):
            if winner is None:
                click_cell(i)
    if (i + 1) % 3 == 0 and i < 8:
        cols = st.columns(3)

# --- 勝敗表示 ---
winner = check_winner(st.session_state.board)

if winner:
    st.success(f"🎉 勝者：{winner}")
elif "" not in st.session_state.board:
    st.info("引き分けです！")

if st.button("リセット"):
    st.session_state.board = [""] * 9
    st.session_state.turn = "○"
