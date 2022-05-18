import plotly.express as px
df = px.data.gapminder()
print(df)
print(df.dtypes)
fig = px.scatter(df, x='gdpPercap', y='lifeExp', color='continent', size='pop',
                facet_col='year', facet_col_wrap=4)
fig.show()