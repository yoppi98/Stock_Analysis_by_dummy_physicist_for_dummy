import plotly.graph_objects as go
import plotly.io as pio

x=[1,2,3,4,5]
y=[10,20,30,40,50]

data = go.Bar(x=x,y=x)
fig = go.Figure(data)
fig.show()