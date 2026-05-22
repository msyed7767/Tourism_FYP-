import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

st.set_page_config(
    page_title="Pakistan Tourism Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS ====================
st.markdown("""
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<style>
    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0B1A2E 0%, #1B2F44 50%, #0F1A2A 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1622 0%, #0D1B2A 100%);
        border-right: 1px solid rgba(0, 255, 255, 0.15);
    }
    [data-testid="stSidebar"] * { color: #E8EDF2 !important; }

    .main-title {
        font-size: 2rem; font-weight: 700;
        background: linear-gradient(135deg, #00FFFF 0%, #00B4D8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 10px;
    }
    .subtitle {
        text-align: center; color: #B0C4DE;
        font-size: 0.85rem; margin-bottom: 30px;
    }
    .executive-card {
        background: linear-gradient(135deg, rgba(0,255,255,0.08) 0%, rgba(0,180,216,0.03) 100%);
        border-left: 4px solid #00FFFF; border-radius: 12px;
        padding: 18px 22px; margin: 15px 0;
    }
    .executive-card p { color: #D0D8E0; font-size: 0.9rem; line-height: 1.6; }

    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        backdrop-filter: blur(12px); border-radius: 16px; padding: 20px;
        text-align: center; border: 1px solid rgba(0,255,255,0.25);
        transition: all 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #00FFFF; }
    .kpi-icon {
        font-size: 1.6rem;
        background: linear-gradient(135deg, #00FFFF, #00B4D8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #00FFFF; }
    .kpi-label { font-size: 0.7rem; color: #B0C4DE; letter-spacing: 1px; margin-top: 8px; text-transform: uppercase; }

    .chart-card {
        background: rgba(255,255,255,0.05); border-radius: 16px;
        padding: 18px; margin: 10px 0; border: 1px solid rgba(0,255,255,0.1);
    }
    .chart-title {
        font-size: 1rem; font-weight: 600; color: #00FFFF;
        margin-bottom: 15px; padding-bottom: 8px;
        border-bottom: 2px solid rgba(0,255,255,0.3); display: block;
    }
    .chart-title i { margin-right: 8px; }

    .footer {
        text-align: center; padding: 20px; margin-top: 35px;
        border-top: 1px solid rgba(0,255,255,0.1);
        color: #7A8EA0; font-size: 0.7rem;
    }
    .footer i { margin-right: 4px; color: #00FFFF; }

    .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 10px; }
    .status-green { background-color: #00FF88; box-shadow: 0 0 8px #00FF88; }
    .status-cyan  { background-color: #00FFFF; box-shadow: 0 0 8px #00FFFF; }

    .sidebar-metric {
        background: rgba(0,255,255,0.05); border-radius: 10px;
        padding: 10px 12px; margin: 8px 0; border-left: 2px solid #00FFFF;
    }
    .sidebar-metric .label { font-size: 0.65rem; color: #7A8EA0; text-transform: uppercase; letter-spacing: 1px; }
    .sidebar-metric .label i { margin-right: 5px; color: #00FFFF; }
    .sidebar-metric .value { font-size: 1.2rem; font-weight: bold; color: #00FFFF; }

    [data-testid="stMetric"] { background: rgba(0,255,255,0.08); border-radius: 12px; padding: 15px; }
    [data-testid="stMetric"] label { color: #00FFFF !important; font-weight: 600 !important; }

    .section-header {
        font-size: 0.7rem; color: #00FFFF; margin-bottom: 10px;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .section-header i { margin-right: 6px; }
</style>
""", unsafe_allow_html=True)


# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = [
        os.path.join(base_dir, 'Data', 'raw', 'pakistan_tourism_dataset.csv'),
        os.path.join(base_dir, 'data', 'raw', 'pakistan_tourism_dataset.csv'),
        'Data/raw/pakistan_tourism_dataset.csv',
        'data/raw/pakistan_tourism_dataset.csv',
    ]

    df = None
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break

    if df is None:
        st.warning("CSV not found — showing sample data. Run from TOURISM_FYP root folder.")
        data = {
            'Year': [2015, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Province': ['Punjab', 'Sindh', 'Punjab', 'Balochistan', 'Gilgit-Baltistan',
                         'Khyber Pakhtunkhwa', 'Punjab', 'Sindh', 'Gilgit-Baltistan',
                         'Khyber Pakhtunkhwa', 'Punjab'],
            'City': ['Lahore', 'Karachi', 'Islamabad', 'Ziarat', 'Skardu',
                     'Naran', 'Taxila', 'Hyderabad', 'Fairy Meadows', 'Chitral', 'Murree'],
            'Destination_Type': ['Historical', 'Urban', 'Urban', 'Nature', 'Mountain',
                                  'Nature', 'Historical', 'Cultural', 'Mountain', 'Nature', 'Hill Station'],
            'Domestic_Tourists':      [4500000, 3800000, 2000000, 350000, 800000,
                                        1100000, 500000, 650000, 450000, 550000, 2500000],
            'International_Tourists': [350000, 420000, 500000, 12000, 120000,
                                        60000, 15000, 22000, 90000, 40000, 180000],
            'Peak_Season':  ['Winter', 'Winter', 'Spring', 'Summer', 'Summer',
                             'Summer', 'Winter', 'Winter', 'Summer', 'Summer', 'Summer'],
            'Average_Temperature_C': [18, 22, 20, 14, 9, 12, 19, 25, 7, 11, 13],
            'Average_Cost_USD':      [300, 350, 320, 220, 450, 300, 200, 210, 500, 280, 260],
            'Main_Attraction': ['Badshahi Mosque', 'Clifton Beach', 'Faisal Mosque',
                                'Ziarat Juniper Forest', 'Shangrila Lake', 'Saif-ul-Malook Lake',
                                'Taxila Museum', 'Pakka Qila', 'Nanga Parbat View',
                                'Kalash Valley', 'Mall Road Murree'],
            'Safety_Rating':           [4, 3, 5, 3, 5, 4, 4, 3, 5, 4, 4],
            'Accommodation_Type':      ['Hotels', 'Hotels', 'Hotels', 'Guest Houses', 'Lodges',
                                         'Hotels', 'Hotels', 'Guest Houses', 'Camps', 'Guest Houses', 'Hotels'],
            'Transport_Accessibility': ['High', 'High', 'High', 'Low', 'Medium',
                                         'Medium', 'High', 'Medium', 'Low', 'Low', 'High'],
            'Popularity_Score':        [85, 82, 87, 68, 90, 86, 72, 69, 92, 81, 89],
        }
        df = pd.DataFrame(data)

    df['Total_Tourists'] = df['Domestic_Tourists'] + df['International_Tourists']
    df['Revenue_M'] = ((df['Total_Tourists'] * df['Average_Cost_USD']) / 1_000_000).round(1)

    year_df = (
        df.groupby('Year', as_index=False)
          .agg(
              Domestic_Tourists=('Domestic_Tourists', 'sum'),
              International_Tourists=('International_Tourists', 'sum'),
              Total_Tourists=('Total_Tourists', 'sum'),
              Revenue_M=('Revenue_M', 'sum'),
              Popularity_Score=('Popularity_Score', 'mean'),
          )
    )
    year_df['Total_Tourists_M']         = (year_df['Total_Tourists'] / 1_000_000).round(2)
    year_df['Domestic_Tourists_M']      = (year_df['Domestic_Tourists'] / 1_000_000).round(2)
    year_df['International_Tourists_M'] = (year_df['International_Tourists'] / 1_000_000).round(2)
    year_df['YoY_Growth']               = year_df['Total_Tourists_M'].pct_change() * 100
    year_df['Recovery_Rate']            = (year_df['Total_Tourists_M'] / year_df['Total_Tourists_M'].max()) * 100

    return df, year_df


with st.spinner("Loading tourism data..."):
    df, year_df = load_data()

min_year = int(year_df['Year'].min())
max_year = int(year_df['Year'].max())


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <i class="fas fa-mountain" style="font-size:2.5rem; color:#00FFFF;"></i>
        <div style="font-size:1rem; font-weight:700; margin-top:10px; color:#00FFFF; letter-spacing:1px;">TOURISM ANALYTICS</div>
        <div style="font-size:0.6rem; color:#7A8EA0; letter-spacing:3px; margin-top:4px;">PAKISTAN</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-header"><i class="fas fa-compass"></i> Navigation</div>', unsafe_allow_html=True)
    selected_page = st.radio("", ["Dashboard", "Forecast", "Destinations", "Data"], label_visibility="collapsed")

    st.markdown("---")

    st.markdown('<div class="section-header"><i class="fas fa-calendar-alt"></i> Time Range</div>', unsafe_allow_html=True)
    year_range = st.slider("", min_year, max_year, (min_year, max_year), label_visibility="collapsed")

    st.markdown("---")

    st.markdown('<div class="section-header"><i class="fas fa-chart-bar"></i> Key Metrics</div>', unsafe_allow_html=True)
    latest_year_data = year_df[year_df['Year'] == max_year]
    if not latest_year_data.empty:
        total_m = latest_year_data['Total_Tourists_M'].values[0]
        revenue = latest_year_data['Revenue_M'].values[0]
        st.markdown(f"""
        <div class="sidebar-metric">
            <div class="label"><i class="fas fa-users"></i> Total Tourists ({max_year})</div>
            <div class="value">{total_m:.2f}M</div>
        </div>
        <div class="sidebar-metric">
            <div class="label"><i class="fas fa-dollar-sign"></i> Revenue ({max_year})</div>
            <div class="value">${revenue:.0f}M</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-header"><i class="fas fa-microchip"></i> System Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin:8px 0; font-size:0.8rem;">
        <span class="status-dot status-green"></span>
        <span style="color:#B0C4DE;">Data Active</span>
    </div>
    <div style="margin:8px 0; font-size:0.8rem;">
        <span class="status-dot status-green"></span>
        <span style="color:#B0C4DE;">ML Models Ready</span>
    </div>
    <div style="margin:8px 0; font-size:0.8rem;">
        <span class="status-dot status-cyan"></span>
        <span style="color:#B0C4DE;">Live Dashboard</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="text-align:center; font-size:0.55rem; color:#4A5A6A; letter-spacing:1px;">FYP 2025 &nbsp;|&nbsp; PTDC</div>', unsafe_allow_html=True)


# ---- Filtered data ----
filtered_year = year_df[(year_df['Year'] >= year_range[0]) & (year_df['Year'] <= year_range[1])].copy()
filtered_raw  = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

PLOT_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#FFFFFF',
    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font_color='#00FFFF', tickfont_color='#FFFFFF'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font_color='#00FFFF', tickfont_color='#FFFFFF'),
    legend=dict(font_color='#FFFFFF'),
    height=400,
)


# ==================== DASHBOARD PAGE ====================
if selected_page == "Dashboard":
    st.markdown('<div class="main-title"><i class="fas fa-mountain"></i> Pakistan Tourism Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-chart-line"></i> &nbsp; Real-time Analytics &amp; Business Intelligence</div>', unsafe_allow_html=True)

    if len(filtered_year) > 1:
        latest_t = filtered_year['Total_Tourists_M'].iloc[-1]
        prev_t   = filtered_year['Total_Tourists_M'].iloc[-2]
        growth   = ((latest_t - prev_t) / prev_t) * 100
        best_yr  = filtered_year.loc[filtered_year['Total_Tourists_M'].idxmax(), 'Year']
        best_val = filtered_year['Total_Tourists_M'].max()
        cur_yr   = int(filtered_year['Year'].iloc[-1])

        st.markdown(f"""
        <div class="executive-card">
            <p>
                <i class="fas fa-chart-line" style="color:#00FFFF; margin-right:8px;"></i>
                <strong>EXECUTIVE SUMMARY</strong><br>
                Pakistan's tourism sector is experiencing
                <strong style="color:#00FF88;">{growth:.1f}% YoY growth</strong>
                with <strong style="color:#00FFFF;">{latest_t:.2f}M tourists</strong> in {cur_yr}.
                Best performing year: <strong style="color:#00FFFF;">{int(best_yr)}</strong>
                with <strong style="color:#00FFFF;">{best_val:.2f}M visitors</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    cur_t    = filtered_year['Total_Tourists_M'].iloc[-1] if not filtered_year.empty else 0
    cur_rev  = filtered_year['Revenue_M'].iloc[-1]        if not filtered_year.empty else 0
    g_rate   = filtered_year['YoY_Growth'].iloc[-1]       if len(filtered_year) > 1   else 0
    rec_rate = filtered_year['Recovery_Rate'].iloc[-1]    if not filtered_year.empty else 0

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-users"></i></div>
            <div class="kpi-value">{cur_t:.2f}M</div>
            <div class="kpi-label">Total Tourists</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-arrow-trend-up"></i></div>
            <div class="kpi-value">{g_rate:+.1f}%</div>
            <div class="kpi-label">YoY Growth</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-dollar-sign"></i></div>
            <div class="kpi-value">${cur_rev:.0f}M</div>
            <div class="kpi-label">Revenue</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-rotate"></i></div>
            <div class="kpi-value">{rec_rate:.0f}%</div>
            <div class="kpi-label">Recovery Rate</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart 1
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-chart-line"></i> Tourism Growth Trend (Millions)</span>', unsafe_allow_html=True)
    fig1 = px.line(filtered_year, x='Year', y='Total_Tourists_M', markers=True, template='plotly_dark')
    fig1.update_traces(line_color='#00FFFF', line_width=3, marker_size=10, marker_color='#00FFFF')
    fig1.update_layout(**PLOT_LAYOUT, yaxis_title='Tourists (Millions)', xaxis_title='Year')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-dollar-sign"></i> Revenue Trend (USD Millions)</span>', unsafe_allow_html=True)
    fig2 = px.area(filtered_year, x='Year', y='Revenue_M', template='plotly_dark', color_discrete_sequence=['#00B4D8'])
    fig2.update_layout(**PLOT_LAYOUT, yaxis_title='Revenue (USD Millions)', xaxis_title='Year')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 3
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-chart-bar"></i> Domestic vs International Tourists</span>', unsafe_allow_html=True)
    fig3 = px.bar(filtered_year, x='Year',
                  y=['Domestic_Tourists_M', 'International_Tourists_M'],
                  barmode='group', template='plotly_dark',
                  color_discrete_map={'Domestic_Tourists_M': '#00FFFF', 'International_Tourists_M': '#FF6B6B'},
                  labels={'value': 'Tourists (Millions)', 'variable': 'Type'})
    fig3.update_layout(**PLOT_LAYOUT, yaxis_title='Tourists (Millions)', xaxis_title='Year')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 4
    growth_df = filtered_year[['Year', 'YoY_Growth']].dropna()
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-percent"></i> Year-over-Year Growth Rate</span>', unsafe_allow_html=True)
    fig4 = px.bar(growth_df, x='Year', y='YoY_Growth', template='plotly_dark',
                  color='YoY_Growth', color_continuous_scale='RdYlGn',
                  labels={'YoY_Growth': 'Growth Rate (%)'})
    fig4.update_layout(**PLOT_LAYOUT, yaxis_title='Growth Rate (%)', xaxis_title='Year')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 5
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-rotate"></i> Tourism Recovery Rate (%)</span>', unsafe_allow_html=True)
    fig5 = px.line(filtered_year, x='Year', y='Recovery_Rate', markers=True, template='plotly_dark')
    fig5.update_traces(line_color='#00FF88', line_width=3, marker_size=8)
    fig5.update_layout(**PLOT_LAYOUT, yaxis_title='Recovery Rate (%)', xaxis_title='Year')
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== FORECAST PAGE ====================
elif selected_page == "Forecast":
    st.markdown('<div class="main-title"><i class="fas fa-brain"></i> AI-Powered Forecast 2025–2030</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-microchip"></i> &nbsp; Linear Regression Forecasting Model</div>', unsafe_allow_html=True)

    if len(filtered_year) >= 3:
        X = filtered_year[['Year']].values
        y = filtered_year['Total_Tourists_M'].values

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.arange(2025, 2031).reshape(-1, 1)
        predictions  = model.predict(future_years)
        r2           = model.score(X, y)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model R² Score",  f"{r2:.3f}")
        with col2:
            st.metric("2030 Prediction", f"{predictions[-1]:.2f}M tourists")
        with col3:
            st.metric("Annual Growth",   f"{model.coef_[0]:.3f}M / year")

        st.markdown("---")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_year['Year'], y=filtered_year['Total_Tourists_M'],
            mode='lines+markers', name='Historical Data',
            line=dict(color='#00FFFF', width=3),
            marker=dict(size=10, color='#00FFFF')
        ))
        fig.add_trace(go.Scatter(
            x=future_years.flatten(), y=predictions,
            mode='lines+markers', name='Forecast 2025–2030',
            line=dict(color='#FF6B6B', width=3, dash='dash'),
            marker=dict(size=10, color='#FF6B6B')
        ))
        fig.add_vline(x=2020, line_dash="dash", line_color="orange",
                      annotation_text="COVID-19 Impact", annotation_font_color="orange")
        fig.update_layout(
            title=dict(text="Pakistan Tourism Forecast 2025–2030", font_color='#00FFFF'),
            **PLOT_LAYOUT,
            height=500,
            xaxis_title='Year',
            yaxis_title='Tourists (Millions)',
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown('<span class="chart-title" style="color:#00FFFF; font-size:1rem; font-weight:600;"><i class="fas fa-table"></i> &nbsp; Year-by-Year Forecast Table</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        forecast_table = pd.DataFrame({
            'Year': list(range(2025, 2031)),
            'Predicted Tourists (Millions)': [round(float(p), 2) for p in predictions],
            'Estimated Revenue (USD M)':     [round(float(p) * 1_000_000 * 280 / 1_000_000, 0) for p in predictions],
        })
        st.dataframe(forecast_table, use_container_width=True, hide_index=True)

    else:
        st.warning("Not enough data for forecasting. Need at least 3 years of data.")


# ==================== DESTINATIONS PAGE ====================
elif selected_page == "Destinations":
    st.markdown('<div class="main-title"><i class="fas fa-map-location-dot"></i> Destination Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-magnifying-glass-chart"></i> &nbsp; Explore tourism data by province, city &amp; destination type</div>', unsafe_allow_html=True)

    # Chart 1
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-building-columns"></i> Top Cities by Total Tourists</span>', unsafe_allow_html=True)
    city_df = (filtered_raw.groupby('City', as_index=False)['Total_Tourists']
                .sum().sort_values('Total_Tourists', ascending=False).head(10))
    city_df['Total_Tourists_M'] = (city_df['Total_Tourists'] / 1_000_000).round(2)
    fig_city = px.bar(city_df, x='City', y='Total_Tourists_M', template='plotly_dark',
                      color='Total_Tourists_M', color_continuous_scale='Teal',
                      labels={'Total_Tourists_M': 'Tourists (M)'})
    fig_city.update_layout(**PLOT_LAYOUT, yaxis_title='Tourists (Millions)', xaxis_title='City')
    st.plotly_chart(fig_city, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-map"></i> Tourists by Province</span>', unsafe_allow_html=True)
        prov_df = filtered_raw.groupby('Province', as_index=False)['Total_Tourists'].sum()
        prov_df['Total_Tourists_M'] = (prov_df['Total_Tourists'] / 1_000_000).round(2)
        fig_prov = px.pie(prov_df, values='Total_Tourists_M', names='Province',
                          template='plotly_dark',
                          color_discrete_sequence=px.colors.sequential.Teal)
        fig_prov.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#FFFFFF', height=400)
        st.plotly_chart(fig_prov, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-layer-group"></i> Tourists by Destination Type</span>', unsafe_allow_html=True)
        dest_df = filtered_raw.groupby('Destination_Type', as_index=False)['Total_Tourists'].sum()
        dest_df['Total_Tourists_M'] = (dest_df['Total_Tourists'] / 1_000_000).round(2)
        fig_dest = px.pie(dest_df, values='Total_Tourists_M', names='Destination_Type',
                          template='plotly_dark',
                          color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_dest.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#FFFFFF', height=400)
        st.plotly_chart(fig_dest, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 4
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-shield-halved"></i> Safety Rating vs Popularity Score</span>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered_raw, x='Safety_Rating', y='Popularity_Score',
        color='Destination_Type', size='Total_Tourists',
        hover_data=['City', 'Province', 'Main_Attraction'],
        template='plotly_dark',
        labels={'Safety_Rating': 'Safety Rating (1-5)', 'Popularity_Score': 'Popularity Score'}
    )
    fig_scatter.update_layout(**PLOT_LAYOUT, height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 5
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-money-bill-trend-up"></i> Average Cost (USD) by Destination Type</span>', unsafe_allow_html=True)
    cost_df = filtered_raw.groupby('Destination_Type', as_index=False)['Average_Cost_USD'].mean().round(0)
    fig_cost = px.bar(cost_df, x='Destination_Type', y='Average_Cost_USD',
                      template='plotly_dark', color='Average_Cost_USD',
                      color_continuous_scale='Oranges',
                      labels={'Average_Cost_USD': 'Avg Cost (USD)'})
    fig_cost.update_layout(**PLOT_LAYOUT, yaxis_title='Average Cost (USD)', xaxis_title='Destination Type')
    st.plotly_chart(fig_cost, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 6
    st.markdown('<div class="chart-card"><span class="chart-title"><i class="fas fa-sun"></i> Peak Season Distribution</span>', unsafe_allow_html=True)
    season_df = filtered_raw.groupby('Peak_Season', as_index=False)['Total_Tourists'].sum()
    season_df['Total_Tourists_M'] = (season_df['Total_Tourists'] / 1_000_000).round(2)
    fig_season = px.bar(season_df, x='Peak_Season', y='Total_Tourists_M',
                        template='plotly_dark', color='Peak_Season',
                        color_discrete_sequence=['#00FFFF', '#FF6B6B', '#00FF88', '#FFD700'],
                        labels={'Total_Tourists_M': 'Tourists (M)'})
    fig_season.update_layout(**PLOT_LAYOUT, yaxis_title='Tourists (Millions)', xaxis_title='Peak Season')
    st.plotly_chart(fig_season, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== DATA PAGE ====================
elif selected_page == "Data":
    st.markdown('<div class="main-title"><i class="fas fa-database"></i> Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-table"></i> &nbsp; Raw Tourism Data — All Columns</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Records",     len(filtered_raw))
    with col2: st.metric("Cities",            filtered_raw['City'].nunique())
    with col3: st.metric("Provinces",         filtered_raw['Province'].nunique())
    with col4: st.metric("Destination Types", filtered_raw['Destination_Type'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    provinces = ['All'] + sorted(filtered_raw['Province'].unique().tolist())
    selected_province = st.selectbox("Filter by Province", provinces)
    display_df = filtered_raw if selected_province == 'All' else filtered_raw[filtered_raw['Province'] == selected_province]

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    csv = display_df.to_csv(index=False).encode()
    st.download_button(
        label="Download CSV for Power BI",
        data=csv,
        file_name="pakistan_tourism_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown('<span style="color:#00FFFF; font-size:1rem; font-weight:600;"><i class="fas fa-chart-simple"></i> &nbsp; Quick Statistics</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(display_df.describe().round(2), use_container_width=True)


# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <i class="fas fa-database"></i> Data Source: PTDC | World Bank &nbsp;&nbsp;|&nbsp;&nbsp;
    <i class="fab fa-python"></i> Python &amp; Streamlit &nbsp;&nbsp;|&nbsp;&nbsp;
    <i class="fas fa-brain"></i> ML: Linear Regression &nbsp;&nbsp;|&nbsp;&nbsp;
    <i class="fas fa-graduation-cap"></i> Final Year Project 2025
</div>
""", unsafe_allow_html=True)