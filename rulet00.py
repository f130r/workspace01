import streamlit as st
import random
import time


def run_roulette(options, duration=1.5):
    """
    ルーレットを回すアニメーションを実行し、結果を返す
    """
    # 状態の初期化
    st.session_state.result = None
    st.session_state.spinning = True

    # 1. 最終結果をランダムに決定
    final_choice = random.choice(options)

    # 2. アニメーション表示用のプレースホルダー
    # st.empty()は、その場所の内容を動的に更新するために使用
    status_text = st.empty()

    # 3. アニメーションの実行
    start_time = time.time()

    # 短い時間で高速に表示を切り替える (スピニング演出)
    while time.time() - start_time < duration:
        current_spin = random.choice(options)
        status_text.markdown(f"## 🌀 **Spinning...** 🎯 **{current_spin}**")
        time.sleep(0.05)

        # 4. 最終結果に近づくための「減速演出」
    for delay in [0.2, 0.4, 0.6]:
        status_text.markdown(f"## ⏳ **Slowing Down...** 🎯 **{final_choice}**")
        time.sleep(delay)

        # 5. 最終結果の表示とセッションステートの更新
    status_text.markdown(f"## 🎉 **Result!** 🎉 **{final_choice}**")

    # セッションステートを更新して、メインルーチンの結果表示セクションを有効にする
    st.session_state.result = final_choice
    st.session_state.spinning = False

    # st.experimental_rerun() を削除しました
    # 関数が終了し、Streamlitが再実行されるのを待ちます


# --- Streamlit UI設定 ---

st.set_page_config(page_title="Streamlit Roulette", layout="centered")
st.title("🎰 シンプルなルーレットアプリ")

# 1. セッションステートの初期化
if 'options_input' not in st.session_state:
    st.session_state.options_input = "当たり, ハズレ, 大当たり, 再挑戦"
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'result' not in st.session_state:
    st.session_state.result = None

# 2. 選択肢の入力エリア
st.subheader("📝 選択肢の入力")
options_text = st.text_area(
    "カンマ区切りでルーレットの選択肢を入力してください:",
    value=st.session_state.options_input,
    height=100,
    key="options_area",
    help="例: 当たり, ハズレ, 大当たり, 再挑戦"
)
st.session_state.options_input = options_text
options = [opt.strip() for opt in options_text.split(',') if opt.strip()]

st.markdown("---")

# 3. ルーレットの実行ボタン
st.subheader("🔄 ルーレット開始")

if not options:
    st.error("選択肢をカンマ区切りで入力してください。")
else:
    # スピンボタン。回転中は無効化
    # `run_roulette`は、st.buttonが押された際に実行されます
    if st.button("スピン！", disabled=st.session_state.spinning or not options):
        run_roulette(options)

    # 4. 現在の選択肢リストの表示
    st.info(f"現在の選択肢: **{', '.join(options)}**")

# 5. 結果表示エリア (st.session_state.resultが更新された後に表示される)
if st.session_state.result and not st.session_state.spinning:
    st.balloons()
    st.subheader("✨ 結果発表 ✨")
    st.success(f"選ばれたのは... **{st.session_state.result}** です！")

# 6. リセットボタン
if st.button("リセット"):
    st.session_state.result = None
    st.session_state.spinning = False
    # リセット時に状態をクリアするため、再実行は必要
    st.rerun()