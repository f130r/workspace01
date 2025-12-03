import streamlit as st
import random
from hanafuda_logic00 import HanafudaRule, initialize_game, Card, BRIGHT, ANIMAL, RIBBON, JUNK


def init_session_state():
    """Streamlitのセッション状態を初期化します。"""
    if 'game_state' not in st.session_state:
        st.session_state['game_state'] = initialize_game()
        st.session_state['selected_hand_card'] = None  # プレイヤーが選択した手札


def display_card_text(card: Card, key_prefix: str):
    """札の種別に応じて色分けしたテキストで表示します。（画像不使用のため）"""
    # 札の種別に応じて色と記号を決定
    color_map = {
        BRIGHT: ("red", "⭐"),
        ANIMAL: ("green", "◎"),
        RIBBON: ("blue", "🎗️"),
        JUNK: ("gray", "⚫")
    }
    color, symbol = color_map.get(card.type, ("black", "❓"))

    # st.markdown は表示のみに使用し、キーは使用しない
    st.markdown(
        f"<div style='border: 1px solid {color}; padding: 5px; margin: 2px; text-align: center; border-radius: 5px; background-color: #f0f0f0;'>"
        f"**{symbol} {card.name}**<br><span style='font-size: 0.8em;'>({card.month}月/{card.type})</span>"
        f"</div>",
        unsafe_allow_html=True,
        # key=display_key # 👈 この行を削除/コメントアウトします
    )


def handle_turn_action():
    """
    手札から札を出した後、山札から札を引く処理を含む、ターン処理全体を実行します。
    この関数はプレイヤー1のターンを処理します。
    """
    state = st.session_state['game_state']
    selected_card = st.session_state['selected_hand_card']

    # 処理すべき札が選択されていなければ終了
    if selected_card is None:
        return

    # プレイヤーの手札から選択した札を削除
    state['player1_hand'] = [
        card for card in state['player1_hand'] if card.id != selected_card.id
    ]

    # --- 1. 手札から場へ札を出す処理の実行 ---

    temp_played_card: Optional[Card] = selected_card

    # マッチする場札を探す
    matching_field_cards_hand = [card for card in state['field_cards'] if card.month == temp_played_card.month]

    if len(matching_field_cards_hand) >= 1:
        # 簡易版：最初のマッチング札を獲得
        gained_card_hand = matching_field_cards_hand[0]

        # 場札から獲得札を削除
        state['field_cards'].remove(gained_card_hand)

        # 獲得札リストに追加
        state['player1_collected'].append(temp_played_card)
        state['player1_collected'].append(gained_card_hand)
        st.success(f"🎊 **{temp_played_card.name}** が **{gained_card_hand.name}** と組み合わさり、2枚を獲得しました！")

        temp_played_card = None  # 獲得されたため場には出ない
    else:
        st.info(f"👉 手札の札 **{temp_played_card.name}** は場札とマッチしませんでした。")

    # --- 2. 山札から札を引く処理 ---

    temp_drawn_card: Optional[Card] = None

    if state['yama_fuda']:
        drawn_card = state['yama_fuda'].pop(0)
        temp_drawn_card = drawn_card
        st.info(f"🃏 山札から **{drawn_card.name}** が引かれました。")

        # 場札から、引いた札と同じ月の札があるか探す
        matching_field_cards_yama = [card for card in state['field_cards'] if card.month == temp_drawn_card.month]

        if len(matching_field_cards_yama) >= 1:
            gained_card_yama = matching_field_cards_yama[0]

            state['field_cards'].remove(gained_card_yama)

            # 獲得札リストに追加
            state['player1_collected'].append(temp_drawn_card)
            state['player1_collected'].append(gained_card_yama)

            st.success(
                f"🎉 山札の **{temp_drawn_card.name}** が **{gained_card_yama.name}** と組み合わさり、さらに2枚を獲得！")

            temp_drawn_card = None  # 獲得されたため場には出ない
        else:
            st.info(f"👉 山札の札 **{temp_drawn_card.name}** は場札とマッチしませんでした。")

    # --- 3. 場の更新処理（獲得されなかった札を場に追加） ---

    # 手札から出した札（獲得されなかった場合）を場に追加
    if temp_played_card:
        state['field_cards'].append(temp_played_card)
        st.warning(f"❌ 手札から出した札 **{temp_played_card.name}** が場に残りました。")

        # 山札から引いた札（獲得されなかった場合）を場に追加
    if temp_drawn_card:
        state['field_cards'].append(temp_drawn_card)
        st.warning(f"⚠️ 山札の札 **{temp_drawn_card.name}** が場に残りました。")

        # 4. 後処理: ターンを相手（AI）に渡すことを明確にする
    st.session_state['selected_hand_card'] = None
    state['current_turn'] = 2  # 相手ターンへ確実に移行


def display_collected_summary(cards: list[Card], is_player: bool):
    """獲得した札のサマリー（枚数と種類別カウント、点数）を表示する"""
    score_info = HanafudaRule.calculate_score(cards)
    total_score = score_info[0]
    counts = score_info[1]  # 種類別枚数

    if is_player:
        st.write(f"合計枚数: **{len(cards)}枚**")
        st.write(f"合計点数: **{total_score}点**")
    else:
        st.write(f"合計枚数: **{len(cards)}枚**")
        # AIの点数は非表示

    st.markdown("---")
    st.markdown(
        f"**⭐ 光:** {counts[BRIGHT]}枚 / **◎ タネ:** {counts[ANIMAL]}枚 / **🎗️ タン:** {counts[RIBBON]}枚 / **⚫ カス:** {counts[JUNK]}枚"
    )


# -------------------- MAIN --------------------

def main():
    st.set_page_config(layout="wide")
    st.title("簡易版 Streamlit 花札 🌸")

    init_session_state()
    state = st.session_state['game_state']

    # 手札が選択されていたら、獲得処理を実行（ボタンを押した後に実行される）
    handle_turn_action()

    # --- 0. ゲーム情報と山札の表示 (サイドバー) ---
    st.sidebar.header("ゲーム情報")
    st.sidebar.write(f"現在のターン: **{'あなた' if state['current_turn'] == 1 else '相手（AI）'}**")
    st.sidebar.markdown("---")
    st.sidebar.write(f"山札の残り: **{len(state['yama_fuda'])}枚**")
    st.sidebar.write(f"あなたの手札: **{len(state['player1_hand'])}枚**")
    st.sidebar.write(f"相手の手札: **{len(state['player2_hand'])}枚**")
    st.sidebar.markdown("---")

    # --- 1. 場の札の表示 ---
    st.header("場の札 (Field)")

    # 場の札を月ごとにソートして表示
    sorted_field = sorted(state['field_cards'], key=lambda card: card.month)
    num_field_cards = len(sorted_field)

    # 列数を最大12に制限し、動的に調整
    max_cols = min(num_field_cards, 12)
    cols = st.columns(max_cols if max_cols > 0 else 1)

    if num_field_cards > 0:
        for i, card in enumerate(sorted_field):
            with cols[i % max_cols]:  # 12枚を超えたら次の行に表示されるように制御
                display_card_text(card, key_prefix="field")

    # --- 2. プレイヤーの手札の表示 ---
    st.header("あなたの手札 (Your Hand)")

    # プレイヤーの手札を月ごとにソートして表示
    sorted_hand = sorted(state['player1_hand'], key=lambda card: card.month)
    num_hand_cards = len(sorted_hand)
    hand_cols = st.columns(num_hand_cards if num_hand_cards > 0 else 1)

    # ターンチェック
    if state['current_turn'] == 1 and num_hand_cards > 0:
        # プレイヤーのターン: 操作可能
        for i, card in enumerate(sorted_hand):
            with hand_cols[i]:
                # 札の表示
                display_card_text(card, key_prefix="hand")

                # プレイヤーがこの札を選択するボタン
                if st.button("出す", key=f"hand_btn_{card.id}"):
                    st.session_state['selected_hand_card'] = card
                    st.rerun()  # これにより main() が再実行され、handle_turn_action() が動く
    elif state['current_turn'] == 2:
        # 相手（AI）のターン: 処理はhandle_turn_actionで完了しているため、メッセージを表示してプレイヤーのターンに戻す
        st.info("🤖 相手（AI）のターンはスキップされました。あなたの番です。")
        state['current_turn'] = 1  # 処理後にすぐにプレイヤーのターンに戻す
    else:
        st.info("手札がありません。ゲーム終了までお待ちください。")

    # --- 3. 獲得札の表示 ---
    st.header("獲得札 (Collected Cards)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("あなた")
        display_collected_summary(state['player1_collected'], is_player=True)
    with col2:
        st.subheader("相手 (AI)")
        display_collected_summary(state['player2_collected'], is_player=False)

    # --- 4. ゲームオーバー判定 (勝敗結果の表示) ---
    if len(state['player1_hand']) == 0 and len(state['player2_hand']) == 0 and len(state['yama_fuda']) == 0:
        st.header("ゲーム終了！最終結果")
        score1, _ = HanafudaRule.calculate_score(state['player1_collected'])
        score2, _ = HanafudaRule.calculate_score(state['player2_collected'])

        if score1 > score2:
            st.balloons()
            st.success(f"🥳 あなたの勝利です！ ({score1}点 vs {score2}点)")
        elif score2 > score1:
            st.error(f"😞 相手（AI）の勝利です。 ({score1}点 vs {score2}点)")
        else:
            st.info(f"🤝 引き分けです。 ({score1}点 vs {score2}点)")


if __name__ == "__main__":
    main()