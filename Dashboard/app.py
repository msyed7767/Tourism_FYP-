import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Tourism Pakistan", layout="wide")

# Title
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
[data-testid="stSidebar"] { background: #0B1120; }
.main-title { font-size: 2rem; font-weight: bold; text-align: center; color: #FFD700; }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD DATA ====================
@st.cache_data
def load_data():
    # Try multiple paths for Streamlit Cloud
    possible_paths = [
        'Data/raw/pakistan_tourism_dataset.csv',
        'data/raw/pakistan_tourism_dataset.csv',
        'pakistan_tourism_dataset.csv',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df, path
    
    # Agar koi CSV nahi milti to sample data
    st.warning("⚠️ Dataset not found! Using sample data.")
    data = {
        'Year': list(range(2015, 2025)),
        'Domestic_Tourists': [12.5, 13.2, 14.1, 15.0, 16.2, 3.5, 4.2, 8.5, 10.2, 13.5],
        'International_Tourists': [1.8, 1.9, 2.1, 2.2, 2.0, 0.4, 0.6, 1.2, 1.6, 2.3],
        'Revenue_USD_M': [850, 890, 950, 1020, 1100, 220, 310, 580, 780, 1050],
    }
    df = pd.DataFrame(data)
    df['Total_Tourists_M'] = df['Domestic_Tourists'] + df['International_Tourists']
    return df, "Sample Data"

df, source = load_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🏔️ TOURISM PAKISTAN")
    st.markdown("---")
    page = st.radio("Menu", ["Dashboard", "Forecast", "Data"])
    st.markdown("---")
    st.caption(f"Data Source: {source}")

# ==================== DASHBOARD ====================
if page == "Dashboard":
    st.markdown('<div class="main-title">🇵🇰 Pakistan Tourism Analytics</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    current = df['Total_Tourists_M'].iloc[-1]
    avg_rev = df['Revenue_USD_M'].mean()
    
    with col1:
        st.metric("Total Tourists", f"{current:.1f}M")
    with col2:
        st.metric("Avg Revenue", f"${avg_rev:.0f}M")
    with col3:
        st.metric("Years Data", f"{len(df)}")
    
    # Chart
    fig = px.line(df, x='Year', y='Total_Tourists_M', markers=True, 
                  title="Tourism Growth Trend", template='plotly_dark')
    fig.update_traces(line_color='#FFD700', line_width=3)
    st.plotly_chart(fig, use_container_width=True)

# ==================== FORECAST ====================
elif page == "Forecast":
    st.markdown('<div class="main-title">🔮 Forecast 2025-2030</div>', unsafe_allow_html=True)
    
    from sklearn.linear_model import LinearRegression
    
    X = df[['Year']].values
    y = df['Total_Tourists_M'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    future = np.arange(2025, 2031).reshape(-1, 1)
    pred = model.predict(future)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("2030 Prediction", f"{pred[-1]:.1f}M")
    with col2:
        st.metric("Annual Growth", f"{model.coef_[0]:.2f}M")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Total_Tourists_M'], 
                             mode='lines+markers', name='Historical'))
    fig.add_trace(go.Scatter(x=future.flatten(), y=pred, 
                             mode='lines+markers', name='Forecast',
                             line=dict(dash='dash', color='orange')))
    fig.update_layout(title="Tourism Forecast", template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

# ==================== DATA PAGE ====================
elif page == "Data":
    st.markdown('<div class="main-title">📊 Dataset</div>', unsafe_allow_html=True)
    st.dataframe(df)
    
    csv = df.to_csv(index=False).encode()
    st.download_button("Download CSV", csv, "tourism_data.csv", "text/csv")

st.markdown("---")
st.caption("Pakistan Tourism Analytics | Final Year Project 2025")