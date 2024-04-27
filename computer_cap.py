import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

custom_css = """
<style>
body {
    background-color: #D3D3D3;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title('Decoding Laptop Specs: Price Dynamics and Frequency Trends')

copy_df = pd.read_csv('copy_df.csv')
screen_copy_df = pd.read_csv('screen_copy_df')

# lines 22-46 created groups by their gpus, found each groups average price, and created a bar graph 
def calculate_average_price(copy_df):
    gpu_groups = {
        'Intel': copy_df[copy_df['Gpu'].str.startswith('Intel')],
        'AMD': copy_df[copy_df['Gpu'].str.startswith('AMD')],
        'Nvidia': copy_df[copy_df['Gpu'].str.startswith('Nvidia')]
    }
    average_prices = {}
    for manufacturer, group_df in gpu_groups.items(): 
        average_price = group_df['Price in Dollars'].mean()
        average_prices[manufacturer] = average_price

    return average_prices
average_prices = calculate_average_price(copy_df)
average_prices_df = pd.DataFrame.from_dict(average_prices, orient='index', columns=['Average Price'])
average_prices_df.reset_index(inplace=True)
average_prices_df.rename(columns={'index': 'Manufacturer'}, inplace=True)
bar_chart = alt.Chart(average_prices_df).mark_bar().encode(
    x='Manufacturer',
     y=alt.Y('Average Price', axis=alt.Axis(format='$.2f')),
    color='Manufacturer'
).properties(
    title='Average Prices of GPUs by Manufacturer',
    width=200,
    height=400
)

# lines 50-58 creates a graph showing the average price of a laptop based on company, and formats the price
# my hypothesis was that Apple was going to be the highest but it was Razer
average_prices_by_company = copy_df.groupby('Company')['Price in Dollars'].mean().reset_index()
average_prices_by_company.columns = ['Company', 'Average Price']
company_chart = alt.Chart(average_prices_by_company).mark_bar().encode(
    x='Company',
    y=alt.Y('Average Price', axis=alt.Axis(format='$.2f')),
).properties(
    title='Average Prices of Laptops by Company',
    width=alt.Step(80)
)

# lines 61-74 creates a scatter plot chart showing the price of a laptop with certain ram
dot_color = '#FF0000'
scatter_plot = alt.Chart(copy_df).mark_circle().encode(
    x='Ram:Q',
    y=alt.Y('Price in Dollars:Q', axis=alt.Axis(format='$,d')),
    color=alt.value(dot_color),
    tooltip=['Ram:Q', alt.Tooltip('Price in Dollars:Q', format='$,.0f')]
).properties(
    width=400,
    height=600,
    title='RAM vs Price Scatter Plot'
)
scatter_plot.configure_title(
    fontSize=16
)

# lines 77-94 creates a histogram of how many laptops have certain screen sizes
screen_size_counts = screen_copy_df['Inches'].value_counts().reset_index()
screen_size_counts.columns = ['Screen Size (Inches)', 'Frequency']
chart = alt.Chart(screen_size_counts).mark_bar().encode(
    x=alt.X('Screen Size (Inches):O', title='Screen Size (Inches)'),
    y=alt.Y('Frequency:Q', title='Frequency'),
    tooltip=['Screen Size (Inches)', 'Frequency'],
    color=alt.condition(
        alt.datum['Screen Size (Inches)'] == 15.6,
        alt.value('#f02929'),
        alt.value('#96daff') 
    )
).properties(
    width=500,
    height=300
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

# lines 97-109 formats streamlit into 2 columns
col1, col2 = st.columns((2, 2))
with col1:
    st.altair_chart(bar_chart, use_container_width=True)
    st.write("When we organize GPUs by brand, it's clear that 'Nvidia' laptops tend to have the highest average price")
    st.altair_chart(company_chart, use_container_width=True)
    st.write("I initially guessed 'Apple' would be the priciest brand, but this chart makes it clear that 'Razer' laptops actually claim the top spot for expense."
)
   
with col2:
    st.altair_chart(scatter_plot)
    st.write("Each laptop is represented by a dot on the chart, indicating its RAM and price. It's evident that as the RAM increases, so does the price of the laptop.")
    st.altair_chart(chart, use_container_width=True)
    st.write("This chart illustrates different screen sizes, with 15.6-inch screens being the most common.")
