import streamlit as st

st.title("マルバツゲーム（Tic-Tac-Toe）")

# 3x3 のボードをセッションステートで保持
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "O"  # O からスタート
    st.session_state.winner = None

# 勝敗判定関数
def check_winner(board):
    # 横・縦
    for i in range(3):
        if board[i][0] != "" and all(board[i][j] == board[i][0] for j in range(3)):
            return board[i][0]
        if board[0][i] != "" and all(board[j][i] == board[0][i] for j in range(3)):
            return board[0][i]
    # 斜め
    if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(3)):
        return board[0][0]
    if board[0][2] != "" and all(board[i][2-i] == board[0][2] for i in range(3)):
        return board[0][2]
    # 引き分け
    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return "Draw"
    return None

# ボード表示
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if st.session_state.board[i][j] == "" and st.session_state.winner is None:
            if cols[j].button(" "):
                st.session_state.board[i][j] = st.session_state.turn
                st.session_state.turn = "X" if st.session_state.turn == "O" else "O"
                st.session_state.winner = check_winner(st.session_state.board)
        else:
            cols[j].button(st.session_state.board[i][j], disabled=True)

# 結果表示
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("引き分け！")
    else:
        st.success(f"{st.session_state.winner} の勝ち！")

# リセットボタン
if st.button("リセット"):
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "O"
    st.session_state.winner = None
