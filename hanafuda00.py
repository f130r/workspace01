def handle_turn_action():
    """
    手札から札を出した後、山札から札を引く処理を含む、ターン処理全体を実行します。
    この関数はプレイヤー1のターンを処理します。
    """
    state = st.session_state['game_state']
    selected_card = st.session_state['selected_hand_card']

    if selected_card is None:
        return

    # 1. 選択した手札をプレイヤーの手札から削除
    # selected_cardはオブジェクトであるため、参照で削除する必要がある
    # card.idを比較することで確実に削除
    state['player1_hand'] = [
        card for card in state['player1_hand'] if card.id != selected_card.id
    ]

    # --- 2. 手札から場へ札を出す処理の実行 ---

    # 処理中の札（手札から出した札）
    temp_played_card = selected_card

    # マッチする場札を探す
    matching_field_cards_hand = [card for card in state['field_cards'] if card.month == temp_played_card.month]

    # 獲得処理（出した札と場札）
    if len(matching_field_cards_hand) >= 1:
        # 簡易版のため、最初のマッチング札を獲得対象とする
        gained_card_hand = matching_field_cards_hand[0]

        # 場札から獲得札を削除
        state['field_cards'].remove(gained_card_hand)

        # 獲得札リストに追加
        state['player1_collected'].append(temp_played_card)
        state['player1_collected'].append(gained_card_hand)
        st.success(f"🎊 **{temp_played_card.name}** が **{gained_card_hand.name}** と組み合わさり、2枚を獲得しました！")

        # この札は獲得されたため、場には出ない
        temp_played_card = None
    else:
        # マッチする札がない場合、手札の札は場に残る（temp_played_cardのまま）
        st.warning(f"❌ **{temp_played_card.name}** は場に残る候補です。")

    # --- 3. 山札から札を引く処理（ターン進行の核心） ---

    if state['yama_fuda']:
        # 山札のトップから1枚引く
        drawn_card = state['yama_fuda'].pop(0)
        st.info(f"🃏 山札から **{drawn_card.name}** が引かれました。")

        # 処理中の札（山札から引いた札）
        temp_drawn_card = drawn_card

        # 場札から、引いた札と同じ月の札があるか探す
        matching_field_cards_yama = [card for card in state['field_cards'] if card.month == temp_drawn_card.month]

        # 獲得処理（引いた札と場札）
        if len(matching_field_cards_yama) >= 1:
            gained_card_yama = matching_field_cards_yama[0]

            state['field_cards'].remove(gained_card_yama)

            # 獲得札リストに追加
            state['player1_collected'].append(temp_drawn_card)
            state['player1_collected'].append(gained_card_yama)

            st.success(
                f"🎉 山札の **{temp_drawn_card.name}** が **{gained_card_yama.name}** と組み合わさり、さらに2枚を獲得！")

            # この札は獲得されたため、場には出ない
            temp_drawn_card = None
        else:
            # マッチする札がない場合、引いた札は場に残る（temp_drawn_cardのまま）
            st.warning(f"⚠️ 山札の札 **{temp_drawn_card.name}** は場に残る候補です。")

        # 場の更新処理（ここで初めて場に追加する）
        # 手札から出した札（獲得されなかった場合）を場に追加
        if temp_played_card:
            state['field_cards'].append(temp_played_card)
            st.warning(
                f"❌ 手札から出した札 **{temp_played_card.name}** が場に残りました。")  # 2重でメッセージが出るため、このメッセージは不要な場合もある

        # 山札から引いた札（獲得されなかった場合）を場に追加
        if temp_drawn_card:
            state['field_cards'].append(temp_drawn_card)
            st.warning(f"⚠️ 山札の札 **{temp_drawn_card.name}** が場に残りました。")  # 2重でメッセージが出るため、このメッセージは不要な場合もある

    # 4. 後処理: ターンを相手（AI）に渡すことを明確にする
    st.session_state['selected_hand_card'] = None
    state['current_turn'] = 2

    # 5. 再描画のトリガー
    # st.rerun() は main() 関数内で押されたボタンによって呼ばれるため、ここでは不要だが、
    # 処理が長くなる場合はユーザーに次のアクションを促すメッセージを入れると良い。
    # 例：st.button("AIのターンへ進む", on_click=lambda: state.update({'current_turn': 2}))