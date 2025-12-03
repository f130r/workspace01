import streamlit as st
import random
# ファイル名の変更に合わせて、インポート元を修正
from hanafuda_logic00 import ALL_CARDS, HanafudaRule, initialize_game, Card


def init_session_state():
    """Streamlitのセッション状態を初期化します。"""
    if 'game_state' not in st.session_state:
        st.session_state['game_state'] = initialize_game()
        st.session_state['selected_hand_card'] = None  # プレイヤーが選択した手札


def display_card_text(card: Card):
    """札の種別に応じて色分けしたテキストで表示します。（画像不使用のため）"""
    # 札の種別に応じて色と記号を決定
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


def handle_turn_action():
    """
    手札から札を出した後の、組み合わせ判定と札の獲得処理を行います。
    """
    state = st.session_state['game_state']
    selected_card = st.session_state['selected_hand_card']

    if selected_card is None:
        return

    # 1. プレイヤーの手札から選択した札を削除
    state['player1_hand'].remove(selected_card)

    # 2. 場札から、同じ月の札があるか探す
    matching_field_cards = [card for card in state['field_cards'] if card.month == selected_card.month]

    # 3. 札の獲得処理
    if len(matching_field_cards) >= 1:
        # マッチした札の中から獲得する札を決定（ここでは最初に見つかった1枚とする）
        gained_card = matching_field_cards[0]

        # 獲得した札を場札から削除
        state['field_cards'].remove(gained_card)

        # 獲得札リストに追加
        state['player1_collected'].append(selected_card)
        state['player1_collected'].append(gained_card)

        st.success(f"🎊 {selected_card.name} が {gained_card.name} と組み合わさり、2枚を獲得しました！")

    else:
        # マッチする札がない場合、手札の札は場に残る
        state['field_cards'].append(selected_card)
        st.warning(f"❌ {selected_card.name} は場に残りました。")

    # 4. 山札からの自動プレイ（今回は簡易的にスキップ）
    # この後、山札から1枚引いて場に出し、組み合わせ判定をするロジックが本来は必要です。
    # ターンが終了したことを示す
    st.session_state['selected_hand_card'] = None
    state['current_turn'] = 2  # 相手ターンへ


# -------------------- MAIN --------------------

def main():
    st.set_page_config(layout="wide")
    st.title("簡易版 Streamlit 花札 🌸")

    init_session_state()
    state = st.session_state['game_state']

    # 手札が選択されていたら、獲得処理を実行（ボタンを押した後に実行される）
    handle_turn_action()

    # --- 1. 場の札の表示 ---
    st.header("場の札 (Field)")
    cols = st.columns(8)
    for i, card in enumerate(state['field_cards']):
        with cols[i]:
            display_card_text(card)

    # --- 2. プレイヤーの手札の表示 ---
    st.header("あなたの手札 (Your Hand)")

    # ターンチェック（今回はプレイヤー1の操作のみ可能）
    if state['current_turn'] == 1:
        hand_cols = st.columns(8)
        for i, card in enumerate(state['player1_hand']):
            with hand_cols[i]:
                display_card_text(card)

                # プレイヤーがこの札を選択するボタン
                if st.button("出す", key=f"hand_{card.id}"):
                    # 選択した札をセッションに一時保存し、画面更新（リラン）をトリガーする
                    st.session_state['selected_hand_card'] = card
                    st.experimental_rerun()  # これにより main() が再実行され、handle_turn_action() が動く
    else:
        st.info("相手（AI）のターンです。次回の実装でAIのロジックを追加します。")
        # AIターン処理を実装するまで、ここで処理を停止

    # --- 3. 獲得札の表示 ---
    st.header("獲得札 (Collected)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("あなた")
        score, yaku = HanafudaRule.calculate_score(state['player1_collected'])
        st.write(f"枚数: **{len(state['player1_collected'])}枚**")
        st.write(f"点数: **{score}点**")
        # st.write(f"役: {', '.join(yaku)}") # 役の表示は未実装
    with col2:
        st.subheader("相手 (AI)")
        st.write(f"枚数: **{len(state['player2_collected'])}枚**")

    # --- 4. ゲームオーバー判定 ---
    if len(state['player1_hand']) == 0 and len(state['player2_hand']) == 0:
        st.header("ゲーム終了！")
        state['game_over'] = True


if __name__ == "__main__":
    main()


