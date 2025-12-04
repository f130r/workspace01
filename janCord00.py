import streamlit as st
import requests
import pandas as pd

# APIのエンドポイント (URL)
OPENBD_API_URL = "https://api.openbd.jp/v1/get"
# Amazon検索リンクのベースURLに変更
AMAZON_SEARCH_URL = "https://www.amazon.co.jp/s?k="

st.title("📚 Streamlit 簡易書籍検索 (JANコード/ISBN利用)")
st.caption("OpenBD API を利用して、実際に出版されている書籍情報を検索します。")

# --- 1. ユーザー入力の改善 ---
raw_input = st.text_input(
    "検索したいJANコード (ISBN 13桁) を入力してください（ハイフン可）",
    max_chars=17,
    placeholder="例: 978-408-780928-2"
)

# ハイフンを除去して検索用のJANコードを生成
jan_input = raw_input.replace('-', '')

# --- 2. 検索実行 ---
if st.button("書籍情報を検索"):
    # 検索前にJANコードの形式をチェック
    if not jan_input.isdigit() or len(jan_input) != 13:
        st.error("❌ 13桁の半角数字（ハイフンを含まない場合）でJANコード（ISBN）を入力してください。")
    else:
        with st.spinner('データを検索中...'):
            try:
                # APIリクエストの実行
                response = requests.get(OPENBD_API_URL, params={"isbn": jan_input})
                response.raise_for_status()  # HTTPエラーチェック

                data = response.json()

                if data and data[0] is not None:
                    book_info = data[0]

                    # 3. Amazon検索リンクを生成（最も確実）
                    amazon_search_link = f"{AMAZON_SEARCH_URL}{jan_input}"

                    st.success(f"✅ 検索成功！ (ISBN: {jan_input})")

                    # クリック可能なリンクとして表示
                    st.markdown(f"### 🛍️ [Amazonでこの商品を見る]({amazon_search_link})")
                    st.markdown("---")

                    # 必要な情報を抽出 (省略)
                    summary = {
                        "タイトル": book_info.get("summary", {}).get("title", "N/A"),
                        "著者": book_info.get("summary", {}).get("author", "N/A"),
                        "出版社": book_info.get("summary", {}).get("publisher", "N/A"),
                        "出版日": book_info.get("summary", {}).get("pubdate", "N/A"),
                        "ISBN": book_info.get("summary", {}).get("isbn", jan_input)
                    }

                    # 情報をDataFrameにして表示
                    df = pd.DataFrame(list(summary.items()), columns=['項目', '情報'])
                    st.dataframe(df.set_index('項目'), use_container_width=True)

                else:
                    st.warning(f"⚠️ JANコード: {jan_input} に一致する書籍情報が見つかりませんでした。")

            except requests.exceptions.RequestException as e:
                st.error(f"接続エラーが発生しました: {e}")
            except Exception as e:
                st.error(f"予期せぬエラーが発生しました: {e}")

# デモ用ISBN (検索に使えるコード)
st.sidebar.subheader("デモ用コード (ISBN)")
st.sidebar.code("9784087809282")
