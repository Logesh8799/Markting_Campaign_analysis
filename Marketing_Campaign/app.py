import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# 1. Page Config & Layout
st.set_page_config(page_title="Executive Customer Analytics", layout="wide")
st.title("🎯 Consolidated Customer Analytics Solution")
st.markdown("### Strategic insights across customer profiles, campaign acceptance, and channels.")

# 2. Secure Connection to MySQL Database
@st.cache_data
def load_data_from_db():
    DB_USER = "root"
    DB_PASSWORD = "Iyal@244"
    DB_HOST = "127.0.0.1"
    DB_PORT = "3306"
    DB_NAME = "marketing_campaign"
    # Replace with your actual database credentials from your setup step
    encoded_password = quote_plus(DB_PASSWORD)
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string, pool_pre_ping=True)
    query = "SELECT * FROM customers_spend"
    return pd.read_sql(query, con=engine)

# Fallback to CSV if your local MySQL server is offline during testing
try:
    df = load_data_from_db()
except Exception:
    df = pd.read_csv(r"C:\Users\My Lap\OneDrive\Desktop\Marketing_Campaign\segmented_data.csv")

# ==========================================
# MANDATORY EXECUTIVE FILTERS (Sidebar)
# ==========================================
st.sidebar.header("🕹️Filter Options")

def create_filter(label, column_name):
    options = sorted(df[column_name].dropna().unique())
    selected = st.sidebar.multiselect(f"{label}", options, default=options)
    return selected

selected_country = create_filter("Country", "Country")
selected_education = create_filter("Education", "Education")
selected_marital = create_filter("Marital Status", "Marital_Status")
selected_age_band = create_filter("Age Band", "Segment_Young_Customer")
selected_income_band = create_filter("Income Band", "Segment_High_Income")

# Filter dataset dynamically
filtered_df = df[
    (df["Country"].isin(selected_country)) &
    (df["Education"].isin(selected_education)) &
    (df["Marital_Status"].isin(selected_marital)) &
    (df["Segment_Young_Customer"].isin(selected_age_band)) &
    (df["Segment_High_Income"].isin(selected_income_band))
]

# ==========================================
# EXECUTIVE STRATEGIC TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "👑 Profile: Who are our Best Customers?", 
    "📣 Campaigns: What Drives Acceptance?", 
    "🏪 Channels: Segment Behavior Across Touchpoints"
])

# ------------------------------------------
# TAB 1: BEST CUSTOMERS PROFILE
# ------------------------------------------
with tab1:
    st.subheader("High-Value Segment Analysis (Top 10% Spenders)")
    
    col1, col2 = st.columns(2)
    with col1:
        # Donut Chart: Where do our highest spenders sit across income bands?
        high_spenders = filtered_df[filtered_df["Segment_High_Spender"].str.startswith("> ₹", na=False)]
        fig_profile = px.pie(
            high_spenders, names="Segment_High_Income", hole=0.4,
            title="Income Distribution of High-Value Spenders",
            template="plotly_white"
        )
        st.plotly_chart(fig_profile, use_container_width=True)
        
    with col2:
        # Box plot: Tenure days of top spenders vs normal spenders
        fig_tenure = px.box(
            filtered_df, x="Segment_High_Spender", y="Customer_Tenure_Months",
            color="Segment_High_Spender", title="Distribution of Customer Relationship Length Across Spending Tiers",
            labels={"Segment_High_Spender": "Spender Tier", "Customer_Tenure_Months": "Months Registered"},
            template="plotly_white"
        )
        st.plotly_chart(fig_tenure, use_container_width=True)

# ------------------------------------------
# TAB 2: CAMPAIGN ACCEPTANCE DRIVERS
# ------------------------------------------
with tab2:
    st.subheader("Evaluating What Triggers a Positive Response")
    
    col1, col2 = st.columns(2)
    with col1:
        # Grouped bar: Campaign response split by Family Status
        fig_camp_fam = px.histogram(
            filtered_df, x="Segment_Family_Customer", color="Segment_Campaign_Responder",
            barmode="group", title="Campaign Acceptance: Family Customers vs Single Profiles",
            labels={"Segment_Family_Customer": "Has Children Group", "Segment_Campaign_Responder": "Accepted Offer? (1=Yes)"},
            template="plotly_white"
        )
        st.plotly_chart(fig_camp_fam, use_container_width=True)
        
    with col2:
        fig_camp_spend = px.density_heatmap(
            filtered_df, 
            x="Income", 
            y="Total_Spend", 
            facet_col="Segment_Campaign_Responder", # Splits into two side-by-side comparison panels
            title="Concentration of Income vs. Spend: Non-Responders vs. Responders",
            labels={"Income": "Annual Income (₹)", "Total_Spend": "Total Expenditure (₹)"},
            template="plotly_white"
        )
        st.plotly_chart(fig_camp_spend, use_container_width=True)   
# ------------------------------------------
# TAB 3: CHANNELS & PRODUCT BEHAVIOR
# ------------------------------------------
with tab3:
    st.subheader("Where Segments Interact: Web Engagement Deep Dive")
    
    # Heatmap style layout: Comparing Web Visits across Age Groups vs Income Bands
    pivot_df = filtered_df.groupby(["Segment_Young_Customer", "Segment_High_Income"])["NumWebVisitsMonth"].mean().reset_index()
    
    fig_channel = px.bar(
        pivot_df, x="Segment_High_Income", y="NumWebVisitsMonth", color="Segment_Young_Customer",
        barmode="group", title="Average Monthly Web Visits by Demographic Cross-Segments",
        labels={"NumWebVisitsMonth": "Avg Web Visits / Month", "Segment_High_Income": "Income Group"},
        template="plotly_white"
    )
    st.plotly_chart(fig_channel, use_container_width=True)

# Data table preview at the bottom
st.subheader("📋 Filtered Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)
