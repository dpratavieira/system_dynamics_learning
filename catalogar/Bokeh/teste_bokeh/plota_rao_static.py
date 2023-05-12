#%%
import numpy as np
import pandas as pd
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Range1d, Slider, TextInput, Button, Paragraph
from bokeh.plotting import ColumnDataSource, figure, show, curdoc

dofs_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
arq4 = pd.read_csv('force.4', header=None, delim_whitespace=True)
arq4.columns=['Period','Incidence','DOF','MOD','PHA','REAL','IMAG']

per = np.unique(arq4['Period'])
inc = np.unique(arq4['Incidence'])
pos = arq4['DOF']==4
rao_roll = arq4['MOD'][pos].to_numpy().reshape((-1,len(inc)))

#%%
rao = []
for ii in range(6):
    pos = arq4['DOF']==ii+1
    rao_aux = arq4['MOD'][pos].to_numpy().reshape((-1,len(inc)))
    rao.append(rao_aux.transpose().tolist())

#%%

# def update(attr, old, new):
#     texto.text = dofs_names[sld.value - 1]
#     dof = sld.value
#     pos = arq4['DOF']==dof
#     matriz = arq4['MOD'][pos].to_numpy().reshape((-1,len(inc)))
#     rao = interp2d(per,inc,np.fliplr(matriz.transpose()))
#     inc_q=np.float(inc_q_txt.value) % 360
#     new_data = dict(ds.data)
#     new_data['x'] = per
#     new_data['y'] = rao(per,inc_q)
#     ds.data = new_data


xs = np.repeat(per.reshape(-1,1).transpose(),25,axis=0).tolist()
ys = rao_roll.transpose().tolist()

dados = dict(xs1=xs, ys1=ys)

data=dict(x=xs[1], y=ys[1])
source = ColumnDataSource(data)

plot = figure(x_range=(0, 20), width=800, height=400)
plot.line('x','y', source=source)

sld1 = Slider(start=1, end = 6, value=1, step=1, title='Grau de Liberdade')
sld2 = Slider(start=0, end = 360, value=90, step=15, title='Incidencia')
texto = Paragraph()
inc_q_txt = TextInput(value='180')

update = CustomJS(args=dict(source=source, sld1=sld1, sld2=sld2, inc1 = list(inc), per1 = list(per), rao1 = rao),
                    code="""
    const data = source.data;
    const DOF = sld1.value - 1 ;
    const SLD2 = sld2.value;
    const INC = inc1
    var pos = 0
    const x = data['x']
    const y = data['y']
    console.log(x)
    for (let i = 0; i < inc1.length;++i){
        if (SLD2 === INC[i]){
            console.log("Passou aqui")
            pos = i
            console.log("Pos = " + pos)
            for (let j = 0; j < x.length;++j){
                y[j] = rao1[DOF][pos][j]
            }
        }
    }
    source.change.emit();
""")

sld1.js_on_change('value',update)
sld2.js_on_change('value',update)
# inc_q_txt.js_on_change('value',update)


layout = row(plot,column(sld1, sld2))

show(layout)


