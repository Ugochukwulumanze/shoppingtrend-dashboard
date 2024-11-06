import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration 
st.set_page_config( page_title="SHOPPING TREND ANALYSIS",
                   page_icon= ":bar_chart:",
                   layout='wide'
                   )



# Optimized data caching and error handling
@st.cache_data
def get_data():
    try:
        df = pd.read_csv("shopping_trends.csv")
    except FileNotFoundError:
        st.error("File not found. Please upload the correct file.")
        return pd.DataFrame
    return df

df = get_data()

# ---- SIDEBAR ----
st.sidebar.header('Please filter here')
category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)
gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)
location = st.sidebar.multiselect(
    "Select Location",
    options=df['Location'].unique(),
    default=df['Location'].unique()
)
# Filter dataframe based on sidebar inputs
df_selection = df.query(
    "Category == @category & Location == @location & Gender == @gender"
)

# Title and KPIs
st.title(":bar_chart: DATA ANALYSIS EXECUTIVE REPORT ON THE SHOPPING TREND DATA")
st.markdown('##')

# Top KPIs
total_revenue = df_selection['Purchase Amount (USD)'].sum()
number_of_customers=df_selection['Customer ID'].count()

left_column,right_column =st.columns(2)

with left_column:
    st.subheader("Total Revenue")
    st.subheader(f"US $ {total_revenue:,}")
with right_column:
    st.subheader("Number Of Customer")
    st.subheader(f'{number_of_customers:,}')

count_payment_methods=df_selection['Payment Method'].value_counts(ascending=False)
shipping_type=df_selection.groupby(['Shipping Type'])['Purchase Amount (USD)'].sum()
season=df_selection.groupby(['Season'])['Purchase Amount (USD)'].sum()
promo=df_selection['Promo Code Used'].value_counts()

def create_bar_chart(data, x, y, title,labels):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=['#0083B8'] * len(data),
        template="plotly_white",
        labels=labels
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )
    return fig
payment_chart=create_bar_chart(data=count_payment_methods,x=count_payment_methods.index,y=count_payment_methods,title="Distribution of payment method",labels={'y':'Count of Payment Methods'})
shipping_chart=create_bar_chart(data=shipping_type,y=shipping_type.index,x=shipping_type,title="Revenue By Shipping Type",labels={'x':'Amount Made'})
season_chart=px.area(season,x=season.index,y=season,title="<b>Revenue By Season</b>",labels={"y":"Revenue"})
promo_chart =px.pie(promo,names=promo.index,values=promo,title="Distribution Of Promo Code User")
column_left,column_right=st.columns(2)
with column_left:
    st.plotly_chart(payment_chart,use_container_width=True)
    st.plotly_chart(season_chart,use_container_width=True)
with column_right:
    st.plotly_chart(promo_chart,use_container_width=True)
    st.plotly_chart(shipping_chart,use_container_width=True)
    

