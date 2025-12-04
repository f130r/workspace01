import streamlit as st

# 1. 簡易的な商品データベース（JANコードと商品のマッピング）を作成
# 実際にはCSVファイルやデータベースから読み込みます。
JAN_DATABASE = {
    "4901234567890": {
        "商品名": "特選コーヒー豆ブレンドA 200g",
        "カテゴリ": "飲料・食品",
        "メーカー": "山川食品",
        "価格": 1280
    },
    "4998765432109": {
        "商品名": "超音波式加湿器 S-100",
        "カテゴリ": "家電製品",
        "メーカー": "未来テクノロジー",
        "価格": 4980
    },
    "4500000000001": {
        "商品名": "高級ノート B5サイズ 100枚",
        "カテゴリ": "文房具",
        "メーカー": "文具のタナカ",
        "価格": 350
    },
    # ダミーデータとして、別のコードも追加
    "4911122233445": {
        "商品名": "プレミアムチョコレート 10個入",
        "カテゴリ": "菓子",
        "メーカー": "甘味堂",
        "価格": 550
    }
}


def jan_lookup(jan_code):
    """
    JANコードをデータベースで検索し、結果を返す関数。
    """
    # 入力が13桁の数字でない場合はエラーを返す
    if not jan_code.isdigit() or len(jan_code) != 13:
        return None, "JANコードは13桁の半角数字で入力してください。"

    # データベースから情報を取得
    if jan_code in JAN_DATABASE:
        return JAN_DATABASE[jan_code], None
    else:
        return None, f"JANコード: {jan_code} に一致する商品が見つかりませんでした。"


# --- Streamlit アプリケーションの構築 ---

st.title("🛒 簡易 JANCORD 検索シミュレーター")
st.caption("13桁のJANコードを入力し、商品情報を検索します。")

# 2. ユーザーからの入力フォーム
jan_input = st.text_input(
    "JANコードを入力してください (例: 4901234567890)",
    max_chars=13
)

# 3. 検索ボタン
if st.button("検索"):
    if jan_input:
        # 検索関数の実行
        item_data, error_message = jan_lookup(jan_input)

        st.subheader("検索結果")

        if item_data:
            # 検索成功時
            st.success(f"✅ 商品が見つかりました！ (JAN: {jan_input})")

            # 商品情報をテーブル形式で表示
            data_list = list(item_data.items())
            st.table(data_list)

            # 価格情報を強調表示
            price = item_data.get("価格", "N/A")
            st.markdown(f"#### **税込価格**: ¥{price} (税抜き価格ではありません)")

        else:
            # 検索失敗時や入力エラー時
            st.error(f"❌ 検索失敗: {error_message}")
    else:
        st.warning("JANコードを入力してから検索ボタンを押してください。")

# 4. デモ用のJANコード表示
st.sidebar.subheader("デモ用JANコード")
st.sidebar.code("4901234567890")
st.sidebar.code("4998765432109")