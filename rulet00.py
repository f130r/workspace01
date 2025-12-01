import streamlit as st
from PIL import Image
import random
import time
import io

# 1. ルーレット画像を読み込む（ご提示の画像を 'roulette_base.png' として保存したと仮定）
#    ※ 実際にはユーザーに画像をアップロードしてもらう仕組みも可能です。
try:
    base_image = Image.open("roulette_base.png")
except FileNotFoundError:
    st.error(
        "画像を読み込めませんでした。ファイル名を 'roulette_base.png' にして実行ファイルと同じディレクトリに置いてください。")
    st.stop()

# 2. 当たり判定と回転角度の定義
# （この例では6等分で、角度は画像の中心から時計回り）
OPTIONS = ["イギリス", "オランダ", "アメリカ", "カナダ", "ドイツ", "オーストラリア"]
DEGREES_PER_OPTION = 360 / len(OPTIONS)


def get_winning_angle(winning_option_index):
    # 当たりセクションの中央を指す角度を計算
    # 最初のセクションの開始位置を考慮して計算します
    base_angle = winning_option_index * DEGREES_PER_OPTION
    center_angle = base_angle + (DEGREES_PER_OPTION / 2)
    # PILのrotateは反時計回りなので、360から引く
    return 360 - center_angle


st.title("🎲 Streamlit動的ルーレット")

# プレースホルダーの準備
image_placeholder = st.empty()
progress_placeholder = st.empty()

# 初期画像の表示
image_placeholder.image(base_image, use_column_width=True)

if st.button("ルーレットを回す！"):
    # 3. 結果の決定
    winning_index = random.randrange(len(OPTIONS))
    winning_label = OPTIONS[winning_index]

    # 4. アニメーション（回転演出）
    with progress_placeholder.container():
        st.subheader("ルーレット回転中...")
        progress_bar = st.progress(0)

        # 演出のステップ数と時間
        animation_steps = 20
        total_time = 2.0  # 2秒間の回転演出
        delay = total_time / animation_steps

        for step in range(animation_steps):
            # プログレスバーの更新
            progress_bar.progress(int((step + 1) / animation_steps * 100))

            # 回転角度の計算（演出として大きく回転させ、徐々に減速するような動きも可能）
            # ここではシンプルに、徐々に最終角度に近づくように計算
            # ※ 実際には、高速で何度も回っているように見せるため、ランダムな角度や加速・減速の計算が必要

            current_rotation = (step * 50) + random.randint(0, 30)  # 演出用のランダムな回転
            rotated_img = base_image.rotate(current_rotation, resample=Image.BICUBIC, expand=False)

            image_placeholder.image(rotated_img, use_column_width=True)
            time.sleep(delay)

    # 5. 最終結果の表示（画像を固定し、ポインターを当てる）
    final_angle = get_winning_angle(winning_index)

    # 最後に、決定した角度に正確に回転させて表示
    final_rotated_img = base_image.rotate(final_angle, resample=Image.BICUBIC, expand=False)

    # プログレスバーと「回転中」のテキストをクリア
    progress_placeholder.empty()
    image_placeholder.image(final_rotated_img, use_column_width=True)

    st.success(f"🎊 当たりは **{winning_label}** です！")