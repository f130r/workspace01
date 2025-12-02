import streamlit as st
import yfinance as yf
import time
import pandas as pd
import plotly.express as px  # Plotlyは縦軸最適化のため引き続き必要です

# ページ設定
st.set_page_config(page_title="USD/JPY Monitor", layout="wide")
st.title("USD/JPY リアルタイムレート")

# 1. データ取得関数
def get_rate_data():
    # 修正点: USD/JPY のみを取得
    tickers = ["USDJPY=X"]
    # 期間を5日間に、間隔を1時間に変更
    df = yf.download(tickers, period="5d", interval="1h", progress=False)

    if df.empty:
        return pd.DataFrame()

    return df

# 2. データのロードと整形
df = get_rate_data()

if not df.empty:
    # 修正点: シングルティッカーのため、'Close'列は Pandas Series となります
    closes = df["Close"]

    # 最新価格の取得
    # 修正点: シングルティッカーのため、キー指定は不要
    last_usd = closes.iloc[-1]

    # データのタイムゾーンを日本時間(JST)に変換して表示
    latest_timestamp = closes.index[-1].tz_convert('Asia/Tokyo').strftime('%Y-%m-%d %H:%M:%S')

    st.subheader("📊 データ鮮度チェック")
    st.markdown(f"**最終データ取得日時 (JST):** `{latest_timestamp}`")
    st.caption("取得データの最終5行:")
    st.dataframe(closes.tail(5))

    # 3. メトリクス表示 (現在のレート)
    st.metric(label="USD/JPY", value=f"{last_usd:.2f} 円")
    # CAD/JPY のメトリクス表示は削除

    # 4. チャート表示
    st.subheader("直近5日間の推移 (1時間足) - 縦幅ズーム済み")

    # 1. Plotly用にデータを整形 (シングルティッカーのため melt は不要、列名を明確化)
    plot_df = closes.reset_index()
    plot_df.columns = ['Date', 'Rate'] # 列名を 'Date' と 'Rate' に強制的に設定

    # 2. 最新価格を取得し、Y軸の範囲を決定
    # 最新のレートから±0.5円の範囲にズームする
    y_min = max(0, last_usd - 0.5)
    y_max = last_usd + 0.5

    # 3. Plotlyでチャートを作成
    # 修正点: colorパラメーターを削除
    fig = px.line(
        plot_df,
        x='Date',
        y='Rate',
        title='USD/JPY レート推移',
        labels={'Rate': 'レート (円)', 'Date': '日時'}
    )

    # 4. Y軸の範囲を固定してズームイン
    fig.update_yaxes(range=[y_min, y_max])
    fig.update_layout(hovermode="x unified")

    # 5. Streamlitに表示
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("データの取得に失敗しました。")

# 5. スリープ防止（自動リロード）メカニズム
time.sleep(60)
st.rerun()