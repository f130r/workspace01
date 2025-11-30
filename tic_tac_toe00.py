import streamlit as st

# ページの基本設定
st.set_page_config(page_title="マルバツゲーム", layout="centered")

# --- カスタムCSSの適用 (見た目の再現) ---
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
# 盤面を9要素のフラットなリストとして管理します
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "○"
if "winner" not in st.session_state:
    st.session_state.winner = None


# --- ロジック関数 ---
def check_win(board):
    """標準Pythonリストを使って勝敗を判定 (インデックス0〜8)"""

    # 勝利の組み合わせ
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 横
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 縦
        [0, 4, 8], [2, 4, 6]  # 斜め
    ]

    for a, b, c in wins:
        # 3つすべてが同じマークで、かつ空でない場合
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]  # 勝者を返す

    # 引き分け判定 (すべてのマスが埋まっているか)
    if "" not in board:
        return "Draw"

    return None  # 継続


def click_cell(index):
    """セルクリック時の処理 (indexは0〜8)"""
    if st.session_state.winner is None and st.session_state.board[index] == "":

        # 盤面にマークを配置
        st.session_state.board[index] = st.session_state.turn

        # 勝敗判定を実行
        result = check_win(st.session_state.board)
        if result is not None:
            st.session_state.winner = result

        # ターンを切り替え (勝者がいない場合のみ)
        if st.session_state.winner is None:
            st.session_state.turn = "×" if st.session_state.turn == "○" else "○"


def reset_game():
    """ゲームを初期状態に戻す"""
    st.session_state.board = [""] * 9
    st.session_state.turn = "○"
    st.session_state.winner = None
    st.experimental_rerun()


# --- ページ描画 ---
st.title("⭕❌ マルバツゲーム")
st.write(f"現在のターン: **{st.session_state.turn}**")

# マス目の描画
board_container = st.container()
with board_container:
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            # 0〜8のインデックスを計算
            index = row * 3 + col
            mark = st.session_state.board[index]

            # 勝敗が決まっていたら、ボタンを非活性化
            is_disabled = st.session_state.winner is not None

            # ボタンに表示する文字 (空白の場合はスペースを入れてボタンの高さを維持)
            display_char = mark if mark != "" else " "

            # ボタンのクリック処理
            if cols[col].button(display_char, key=f"cell_{index}", disabled=is_disabled):
                click_cell(index)

# --- 結果表示とリセットボタン ---
if st.session_state.winner is not None:
    if st.session_state.winner == "Draw":
        st.info("引き分けです！")
    else:
        # 添付画像のようなメッセージ表示を模倣: "×の勝ち！"
        st.success(f"**{st.session_state.winner}** の勝ち！")

        # 添付画像のOKボタンを模倣し、クリックでリセット
        if st.button("OK", key="reset_ok"):
            reset_game()

# ゲームプレイ中のリセットボタン (勝敗決定後のOKボタンと分離)
else:
    if st.button("リセット", key="reset_playing"):
        reset_game()