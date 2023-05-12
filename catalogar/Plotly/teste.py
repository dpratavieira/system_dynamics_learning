# import chart_studio.plotly as py
import numpy as np
import plotly.io as pio

data = [dict(
        visible = False,
        line=dict(color='#00CED1', width=6),
        name = '𝜈 = '+str(step),
        x = np.arange(0,10,0.01),
        y = np.sin(step*np.arange(0,10,0.01))) for step in np.arange(0,5,0.1)]
data[10]['visible'] = True

steps = []
for i in range(len(data)):
    step = dict(
        method = 'restyle',
        args = ['visible', [False] * len(data)],
    )
    step['args'][1][i] = True # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active = 10,
    currentvalue = {"prefix": "Frequency: "},
    pad = {"t": 50},
    steps = steps
)]

layout = dict(sliders=sliders)
fig = dict(data=data, layout=layout)
pio.write_html(fig, 'teste_pio.html', auto_open=True)

# py.iplot(fig, filename='Sine Wave Slider')

# import chart_studio.plotly as py
# import plotly.figure_factory as ff
# import pandas as pd

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/school_earnings.csv")

# table = ff.create_table(df)
# py.iplot(table, filename='jupyter-table1')

# import plotly.express as px
# fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
# fig.write_html('first_figure.html', auto_open=True)