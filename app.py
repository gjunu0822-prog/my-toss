import streamlit as st
import yfinance as yf
import pandas as pd

# --- [설정] 본인의 실제 자산 정보를 여기에 입력하세요 ---
MY_CASH = 5000000 # 예: 현금 500만원
MY_STOCKS = {
    "TSLA": 10, # 테슬라 보유 수량
    "NVDA": 5, # 엔비디아 보유 수량
    "PLTR": 100 # 팔란티어 보유 수량
}
# --------------------------------------------------

st.set_page_config(page_title="Minimal Finance", page_icon="💰")

# 테마 스타일 적용 (토스 느낌의 깔끔한 디자인)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #3182f6; color: white; }
    .asset-card { padding: 20px; background-color: white; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_content_html=True)

st.title("자산 현황")
st.caption("쇼핑, 혜택 기능을 제거한 클린 버전")

# 1. 실시간 주가 데이터 불러오기
@st.cache_data(ttl=60) # 1분마다 업데이트
def get_stock_data(tickers):
    data = {}
    for t in tickers:
        stock = yf.Ticker(t)
        data[t] = stock.history(period="1d")['Close'].iloc[-1]
    return data

prices = get_stock_data(list(MY_STOCKS.keys()))

# 2. 총자산 계산
total_stock_value = sum(prices[t] * MY_STOCKS[t] for t in MY_STOCKS)
# 환율 대략 계산 (1350원 기준)
total_asset = MY_CASH + (total_stock_value * 1350)

# 상단 총액 표시
st.subheader(f"총 자산: {total_asset:,.0f}원")
st.divider()

# 3. 계좌 섹션
st.write("### 🏦 계좌")
with st.container():
    st.markdown(f"""
    <div class="asset-card">
        <small>토스뱅크 통장</small><br>
        <strong>{MY_CASH:,.0f}원</strong>
    </div>
    """, unsafe_content_html=True)

st.write("") # 간격

# 4. 주식 섹션
st.write("### 📈 증권 (실시간)")
stock_list = []
for t in MY_STOCKS:
    current_val = prices[t] * MY_STOCKS[t] * 1350
    stock_list.append({
        "종목": t,
        "현재가": f"${prices[t]:.2f}",
        "보유수량": f"{MY_STOCKS[t]}주",
        "평가금액": f"{current_val:,.0f}원"
    })

st.table(pd.DataFrame(stock_list))

if st.button("새로고침"):
    st.rerun ()
