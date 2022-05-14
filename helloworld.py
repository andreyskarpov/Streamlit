import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

with st.echo(code_location='below'):
    def graph(x):
        fig=px.histogram(df[df['Branch']==x][['Month','Total']]
                                 .groupby('Month')
                                 .sum()
                                 .reset_index()
                                 , x="Month",y='Total', histfunc='sum', width=300, height=400,
                         labels=dict(Month="Месяц", Total ="Сумма продаж"))\
            .update_xaxes(categoryorder='array', categoryarray=['January','February', 'March'],)
        return fig

    @st.cache
    def get_data():
        data_url = (
            "https://raw.githubusercontent.com/sushantag9/Supermarket-Sales-Data-Analysis/master/supermarket_sales%20-%20Sheet1.csv"
        )
        return (
            pd.read_csv(data_url)
                .dropna(subset=["Date"])
                .assign(
                Date=lambda x: pd.to_datetime(
                    x["Date"]
                )
            )
        )


    sns.set_palette("Paired")
    df=get_data()
    df['Month'] = df['Date'].dt.month_name()
    df['Weekday'] = df['Date'].dt.weekday
    """
    ## Привет! Сегодня мы посмотрим на данные о продажах в трех магазинах
    """

    """
    ### Для начала посмотрим на общую картину продаж
    """

    a=df[['Total', 'Date']].groupby(['Date']).agg({'Total': ['sum', 'mean']})['Total'].reset_index()
    fig1 = px.line(a, x="Date", y=['sum','mean'], title='Cумма продаж по 3-м магазинам',
                   labels=dict(Date="Дата", Total ="Сумма продаж"))

    st.plotly_chart(fig1)
    ### основан на FROM : (https://docs.streamlit.io/library/api-reference/layout/st.columns)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Магазин А")
        st.plotly_chart(graph('A'))

    with col2:
        st.header("Магазин B")
        st.plotly_chart(graph('B'))

    with col3:
        st.header("Магазин C")
        st.plotly_chart(graph('C'))
    ### END FROM
    fig3= px.pie(df[['Branch','Total']].groupby('Branch').sum().reset_index(), values='Total',names='Branch',  title='Соотношение продаж по магазинам', hole=.3 )
    st.plotly_chart(fig3)

    fig2=px.treemap(df[['Branch','Product line', 'Total','Gender']]
                    .groupby(['Branch','Product line','Gender'])
                    .sum()
                    .reset_index(),
                    path=['Branch','Product line','Gender'],
                    values='Total',
                    color='Product line',
                    title='Разбивка по категориям в каждом магазине (Интерактивный)',
                    width = 800, height=600)

    st.plotly_chart(fig2)

    """
    ### Можно посмотреть на различные корреляции
    """
    col1, col2=st.columns(2)
    with col1:
        x1=st.selectbox('Выберите 1 показатель', ['Пол', 'Категория', 'Метод оплаты'])
    dict={'Пол':'Gender', 'Категория':'Product line', 'Метод оплаты':'Payment'}
    with col2:
        x2=st.selectbox('Выберите 2 показатель', ['Пол', 'Категория', 'Метод оплаты'])
    if x1==x2:
        st.write('Выберите разные показатели')
    else:
        data1=pd.pivot_table(df[['Total',dict[x1],dict[x2]]], index=dict[x1], columns=dict[x2], aggfunc=np.sum)
        fig, ax = plt.subplots()
        sns.heatmap(data1, ax=ax )
        st.pyplot(fig)
    """
    ### Теперь посмотрим на разброс значений чеков в зависимости от дня недели
    """
    fig2, ax2 = plt.subplots()
    sns.boxplot(x='Weekday', y='Total', hue='Gender', data=df[['Weekday','Total','Gender']], ax=ax2)
    st.pyplot(fig2)
