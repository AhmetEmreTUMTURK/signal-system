import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000/api"

# Sayfa yapılandırması
st.set_page_config(page_title="Algoritmik Sinyal Paneli", layout="wide")
st.title("Algoritmik Ticaret Sinyal Paneli")

# API'den veri çeken fonksiyonlar
def fetch_prices():
    try:
        response = requests.get(f"{API_URL}/prices?limit=200")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except:
        pass
    return pd.DataFrame()

def fetch_signals():
    try:
        response = requests.get(f"{API_URL}/signals?limit=50")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except:
        pass
    return pd.DataFrame()

df_prices = fetch_prices()
df_signals = fetch_signals()

if not df_prices.empty:
    unique_symbols = df_prices['symbol'].unique()

    selected_symbol = st.selectbox(" Grafiğini İncelemek İstediğiniz Varlığı Seçin:", unique_symbols)

    filtered_prices = df_prices[df_prices['symbol'] == selected_symbol]

    # Ekranı ikiye böl
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"{selected_symbol} - Fiyat Hareketleri")

        if not filtered_prices.empty:
            # Grafiği Sadece Filtrelenmiş Veriyle Çiz
            fig = go.Figure(data=[go.Candlestick(
                x=filtered_prices['date'],
                open=filtered_prices['open'],
                high=filtered_prices['high'],
                low=filtered_prices['low'],
                close=filtered_prices['close']
            )])
            fig.update_layout(xaxis_rangeslider_visible=False, height=500, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Bu sembol için yeterli fiyat verisi yok.")

    with col2:
        st.subheader(f"{selected_symbol} - Otonom Sinyaller")

        if not df_signals.empty:
            # Sinyalleri de seçili sembole göre filtrele
            filtered_signals = df_signals[df_signals['symbol'] == selected_symbol]

            if not filtered_signals.empty:
                display_df = filtered_signals[['date', 'symbol', 'signal_type']]
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_symbol} için henüz üretilmiş bir sinyal yok.")
        else:
            st.warning("Veritabanında henüz sinyal bulunmuyor.")

    st.divider()
    st.subheader(" Tüm Piyasa - Son Sinyal Durumları")

    if not df_signals.empty:
        latest_global_signals = df_signals.drop_duplicates(subset=['symbol'], keep='first')

        display_global_df = latest_global_signals[['date', 'symbol', 'signal_type','rsi','ema_9','ema_21','macd','macd_signal']]
        st.dataframe(display_global_df, use_container_width=True, hide_index=True)
    else:
        st.info("Sistemde gösterilecek herhangi bir sinyal kaydı yok.")

else:
    st.error("Fiyat verisi çekilemedi. FastAPI sunucusunun çalıştığından emin ol.")
#streamlit run app/dashboard.py