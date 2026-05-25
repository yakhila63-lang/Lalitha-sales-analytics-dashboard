import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Lalitha Sales Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
 .main,.stApp, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF!important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: #FFC907!important;
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #1E1E1E!important;
        font-weight: 700;
    }
.kpi-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        padding: 16px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border: 1px solid #E6E6E6;
        height: 100px;
    }
.kpi-card-yellow {
        background: linear-gradient(135deg, #FFF4CC 0%, #FFC907 100%);
        border: none;
    }
.kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #1E1E1E;
        margin: 0;
    }
.kpi-label {
        font-size: 12px;
        color: #666;
        margin: 0;
        text-transform: uppercase;
        font-weight: 600;
    }
.block-container {
        padding-top: 1rem;
        background-color: #FFFFFF;
    }
.stMarkdown, p, h1, h2, h3, h4, h5, h6, div, span {
        color: #1E1E1E!important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("lalitha sales.csv")
    return df

df = load_data()

with st.sidebar:
    st.markdown("# Lalitha Sales")
    st.markdown("### Business Analytics")
    st.markdown("---")
    st.markdown("### FILTER PANEL")
    region = st.multiselect("Region", options=sorted(df["Region"].unique()), default=df["Region"].unique(), label_visibility="collapsed")
    st.caption("Region")
    category = st.multiselect("Category", options=sorted(df["Category"].unique()), default=df["Category"].unique(), label_visibility="collapsed")
    st.caption("Category")

df_filtered = df[df["Region"].isin(region) & df["Category"].isin(category)]

st.markdown("## Lalitha Sales Analytics Dashboard")
st.caption("Real-time Business Performance Overview")

total_sales = df_filtered["Sales"].sum()
avg_sales = df_filtered["Sales"].mean()
total_orders = df_filtered.shape[0]
avg_profit = df_filtered["Profit"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card kpi-card-yellow">
        <p class="kpi-label">TOTAL SALES</p>
        <p class="kpi-value">₹{total_sales/100000:.2f}L</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">AVG SALES</p>
        <p class="kpi-value">₹{avg_sales/1000:.0f}K</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">NO OF ORDERS</p>
        <p class="kpi-value">{total_orders}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">AVG PROFIT</p>
        <p class="kpi-value">₹{avg_profit/1000:.0f}K</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("#### SALES BY REGION")
    fig_donut = px.pie(df_filtered.groupby("Region")["Sales"].sum().reset_index(), values="Sales", names="Region", hole=0.6, color_discrete_sequence=["#FFC907", "#54A24B", "#4C78A8", "#F58518"])
    fig_donut.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
    fig_donut.add_annotation(text=f"₹{total_sales/100000:.2f}L<br>Total", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#1E1E1E")
    fig_donut.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=280, paper_bgcolor='white', plot_bgcolor='white', font_color="#1E1E1E")
    st.plotly_chart(fig_donut, use_container_width=True)
    
    st.markdown("#### SALES BY CATEGORY")
    cat_data = df_filtered.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
    fig_hbar = px.bar(cat_data, x="Sales", y="Category", orientation='h', text_auto='.2s', color_discrete_sequence=["#FFC907"])
    fig_hbar.update_traces(textposition="outside", textfont_size=10)
    fig_hbar.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=300, paper_bgcolor='white', plot_bgcolor='white', font_color="#1E1E1E")
    st.plotly_chart(fig_hbar, use_container_width=True)

with right_col:
    st.markdown("#### SALES TREND")
    trend_data = df_filtered.groupby("Region")["Sales"].sum().reset_index()
    fig_line = px.area(trend_data, x="Region", y="Sales", color_discrete_sequence=["#FFC907"])
    fig_line.update_traces(mode='lines+markers', line=dict(width=3), fill='tozeroy')
    fig_line.update_layout(xaxis_title=None, yaxis_title="Sales (₹)", showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=280, paper_bgcolor='white', plot_bgcolor='white', font_color="#1E1E1E")
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("#### PROFIT DISTRIBUTION")
    funnel_data = df_filtered.groupby("Region")["Profit"].sum().reset_index().sort_values("Profit", ascending=False)
    fig_funnel = px.funnel(funnel_data, x="Profit", y="Region", color_discrete_sequence=["#FFC907", "#FFD966", "#FFE599", "#FFF2CC"])
    fig_funnel.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, paper_bgcolor='white', plot_bgcolor='white', font_color="#1E1E1E")
    st.plotly_chart(fig_funnel, use_container_width=True)

# CATEGORY PERFORMANCE - FIXED
st.markdown("#### CATEGORY PERFORMANCE")
summary_df = df_filtered.groupby("Category").agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    No_of_Orders=('Sales', 'count')
).reset_index()

summary_df["Avg Sales"] = summary_df["Total_Sales"] / summary_df["No_of_Orders"]
summary_df["Margin %"] = (summary_df["Total_Profit"]/summary_df["Total_Sales"]*100).round(1)

summary_df_display = summary_df.copy()
summary_df_display.columns = ["Category", "Total Sales", "Total Profit", "No of Orders", "Avg Sales", "Margin %"]

for col in ["Total Sales", "Total Profit", "Avg Sales"]:
    summary_df_display[col] = summary_df_display[col].apply(lambda x: f"₹{x/1000:.0f}K")

st.dataframe(summary_df_display, use_container_width=True, hide_index=True)