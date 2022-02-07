import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import Div
from bokeh.palettes import Spectral
from bokeh.io import curdoc
from bokeh.models import Title

lw = 1.5
ds = 25

spend = pd.read_csv('total-government-expenditure-on-education-gdp.csv')

UK_spend = spend.loc[spend['Entity'] == 'United Kingdom']
PL_spend = spend.loc[spend['Entity'] == 'Poland']
FR_spend = spend.loc[spend['Entity'] == 'France']
UKR_spend = spend.loc[spend['Entity'] == 'Ukraine']
SK_spend = spend.loc[spend['Entity'] == 'South Korea']

UK_year = UK_spend['Year'].to_numpy()
PL_year = PL_spend['Year'].to_numpy()
FR_year = FR_spend['Year'].to_numpy()
UKR_year = UKR_spend['Year'].to_numpy()
SK_year = SK_spend['Year'].to_numpy()

UK_gdp = UK_spend['Government expenditure on education, total (% of GDP)'].to_numpy()
PL_gdp = PL_spend['Government expenditure on education, total (% of GDP)'].to_numpy()
FR_gdp = FR_spend['Government expenditure on education, total (% of GDP)'].to_numpy()
UKR_gdp = UKR_spend['Government expenditure on education, total (% of GDP)'].to_numpy()
SK_gdp = SK_spend['Government expenditure on education, total (% of GDP)'].to_numpy()

p = figure(width=700, height=600, toolbar_location="right",)
curdoc().theme = 'contrast'
p.add_layout(Title(text="Całkowite wydatki sektora instytucji rządowych i samorządowych na edukację\n(wszystkie poziomy administracji i wszystkie poziomy edukacji), podane jako udział w PKB.", text_font_style="italic"), 'above')
p.add_layout(Title(text="Całkowite wydatki rządowe na edukację, 1970 do 2019", text_font_size="16pt"), 'above')
p.dot(UK_year, UK_gdp, size=ds, legend_label=f"United Kingdom", line_color="red")
p.dot(PL_year, PL_gdp, size=ds, legend_label=f"Polska", line_color="green")
p.dot(FR_year, FR_gdp, size=ds, legend_label=f"France", line_color="blue")
p.dot(UKR_year, UKR_gdp, size=ds, legend_label=f"Ukraine", line_color="magenta")
p.dot(SK_year, SK_gdp, size=ds, legend_label=f"South Korea", line_color="yellow")
p.line(UK_year, UK_gdp, line_width = lw, line_color="red")
p.line(PL_year, PL_gdp, line_width = lw, line_color="green")
p.line(UKR_year, UKR_gdp, line_width = lw, line_color="magenta")
p.line(FR_year, FR_gdp, line_width = lw, line_color="blue")
p.line(SK_year, SK_gdp, line_width = lw, line_color="yellow")
p.xaxis.axis_label = r" LATA"
p.yaxis.axis_label = f" PKB[%]"
p.legend.label_text_font_size = '15pt'

p.legend.location =(420,2)
show(p)
