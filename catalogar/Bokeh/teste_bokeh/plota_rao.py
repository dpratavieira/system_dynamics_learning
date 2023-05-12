#%%
import numpy as np
import pandas as pd
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
from bokeh.layouts import column, row
from bokeh.models import Range1d, Slider, TextInput, Button, Paragraph
from bokeh.plotting import ColumnDataSource, figure, show, curdoc

dofs_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
arq4 = pd.read_csv('force.4', header=None, delim_whitespace=True)
arq4.columns=['Period','Incidence','DOF','MOD','PHA','REAL','IMAG']

per = np.unique(arq4['Period'])
inc = np.unique(arq4['Incidence'])

def update():
    texto.text = dofs_names[sld.value - 1]
    dof = sld.value
    pos = arq4['DOF']==dof
    matriz = arq4['MOD'][pos].to_numpy().reshape((-1,len(inc)))
    rao = interp2d(per,inc,np.fliplr(matriz.transpose()))
    inc_q=np.float(inc_q_txt.value) % 360
    new_data = dict(ds.data)
    new_data['x'] = per
    new_data['y'] = rao(per,inc_q)
    ds.data = new_data

sld = Slider(start=1, end = 6, value=1, step=1, title='Grau de Liberdade')
texto = Paragraph()
inc_q_txt = TextInput(value='180')

sld.on_change('value',update)
inc_q_txt.on_change('value',update)


dados = ColumnDataSource(data=dict(x=[],y=[]))

grafico = figure(width=800, height=400)

r = grafico.line('x','y',source=dados)
ds = r.data_source

grafico.x_range = Range1d(0,20)

layout = row(grafico,column(texto, sld, inc_q_txt))

curdoc().add_root(layout)

# plt.plot(per,rao(per,inc_q),'r:')
# plt.plot(per,matriz[:,1:3])

# plt.xlim(0,30)
# plt.show()