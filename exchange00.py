import streamlit as st
import yfinance as yf
import time
import pandas as pd
import plotly.express as px

# ページ設定
st.set_page_config(page_title="FX Monitor", layout="wide")
st.title("USD/JPY & CAD/JPY リアルタイムレート")

# 1. データ取得関数
def get_rate_data():
    # データを確実に動かすために、期間を5日間に、間隔を1時間に変更
    tickers = ["USDJPY=X", "CADJPY=X"]
    df = yf.download(tickers, period="5d", interval="1h", progress=False)

    if df.empty:
        return pd.DataFrame()

    return df

# 2. データのロードと整形
df = get_rate_data()

if not df.empty:
    # --- 修正点: データ処理の簡略化 ---
    # マルチインデックスから終値（Close）だけを抽出。エラー回避のためiloc[-1]は使用しない
    closes = df["Close"]

    # 最新価格の取得
    last_usd = closes["USDJPY=X"].iloc[-1]
    last_cad = closes["CADJPY=X"].iloc[-1]

    # データのタイムゾーンを日本時間(JST)に変換して表示
    latest_timestamp = closes.index[-1].tz_convert('Asia/Tokyo').strftime('%Y-%m-%d %H:%M:%S')

    st.subheader("📊 データ鮮度チェック")
    st.markdown(f"**最終データ取得日時 (JST):** `{latest_timestamp}`")
    st.caption("取得データの最終5行:")
    st.dataframe(closes.tail(5))

    # 3. メトリクス表示 (現在のレート)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="USD/JPY", value=f"{last_usd:.2f} 円")
    with col2:
        st.metric(label="CAD/JPY", value=f"{last_cad:.2f} 円")

    import plotly.express as px  # <<< この行をファイルの先頭に追加

    # ... (中略) ...

    # 4. チャート表示
    st.subheader("直近5日間の推移 (1時間足) - 縦幅ズーム済み")

    # 1. Plotly用にデータを整形 (USDJPY=XとCADJPY=Xを一つの列にまとめる)
    plot_df = closes.reset_index().melt(id_vars='index', var_name='Currency', value_name='Rate')

    # 2. 最新価格を取得し、Y軸の範囲を決定
    # 最新のレートから±0.5円の範囲にズームする
    latest_rate = max(last_usd, last_cad)
    y_min = max(0, latest_rate - 0.5)
    y_max = latest_rate + 0.5

    # 3. Plotlyでチャートを作成
    fig = px.line(
        plot_df,
        x='Date',
        y='Rate',
        color='Currency',
        title='USD/JPY と CAD/JPY の比較',
        labels={'Rate': 'レート (円)', 'Date': '日時'}
    )

    # 4. Y軸の範囲を固定してズームイン
    fig.update_yaxes(range=[y_min, y_max])
    fig.update_layout(hovermode="x unified")  # マウスオーバーで全データを表示

    # 5. Streamlitに表示
    st.plotly_chart(fig, use_container_width=True)  # <<< st.line_chartからの変更点
else:
    st.error("データの取得に失敗しました。")

# 5. スリープ防止（自動リロード）メカニズム
# 60秒待機してからスクリプトを再実行します
time.sleep(60)
st.rerun()