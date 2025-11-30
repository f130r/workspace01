import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# --- 状態の初期化 ---
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "○"


# --- 関数定義 ---
def check_winner(board):
    """勝敗判定ロジック"""
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 横
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 縦
        [0, 4, 8], [2, 4, 6]  # 斜め
    ]
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    return None


def click_cell(i):
    """セルクリック時の処理"""
    if st.session_state.board[i] == "":
        st.session_state.board[i] = st.session_state.turn
        # ターンを切り替える
        st.session_state.turn = "×" if st.session_state.turn == "○" else "○"


# --- ページ描画 ---

st.title("⭕❌ マルバツゲーム")

# ⭐ StreamlitにカスタムCSSを適用する核心部分 ⭐
# st.markdown()に<style>タグを埋め込み、unsafe_allow_html=Trueで有効化します。
st.markdown("""
<style>
/* 1. ボタン（マス目）のスタイル調整 */
div.stButton > button {
    width: 100px !important; /* マス目の幅 (正方形を保つ) */
    height: 100px !important; /* マス目の高さ */
    font-size: 80px !important; /* マル/バツの文字サイズを大きく */
    padding: 0 !important;
    line-height: 100px !important; /* 文字を垂直中央に */
    text-align: center !important;
    color: #000 !important; /* 文字色を黒に */
    border: 1px solid #000 !important; /* 枠線を黒に */
    background-color: #ffffff !important; /* 背景色を白に (画像により近づける) */
    margin: -1px !important; /* ⭐ マス目間の間隔を詰めるための重要な調整 ⭐ */
    border-radius: 0px !important; /* 角を丸めない */
}

/* 2. st.columnsによって生じるコンテナ間の余白(gap)を詰める */
/* Streamlitが生成するHorizontalBlockコンテナのギャップを0に設定 */
div[data-testid="stHorizontalBlock"] {
    gap: 0px !important;
}

/* 3. 添付画像のメッセージウィンドウを模倣するCSS */
/* 勝利メッセージを画像のようなシンプルなポップアップ風にする */
.stSuccess {
    border: 1px solid #000 !important;
    background-color: #fff !important;
    color: #000 !important;
    padding: 10px !important;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# 3x3のマス表示
winner = check_winner(st.session_state.board)
disabled_state = winner is not None  # 勝者がいる場合はマス目を非活性化

for row in range(3):
    # gap引数を指定せず、CSSの `div[data-testid="stHorizontalBlock"]` で調整
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        # ボタンに表示する文字。空白の場合は半角スペースを表示してボタンの高さを確保
        display_char = st.session_state.board[idx] or " "

        if cols[col].button(display_char, key=f"cell_{idx}", disabled=disabled_state):
            click_cell(idx)

# --- 勝敗判定とメッセージ表示 ---
if winner:
    # 添付画像のようなメッセージウィンドウを模倣
    # Streamlitのst.successを使用し、上記のCSSで見た目を調整
    st.success(f"×の勝ち！" if winner == "×" else f"〇の勝ち！")

    # 添付画像のOKボタンを模倣し、クリックでリセット
    if st.button("OK"):
        st.session_state.board = [""] * 9
        st.session_state.turn = "○"
        st.experimental_rerun()  # 画面をリロード

elif "" not in st.session_state.board:
    st.info("引き分けです！")

# リセットボタン（勝敗決定後のOKボタンと分離）
if st.button("リセット"):
    st.session_state.board = [""] * 9
    st.session_state.turn = "○"
    st.experimental_rerun()