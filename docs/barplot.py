import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

# Create figures in Express
df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
figure1 = px.bar(df, y='pop', x='country', text_auto='.2s',
            title="Default: various text sizes, positions and angles")

figure2 = px.bar(df, y='pop', x='country', text_auto='.2s',
            title="Default: various text sizes, positions and angles")

# For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
# This is essentially breaking down the Express fig into it's traces
figure1_traces = []
figure2_traces = []
for trace in range(len(figure1["data"])):
    figure1_traces.append(figure1["data"][trace])
for trace in range(len(figure2["data"])):
    figure2_traces.append(figure2["data"][trace])

#Create a 1x2 subplot
this_figure = sp.make_subplots(rows=1, cols=2) 

# Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
for traces in figure1_traces:
    this_figure.append_trace(traces, row=1, col=1)
for traces in figure2_traces:
    this_figure.append_trace(traces, row=1, col=2)

#the subplot as shown in the above image
final_graph = dcc.Graph(figure=this_figure)



