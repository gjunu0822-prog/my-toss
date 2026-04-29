import streamlit as st
import yfinance as yf
import pandas as pd

# --- 자산 설정 ---
MY_CASH = 5000000 
MY_STOCKS = {"TSLA": 10, "NVDA": 5, "PLTR": 100}

st.title("💰 나만의 클린 자산")

# 1. 주가 가져오기
@st.cache_data(ttl=60)
def get_data(tickers):
    d = {}
    for t in tickers:
        try:
            d[t] = yf.Ticker(t).history(period="1d")['Close'].iloc[-1]
        except:
            d[t] = 0
    return d

prices = get_data(list(MY_STOCKS.keys()))

# 2. 총자산 계산
total_stock = sum(prices[t] * MY_STOCKS[t] for t in MY_STOCKS)
total_asset = MY_CASH + (total_stock * 1350)

# 3. 화면 표시
st.metric(label="총 자산(원)", value=f"{total_asset:,.0f}")
st.divider()

st.subheader("🏦 계좌")
st.write(f"토스뱅크: **{MY_CASH:,.0f}원**")

st.subheader("📈 증권 (실시간)")
for t in MY_STOCKS:
    val = prices[t] * MY_STOCKS[t] * 1350
    st.write(f"{t}: ${prices[t]:.2f} ({val:,.0f}원)")

if st.button("새로고침"):
    st.rerun()
