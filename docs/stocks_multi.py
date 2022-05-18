import plotly.express as px

df = px.data.stocks(indexed=True)-1
print(df)
print(df.dtypes)
fig = px.area(df, facet_col="company", facet_col_wrap=2)
fig.show()