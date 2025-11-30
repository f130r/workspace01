import streamlit as st

st.title("マルバツゲーム（Tic-Tac-Toe）")

if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "O"
    st.session_state.winner = None

def check_winner(board):
    for i in range(3):
        if board[i][0] != "" and all(board[i][j] == board[i][0] for j in range(3)):
            return board[i][0]
        if board[0][i] != "" and all(board[j][i] == board[0][i] for j in range(3)):
            return board[0][i]
    if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(3)):
        return board[0][0]
    if board[0][2] != "" and all(board[i][2-i] == board[0][2] for i in range(3)):
        return board[0][2]

    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return "Draw"
    return None

for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        cell_value = st.session_state.board[i][j]

        if cell_value == "" and st.session_state.winner is None:
            if cols[j].button(" ", key=f"btn-{i}-{j}"):
                st.session_state.board[i][j] = st.session_state.turn
                st.session_state.turn = "X" if st.session_state.turn == "O" else "O"
                st.session_state.winner = check_winner(st.session_state.board)
        else:
            cols[j].button(cell_value, key=f"btn-{i}-{j}", disabled=True)

if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("引き分け!")
    else:
        st.success(f"{st.session_state.winner} の勝ち!")

if st.button("リセット"):
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "O"
    st.session_state.winner = None
