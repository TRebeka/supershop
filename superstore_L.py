import streamlit as st
import pandas as pd
import plotly.express as px
import millify as mf
import plotly.graph_objects as go
import altair as alt


#Function to create horizontal barcharts
color_palette = ['#2596be', '#e30d14', '#fbf304', '#e4ecf4', '#062186',"#6f7786", "#658cad","#0d6de1","#facc23", "#c71320","#e93313"]

def create_barchart(data, x_column, y_column, title, xlabel, ylabel):
    fig = px.bar(data, x=x_column, y=y_column, orientation='h', color_discrete_sequence=[color_palette])
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, autosize=False, width=800, )
    
    return fig

#Page config
st.set_page_config(
    page_title="Superstore Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#Load data
df = pd.read_csv('superstore_data.csv')


#Sidebar
with st.sidebar:
    st.title('Superstore Dashboard')

    year_list = ['All'] + list(df['Year'].unique())[::-1]

    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    
    if selected_year != 'All':
        df_selected_year = df[df['Year'] == selected_year]
    else:
        df_selected_year = df


st.title('Superstore Sales Dashboard')

#Summarized data
total_sales = mf.millify(df_selected_year['Sales'].sum(), precision=1)
total_profit = mf.millify(df_selected_year['Profit'].sum(), precision=1)
total_orders = df_selected_year['Order ID'].nunique()


st.header('Summarized Data 📈')
#Row 1
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric("💸 Total Sales", "$" + total_profit)

with col2:
    st.metric('💰 Total profit', "$" + total_profit)

with col3:
    st.metric('📋 Number of orders', total_orders)




#Row 2
col1, col2 = st.columns([2,1])


#Average shipping days
asd = df_selected_year['Days to ship'].mean()

#Plotly indicator
#The displayable range of indicator chart is the minimum and maximum value of Days to ship column.
min_days = df_selected_year['Days to ship'].min()
max_days = df_selected_year['Days to ship'].max()

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=asd,
    title={'text': "Average Shipping Days"},
    domain={'x': [0, 1], 'y': [0, 1]},
    gauge={
        'axis': {'range': [min_days, max_days]},
        'bar': {'color': "#e30d14"},
        'steps': [
            {'range': [min_days, max_days], 'color': "#fff001"},
        ]}))
fig.update_layout(autosize=False, width=400, height=400)

#Display Plotly indicator on dashboard
with col1:
    st.plotly_chart(fig, use_container_width=True)


#Sales trends
sales_trends = df.groupby(['Year', 'Category'])['Sales'].sum().reset_index()

fig = px.bar(sales_trends, x='Year', y='Sales', color='Category', barmode='stack', title='Sales Trends by Product Categories',
             labels={'Sales': 'Total Sales', 'Year': 'Year'},
                          color_discrete_map={'Furniture': '#e30d14', 'Office Supplies': '#fff001', 'Technology': '#0453ab'})

with col2:
    st.plotly_chart(fig, use_container_width=True)

#Top 10 products by sales
top10_sales = df.groupby('Product Name')['Sales'].max().reset_index()
top10_sales = top10_sales.sort_values(by='Sales', ascending=False).head(10)


#Barchart displaying top 10 products by sal
st.plotly_chart(create_barchart(
        data = top10_sales,
        x_column =  "Sales",
        y_column = "Product Name",
        title = "Top 10 Products by Sales",
        xlabel= "Total Sales",
        ylabel= "Product Name"))


#Top 10 products by profit
top10_profit = df_selected_year.groupby('Product Name')['Profit'].max().reset_index()
top10_profit = top10_profit.sort_values(by='Profit', ascending=False).head(10)

#Barchart displaying top 10 products by profit
st.plotly_chart(create_barchart(
        data = top10_profit,
        x_column =  "Profit",
        y_column = "Product Name",
        title = "Top 10 Products by Profit",
        xlabel= "Total Profit",
        ylabel= "Product Name"))
  