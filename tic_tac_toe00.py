import streamlit as st
import numpy as np

# ページの基本設定
st.set_page_config(page_title="マルバツゲーム", layout="centered")

# --- カスタムCSSの適用 ---
# 添付画像のような見た目を実現するため、Streamlitのデフォルトスタイルを上書きします。
st.markdown("""
<style>
/* 1. マス目（ボタン）の共通スタイル設定 */
div.stButton > button {
    width: 100px !important;
    height: 100px !important;
    font-size: 80px !important; /* マル/バツを大きく表示 */
    padding: 0 !important;
    line-height: 100px !important; /* 文字を垂直中央に配置 */
    text-align: center !important;
    border: 1px solid #000 !important; /* 枠線を黒に */
    background-color: #f0f0f0 !important; /* 背景色を薄い灰色に */
    margin: -1px !important; /* ⭐ マス目間の間隔を詰めるための必須設定 ⭐ */
    border-radius: 0px !important; /* 角丸をなくす */
    font-weight: bold;
}

/* 2. st.columnsコンテナの隙間をゼロにする */
div[data-testid="stHorizontalBlock"] {
    gap: 0px !important;
}

/* 3. 添付画像のようなシンプルなメッセージボックスを模倣 */
.stSuccess {
    border: 1px solid #000 !important;
    background-color: #fff !important;
    color: #000 !important;
    padding: 10px !important;
    text-align: center;
    font-size: 20px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- 初期化と状態管理 ---
if "board" not in st.session_state:
    # 9要素のリストを3x3のNumPy配列として管理すると、勝敗判定が容易になります
    st.session_state.board = np.full((3, 3), "", dtype=str)
if "turn" not in st.session_state:
    st.session_state.turn = "○"
if "winner" not in st.session_state:
    st.session_state.winner = None


# --- ロジック関数 ---
def check_win(board_array):
    """NumPy配列を使って勝敗を判定"""
    # 行、列、対角線
    for i in range(3):
        # 行 (Row)
        if all(board_array[i, :] == board_array[i, 0]) and board_array[i, 0] != "":
            return board_array[i, 0]
        # 列 (Column)
        if all(board_array[:, i] == board_array[0, i]) and board_array[0, i] != "":
            return board_array[0, i]

    # 対角線 (Diagonal)
    if all(np.diag(board_array) == board_array[0, 0]) and board_array[0, 0] != "":
        return board_array[0, 0]
    if all(np.diag(np.fliplr(board_array)) == board_array[0, 2]) and board_array[0, 2] != "":
        return board_array[0, 2]

    # 引き分け判定 (NumPy配列がすべて埋まっているか)
    if not any(board_array == ""):
        return "Draw"

    return None  # 継続


def click_cell(row, col):
    """セルクリック時の処理"""
    if st.session_state.winner is None and st.session_state.board[row, col] == "":
        # 盤面にマークを配置
        st.session_state.board[row, col] = st.session_state.turn

        # 勝敗判定を実行
        result = check_win(st.session_state.board)
        if result is not None:
            st.session_state.winner = result

        # ターンを切り替え
        if st.session_state.winner is None:
            st.session_state.turn = "×" if st.session_state.turn == "○" else "○"


# --- ページ描画 ---
st.title("⭕❌ マルバツゲーム")
st.write(f"現在のターン: **{st.session_state.turn}**")

# マス目の描画
board_container = st.container()
with board_container:
    for row in range(3):
        # gap=None (デフォルト) や gap="small" は使わず、CSSで制御
        cols = st.columns(3)
        for col in range(3):
            mark = st.session_state.board[row, col]

            # 勝敗が決まっていたら、ボタンを非活性化
            is_disabled = st.session_state.winner is not None

            # ボタンに表示する文字 (空白の場合はスペースを入れてボタンの高さを維持)
            display_char = mark if mark != "" else " "

            if cols[col].button(display_char, key=f"{row}_{col}", disabled=is_disabled):
                click_cell(row, col)

# --- 結果表示とリセットボタン ---
if st.session_state.winner is not None:
    if st.session_state.winner == "Draw":
        st.info("引き分けです！")
    else:
        # 添付画像のようなメッセージ表示を模倣
        st.success(f"**{st.session_state.winner}** の勝ち！")

        # 添付画像のOKボタンを模倣
        if st.button("OK"):
            st.session_state.board = np.full((3, 3), "", dtype=str)
            st.session_state.turn = "○"
            st.session_state.winner = None
            st.experimental_rerun()  # リセット後の再描画を強制

# ゲームプレイ中のリセットボタン
if st.session_state.winner is None:
    if st.button("リセット"):
        st.session_state.board = np.full((3, 3), "", dtype=str)
        st.session_state.turn = "○"
        st.session_state.winner = None
        st.experimental_rerun()