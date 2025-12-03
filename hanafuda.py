import streamlit as st
from hanafuda_logic import ALL_CARDS, HanafudaRule, initialize_game, Card  # 前回定義したロジックをインポート


def init_session_state():
    """
    Streamlitのセッション状態を初期化します。
    """
    if 'game_state' not in st.session_state:
        st.session_state['game_state'] = initialize_game()
        st.session_state['selected_card'] = None  # プレイヤーが選択した手札


def display_card_text(card: Card):
    """
    札の種別に応じて色分けしたテキストで表示します。
    """
    # 札の種別（光、タネ、タン、カス）に応じて色を決定
    if card.type == "光":
        color = "red"
        symbol = "⭐"
    elif card.type == "タネ":
        color = "green"
        symbol = "◎"
    elif card.type == "タン":
        color = "blue"
        symbol = "🎗️"
    else:  # カス
        color = "gray"
        symbol = "⚫"

    st.markdown(
        f"<div style='border: 1px solid {color}; padding: 5px; margin: 2px; text-align: center; border-radius: 5px; background-color: #f0f0f0;'>"
        f"**{symbol} {card.name}**<br><span style='font-size: 0.8em;'>({card.month}月/{card.type})</span>"
        f"</div>",
        unsafe_allow_html=True
    )


def main():
    st.set_page_config(layout="wide")
    st.title("簡易版 Streamlit 花札 🌸")

    # 状態の初期化
    init_session_state()
    state = st.session_state['game_state']

    # --- 1. 場の札の表示 ---
    st.header("場の札 (Field)")
    cols = st.columns(8)  # 場札は8枚なので8列で表示
    for i, card in enumerate(state['field_cards']):
        with cols[i]:
            display_card_text(card)
            # 札を選択した時の処理は後で実装します
            # st.button("選択", key=f"field_{card.id}")

    # --- 2. プレイヤーの手札の表示 ---
    st.header("あなたの手札 (Your Hand)")
    hand_cols = st.columns(8)  # 手札も8枚なので8列
    for i, card in enumerate(state['player1_hand']):
        with hand_cols[i]:
            display_card_text(card)

            # プレイヤーがこの札を選択するボタン
            if st.button("出す", key=f"hand_{card.id}"):
                st.session_state['selected_card'] = card
                st.info(f"'{card.name}' を選択しました。")
                # 次のターン処理（場札との組み合わせ判定）は後で実装します

    # --- 3. 獲得札の表示 ---
    st.header("獲得札 (Collected)")
    # 獲得札はシンプルにリスト表示
    st.write(f"あなた: {len(state['player1_collected'])}枚")
    st.write(f"相手: {len(state['player2_collected'])}枚")

    # --- 4. デバッグ情報 ---
    # st.subheader("デバッグ情報")
    # st.write(st.session_state['game_state'])


if __name__ == "__main__":
    main()

```eof

上記のコードを実行すると、花札ゲームの ** 最低限の画面レイアウト ** が表示されます。

このコードをベースに、次は **「手札から札を出した後の処理（場札との組み合わせ判定と札の獲得）」 ** のロジックを実装していきます。よろしいでしょうか？