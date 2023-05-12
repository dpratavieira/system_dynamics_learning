#%%
import pandas as pd

cond_amb = pd.read_csv('ca_TOBD_berco_1.csv')

cond_amb.to_parquet('ca_TOBD_berco_1.parquet')