import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Netflix Userbase Dashboard", layout="wide")

# Title
st.title("📊 Netflix Userbase Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/supreetkesti/Downloads/my_downloads/Exploratory-Analysis-of-Netflix-Userbase-main/netflix_userbase.csv")

    # Rename columns
    df.rename(columns={
        'User ID': 'user_id',
        'Subscription Type': 'subscription_type',
    
        'Monthly Revenue': 'monthly_revenue',
        'Join Date': 'join_date',
        'Last Payment Date': 'last_payment_date',
        'Country': 'country',
        'Age': 'age',
        'Gender': 'gender',
        'Device': 'device',
        'Plan Duration': 'plan_duration'
    }, inplace=True)

    # Convert dates
    df['join_date'] = pd.to_datetime(df['join_date'])
    df['last_payment_date'] = pd.to_datetime(df['last_payment_date'])

    return df


df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

country = st.sidebar.multiselect("Select Country", df['country'].unique(), default=df['country'].unique())
subscription = st.sidebar.multiselect("Subscription Type", df['subscription_type'].unique(), default=df['subscription_type'].unique())

filtered_df = df[(df['country'].isin(country)) & (df['subscription_type'].isin(subscription))]

# Overview
st.subheader("Dataset Overview")
st.write(filtered_df.head())

col1, col2, col3 = st.columns(3)

col1.metric("Total Users", len(filtered_df))
col2.metric("Avg Revenue", round(filtered_df['monthly_revenue'].mean(), 2))
col3.metric("Avg Age", round(filtered_df['age'].mean(), 1))

# Revenue Distribution
st.subheader("Monthly Revenue Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['monthly_revenue'], kde=True, ax=ax1)
st.pyplot(fig1)

# Subscription Type Count
st.subheader("Subscription Type Distribution")
fig2, ax2 = plt.subplots()
sns.countplot(data=filtered_df, x='subscription_type', ax=ax2)
st.pyplot(fig2)

# Country-wise users
st.subheader("Users by Country")
country_counts = filtered_df['country'].value_counts()
fig3, ax3 = plt.subplots()
country_counts.plot(kind='bar', ax=ax3)
st.pyplot(fig3)

# Device usage
st.subheader("Device Usage")
fig4, ax4 = plt.subplots()
sns.countplot(data=filtered_df, x='device', ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

# Gender distribution
st.subheader("Gender Distribution")
fig5, ax5 = plt.subplots()
sns.countplot(data=filtered_df, x='gender', ax=ax5)
st.pyplot(fig5)

# Age distribution
st.subheader("Age Distribution")
fig6, ax6 = plt.subplots()
sns.histplot(filtered_df['age'], kde=True, ax=ax6)
st.pyplot(fig6)

# Time trends
st.subheader("User Join Trend Over Time")
join_trend = filtered_df.groupby(filtered_df['join_date'].dt.to_period("M")).size()
join_trend.index = join_trend.index.astype(str)
fig7, ax7 = plt.subplots()
join_trend.plot(ax=ax7)
plt.xticks(rotation=45)
st.pyplot(fig7)

st.markdown("---")
st.write("Built with Streamlit 🚀")



