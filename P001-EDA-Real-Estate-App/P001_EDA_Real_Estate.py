import streamlit as st
import pandas as pd
import folium
import geopandas
import seaborn as sns

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from matplotlib import pyplot as plt

import plotly.express as px
from PIL import Image


pd.set_option('display.float_format', lambda x: '%.f' % x)

# =================================================
# ================== PAGE SET UP ==================
# =================================================
# === page titles

st.set_page_config(layout="wide")

c1, c2 = st.beta_columns((1,3))
# image
with c1:
    photo = Image.open('house.png')
    st.image(photo,width=300)

#headers
with c2:

    st.write('')
    HR_format = '<p style="font-family:sans-serif;' \
                   'font-size: 55px;' \
                   'font-weight: bold;' \
                   'font-style: italic;' \
                   'text-align: center;' \
                   '">House Rocket Company Analysis </p>'

    st.markdown(HR_format, unsafe_allow_html=True)

st.write('')
st.write("House Rocket's business model consists of purchasing and reselling properties through a digital platform. "
         "The data scientist is responsible for developing an online dashboard to help the CEO company "
         "to have an overview of properties available on House Rocket's portfolio and "
         "find the best business opportunities.")

st.write("For more information verify on: "
                         "[GitHub](https://github.com/almirgouvea/P001-Exploratory-Data_Analysis)")

st.write("Made by **Almir Donizette Vicente Gouvea**"
                 " \n\n"
                 "Social media: [LinkedIn](https://www.linkedin.com/in/almirdonizette) "
                 "  [Mail](almir.donizette@gmail.com)")

# =================================================
# =============== HELPER FUNCTIONS ================
# =================================================


@st.cache(allow_output_mutation = True)

def get_data(path):
    data = pd.read_csv(path)
    return data

@st.cache (allow_output_mutation=True)

def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile

def remove_duplicates(data):
    # Removendo os ID que estão duplicados, considerando somente os valores mais recente
    data = data.sort_values('date', ascending=False).drop_duplicates(subset='id', keep='first')
    return data

# removendo o imóveis que possui 33 quartos por ser um outlier
def remove_value(data):
    data = data.drop(15870)
    return data

def overview_data(data):
    st.title("Data Overview")
    exp_data = st.beta_expander("Click here to expand and see the dataset general information", expanded=False)
    with exp_data:
        st.subheader("Data Dimensions")
        st.write("Number of Unique Registers: **21436**")
        st.write("Initial Number of Attributes: **21**")
        st.write("Number of attributes created: **8**")
        st.write("Attributes created: **House_ID, Region, Purchase_price, Best_season_to_sold, Price_season, "
                 "Median_Price, Condition and Status**")
        st.write("Number of suggested houses to sold considering price median: **10579**")
        st.write("Number of suggested houses to sold considering the seasons: **11877**")
        st.write("Date interval of dataset: from **02 May 2014** to **27 May 2015**")

    if st.checkbox('Show dataset'):
        st.write(data)

    return None

def portifolio_density(data,geofile):

    st.title("Region Overview")
    portifolio_density = st.beta_expander("Click here to expand and see the dataset portfolio density", expanded = False)
    with portifolio_density:
        st.subheader("Portfolio Density")
        c1, c2 = st.beta_columns((2, 2))

        df = data

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        # Base Map - Folium
        density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

        marker_cluster = MarkerCluster().add_to(density_map)

        for name, row in df.iterrows():
            folium.Marker([row['lat'], row['long']],
                          popup='Sold R${0} on: {1}. Features: {2} m2,'
                                '{3} bedrooms, {4} bathrooms,'
                                'year built: {5}'.format(row['price'],
                                                     row['date'],
                                                     row['sqft_living'],
                                                     row['bedrooms'],
                                                     row['bathrooms'],
                                                     row['yr_built'])).add_to(marker_cluster)

        with c1:
            st.header('Portfolio Density')
            folium_static(density_map, width=600)

       # Region Price Map
        df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

        df.columns = ['ZIP', 'PRICE']

        geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

        region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                      default_zoom_start=15)

        region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',  # faz um join com os dados
                                fill_color='YlOrRd',  # degrade de cor amarelo, laranja e vermelho
                                fill_opacity=0.7,  # opacidade no preenchimento
                                line_opacity=0.2,  # opacidade na linha
                                legend_name='AVG PRICE')

        with c2:
            st.header("Price Density")
            folium_static(region_price_map, width=600)

    return None


def price_median(data):
    # Agrupar os dados por zipcode e obter a média do preço
    df = data[['price', 'zipcode']].groupby('zipcode').median().reset_index()

    # mudar o nome das colunas
    df.columns = ["zipcode", "price_median"]

    # juntar a mediana de preços por região com o dataset original de acordo com o zipcode
    df2 = pd.merge(data, df, on='zipcode', how='inner')

    # comparando os preços com a mediana de preços para verificar se estão abaixo ou acima da média
    for index, row in df2.iterrows():
        if row['price'] < row['price_median']:
            df2.loc[index, 'price_analyse'] = "below_mean"
        else:
            df2.loc[index, 'price_analyse'] = "above_mean"

    # Verificar quais imóveis que estão com preço abaixo da média e em boas condições para poder sugerir para compra
    for index, row in df2.iterrows():
        if (row['price_analyse'] == 'below_mean') & (row['condition'] >= 3):
            df2.loc[index, 'status'] = "Recommendable"
        else:
            df2.loc[index, 'status'] = "Not Recommendable"

    return df2

def purchase_sugestion(data):

    df2 = price_median(data)

    df3 = df2[['id', 'zipcode', 'price', 'price_median', 'condition', 'status']]

    df3.columns = ['House_ID', 'Region', 'Purchase_price', 'Median_price', "Condition", "Status"]

    purchase_sugestion = df3.loc[df3['Status'] == 'Recommendable', 'Purchase_price'].sum()

    amount_purchase_sugestion = df3.loc[df3['Status'] == 'Recommendable', 'House_ID'].count()

    sold_sugestion = purchase_sugestion*1.3

    first_profit = sold_sugestion - purchase_sugestion

    st.title("Properties Purchases")
    my_expander = st.beta_expander("Click here to expand and see purchase suggestions", expanded=False)
    with my_expander:
        st.info("Here you can choose the columns to analyze the purchase houses suggestions")

        f_attributes = st.multiselect(
            'Choose columns to analyse houses bought',
             df3.columns.sort_values(ascending=True).unique())

        if f_attributes != []:
            df3 = df3[f_attributes]
        else:
            df3 = df3.copy()

        st.dataframe(df3)

        st.write('**The number of recommend houses to buy considering median price is',
                 '{}**'.format(amount_purchase_sugestion))

        st.write('**The value invested on the purchase of recommended houses is',
                 'US$ {:,.2f}**'.format(purchase_sugestion))

        st.write('**The expected profit considering median price is',
                 'US$ {:,.2f}**'.format(first_profit))

    return None

def sazonality(data):

    df2 = price_median(data)

    df2['date'] = pd.to_datetime(df2['date']).dt.strftime('%Y-%m-%d')

    for index, row in df2.iterrows():
        if (row['date'] < '2014-06-01') | ((row['date'] > '2015-03-01') & (row['date'] < '2015-06-01')):
            df2.loc[index, 'season'] = "Spring"
        elif (row['date'] >= '2014-06-01') & (row['date'] < '2014-09-01'):
            df2.loc[index, 'season'] = "Summer"
        elif (row['date'] >= '2014-09-01') & (row['date'] < '2014-11-01'):
            df2.loc[index, 'season'] = "Autumn"
        else:
            df2.loc[index, 'season'] = "Winter"

    df3 = df2[['zipcode', 'season', 'price']].groupby(['zipcode', 'season']).median().reset_index()

    df3.columns = ['zipcode', 'season', 'price_median_per_season']

    # obter o maior preço por zipcode e sazonalidade para saber em qual estação é mais vantajoso vender
    df4 = df3[df3.groupby(['zipcode'])['price_median_per_season'].transform(max) == df3['price_median_per_season']]

    df5 = df4.groupby(['zipcode','price_median_per_season'])['season'].apply(', '.join).reset_index()

    df6 = df2[['id', 'price', 'zipcode']]

    df7 = pd.merge(df6, df5, on='zipcode', how='inner')

    for index, row in df7.iterrows():
        if row['price'] < row['price_median_per_season']:
            df7.loc[index, 'status_season'] = "Recommendable"
        else:
            df7.loc[index, 'status_season'] = "Not Recommendable"

    best_season = df7[['id', 'zipcode', 'price', 'season', 'price_median_per_season','status_season']]

    best_season.columns = ['House_ID', 'Region', 'Purchase_price', 'Best_season_to_sold', "Price_season","Status"]

    st.title("Property Sold Per Season")
    my_expander = st.beta_expander("Click here to expand and see sold suggestions", expanded = False)

    with my_expander:
        st.info("Here you can choose the columns to analyze the sold houses suggestions")

        f_sold_houses = st.multiselect(
            'Choose columns to analyse houses sold',
            best_season.columns)

        if f_sold_houses != []:
            best_season = best_season[f_sold_houses]
        else:
            best_season = best_season.copy()

        st.dataframe(best_season)

    st.title("Probable Value Acquired Per Season")

    df8 = df7.drop(columns=['season', 'price_median_per_season'])

    df9 = pd.merge(df8, df4, on='zipcode', how='inner')

    df10 = df9.drop_duplicates(subset='id', keep='first')

    for index, row in df10.iterrows():
        if (row['price'] < row['price_median_per_season']):
            df10.loc[index, 'price_sold'] = (row['price'] * 1.3)
        else:
            df10.loc[index, 'price_sold'] = (row['price'] * 1.1)

    amount_season_suggestion = df10.loc[df10['status_season'] == 'Recommendable', 'id'].count()

    total_sold = df10.loc[df10['status_season'] == 'Recommendable']['price_sold'].sum()

    total_invested = df10.loc[df10['status_season'] == 'Recommendable']['price'].sum()

    profit = total_sold - total_invested

    my_expander = st.beta_expander("Click here to expand and see the houses per season", expanded = False)
    with my_expander:
        st.info("Here you can verify how much money can earn selling houses in the right season")

        fig = plt.figure(figsize=(10, 6))

        by_season = df10.loc[df10['status_season']=='Recommendable',
                             ['season', 'price_sold']].groupby('season').sum().reset_index()

        ax = sns.barplot(x=by_season['season'], y=by_season['price_sold'], data=by_season)
        plt.title("Profit amount per season")

        sns.set(font_scale=1.4)

        fig = px.bar(by_season, x='season', y='price_sold', color='season',
                     labels={'season': 'Season', 'price_sold': 'Profit earned per season (Billions)'},
                     template='simple_white')

        st.plotly_chart(fig, use_container_width=True)



        st.write("Considering the seasons' analysis criteria:")

        st.write("")

        st.write('**The number of recommend houses to buy is',
                 '{}**'.format(amount_season_suggestion))

        st.write('**The value invested on the purchase is',
                 'US$ {:,.2f}**'.format(total_invested))

        st.write('**The value gained in the purchase process is',
                 'US$ {:,.2f}**'.format(total_sold))

        st.write('**The expected profit for available properties is',
                 'US$ {:,.2f}**'.format(profit))

    return None

# =================================================
# ================== MAIN FILE +==================
# =================================================
if __name__ =="__main__":
    # ETL

    # data extraction
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    data = get_data(path)
    geofile = get_geofile(url)

    # transformation
    remove_duplicates(data)
    remove_value(data)
    overview_data(data)
    portifolio_density(data, geofile)
    price_median(data)
    purchase_sugestion(data)
    sazonality(data)