#%%
import numpy as np
import random
import matplotlib.pyplot as plt

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, TextInput, Button, Paragraph
from bokeh.plotting import ColumnDataSource, figure, show, curdoc

# create some widgets
button = Button(label="Say HI")
input = TextInput(value="Bokeh")
output = Paragraph()
sld = Slider(start=1, end = 5, value=2, step=1, title='expoente')

# add a callback to a widget
def update():
    output.text = "Hello, " + input.value

def update2(attrname, old, new):
    ds.data['y']=x**sld.value

button.on_click(update)
sld.on_change('value',update2)


x = np.array([random.random() for _ in range(100)])
y = x**2
y1= np.sin(x)

dados = ColumnDataSource(data=dict(x=x,y=y))

grafico = figure(width=800, height=400)

r = grafico.scatter('x','y',source=dados)
ds = r.data_source

layout = row(grafico, column(input, button, output, sld))

curdoc().add_root(layout)