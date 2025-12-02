import streamlit as st
import yfinance as yf
import time
import pandas as pd

# ページ設定
st.set_page_config(page_title="FX Monitor", layout="wide")
st.title("USD/JPY & CAD/JPY リアルタイムレート")

# 1. データ取得関数
def get_rate_data():
    # 1分足のデータを取得
    tickers = ["USDJPY=X", "CADJPY=X"]
    data = yf.download(tickers, period="1d", interval="1m", progress=False)
    return data

# 2. データのロードと整形
df = get_rate_data()

if not df.empty:
    # yfinanceのデータ構造からClose（終値）だけを抽出
    # マルチインデックスの場合の処理
    if isinstance(df.columns, pd.MultiIndex):
        closes = df["Close"]
    else:
        closes = df["Close"] # 単一ティッカー等の場合（念のため）

    # 最新価格の取得
    last_usd = closes["USDJPY=X"].iloc[-1]
    last_cad = closes["CADJPY=X"].iloc[-1]

    # 3. メトリクス表示 (現在のレート)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="USD/JPY", value=f"{last_usd:.2f} 円")
    with col2:
        st.metric(label="CAD/JPY", value=f"{last_cad:.2f} 円")

    # 4. チャート表示
    st.subheader("直近24時間の推移 (1分足)")
    st.line_chart(closes)
else:
    st.error("データの取得に失敗しました。")

# 5. スリープ防止（自動リロード）メカニズム
# 60秒待機してからスクリプトを再実行します
time.sleep(60)
st.rerun()