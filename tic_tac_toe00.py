import streamlit as st

# --- 1. 初期設定 ---
# 勝利のパターン (インデックス 0-8)
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 行
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 列
    (0, 4, 8), (2, 4, 6)  # 対角線
]


def initialize_game():
    """ゲームの状態を初期化/リセットする"""
    if 'board' not in st.session_state or st.session_state.game_over:
        st.session_state.board = [''] * 9  # 9マスのリスト
        st.session_state.current_player = 'X'
        st.session_state.game_over = False
        st.session_state.winner = None


def check_winner(board):
    """ボードの状態を確認し、勝者または引き分けを判定する"""
    for line in WINNING_LINES:
        if board[line[0]] == board[line[1]] == board[line[2]] and board[line[0]] != '':
            return board[line[0]]  # 勝者 (例: 'X' または 'O')

    # 引き分け判定 (空きマスがない場合)
    if '' not in board:
        return 'Draw'

    return None  # まだ勝敗は決まっていない


# --- 2. クリック時の処理 ---
def handle_click(index):
    """マスがクリックされたときの処理"""
    if st.session_state.game_over or st.session_state.board[index] != '':
        # ゲーム終了後、または既にマークがあるマスはクリックできない
        return

    # ボードを更新
    st.session_state.board[index] = st.session_state.current_player

    # 勝敗判定
    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
    else:
        # プレイヤーを交代
        st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'


# --- 3. UIの構築とメインロジック ---

# ページ設定 (任意)
st.set_page_config(layout="centered")
st.title("✖️🅾️ マルバツゲーム (Streamlit)")

# ゲームの初期化/リセット
initialize_game()

# ボードの描画 (3x3)
# StreamlitではCSSを使わないため、ボタンのサイズやフォントサイズは制限があります。
# 添付画像のように大きなフォントにするには、ボタンのラベルとして大きな文字を使います。
font_size = "40px"
button_style = f"font-size: {font_size}; height: 100px; width: 100%;"  # スタイリングの代替として

# StreamlitのColumns機能を使って3x3のグリッドを作成
# CSSを使用しないため、配置は st.columns に依存します。
for i in range(3):
    # 3列を作成
    cols = st.columns(3)
    for j in range(3):
        index = i * 3 + j
        mark = st.session_state.board[index]

        # ボタンのラベル: 未入力なら空白、入力済みならマーク
        # フォントを大きく見せるために、Markdownでマークアップします。
        label = f"## {mark if mark else ' '}"

        # Streamlitのボタン
        with cols[j]:
            st.button(
                label,
                key=f"cell_{index}",
                on_click=handle_click,
                args=(index,),
                # Streamlitの内部CSSを使わずにサイズを大きく見せる工夫
                # ただし、これはStreamlitの挙動に依存し、完全なCSS制御はできません
                help="Click to place your mark"
            )

# --- 4. 結果の表示 ---
if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.info("✋ 引き分けです！")
    else:
        # 添付画像のようなポップアップではないが、結果を大きく表示
        st.balloons()
        st.success(f"🎉 **{st.session_state.winner}の勝ちです！**")

# --- 5. ゲームのリセットボタン ---
st.markdown("---")
st.button("🔄 新しいゲームを始める", on_click=initialize_game)