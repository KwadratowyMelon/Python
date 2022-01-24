mport glob
from PIL import Image
import scipy.interpolate
import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import Div
from bokeh.palettes import Spectral


j = 0
lamb = 532 * pow(10,-9)
d = 50 * pow(10, -6)
m = 85
x = []
Xarray = np.arange(1,1281)
YaxisGora = []
YaxisDol = []
imagesPath = glob.glob(".\\E7_step_100s\\*.jpg")
t_start = 20.6
t_end = 44
nazwa_cieklego_krysztalu = "E7"
step = 100


def getColorValues(image, c):  # r = 0, g = 1, b = 2
    array = []
    pix = image.load()
    for i in range(image.size[0]):
        kolor = pix[i, c] #tu moze byc c
        array.append(kolor)
    return array


def correct_values(data):
    result = []
    result.append(0)
    for i in range(1, len(data)):
        val = data[i-1] - data[i]
        if abs(val) > 50:
            val = 0
        result.append(result[i-1] + val)
    return result

def usrednione_5(data):
    usrednione = []
    i = 0
    while i < len(data) - 4:
        var = (data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4])/5
        usrednione.append(var)
        i += 5

    return usrednione

def usrednione_3(data):
    usrednione = []
    i = 0
    while i < len(data) - 2:
        var = (data[i]+data[i+1]+data[i+2])/3
        usrednione.append(var)
        i += 3
    return usrednione


with open("Zaxis.txt", "w+") as file:
        for i in range(len(imagesPath)):
            z = t_start + i*(t_end-t_start)/(len(imagesPath))
            x.append(z)
            file.write(f"{z} \t")
        file.close()



with open("Xaxis.txt", "w+") as file:
    for i in range(len(Xarray)):
        file.write(f"{i} \t")
file.close()


for path in imagesPath:
    Ygora = []
    Ydol = []
    image = Image.open(path)
    gora = int(image.size[1] / 4)
    dol = int(3 * image.size[1] / 4)
    resultGora = image.crop((0, gora, image.size[0], gora + 1))
    resultDol = image.crop((0, dol, image.size[0], dol + 1))

    colorValuesGora = getColorValues(resultGora, 0)
    colorValuesDol = getColorValues(resultDol, 0)
    
    
    with open("GoraYmatrix.txt", "a+") as file:
        for i in range(image.size[0]):
            Ygora.append(colorValuesGora[i][1])
            converted_num = str(colorValuesGora[i][1])
            file.write(f"{converted_num} \t")
        file.write("\n")
        file.close()


    with open("DolYmatrix.txt", "a+") as file:
        for i in range(image.size[0]):
            Ydol.append(colorValuesDol[i][1])
            converted_num = str(colorValuesDol[i][1])
            file.write(f"{converted_num} \t")
        file.write("\n")
        file.close()


    cubic_spline_interpolation_gora = scipy.interpolate.CubicSpline(Xarray, Ygora)
    cubic_spline_interpolation_dol = scipy.interpolate.CubicSpline(Xarray, Ydol)
    
    root_gora = cubic_spline_interpolation_gora.solve(cubic_spline_interpolation_gora.c.max())[1]
    root_dol = cubic_spline_interpolation_dol.solve(cubic_spline_interpolation_dol.c.max())[1]

    
    with open("polozenie_max_gora.txt", "a+") as file:
        YaxisGora.append(root_gora)
        converted_num = str(root_gora)
        file.write(f"{converted_num} \n")
    file.close()


    with open("polozenie_max_dol.txt", "a+") as file:
        YaxisDol.append(root_dol)
        converted_num = str(root_dol)
        file.write(f"{converted_num} \n")
    file.close()


final_pixel_pos_gora = correct_values(YaxisGora)
final_pixel_pos_dol = correct_values(YaxisDol)

avg_5_dol = usrednione_5(final_pixel_pos_dol)
avg_5_gora = usrednione_5(final_pixel_pos_gora)

avg_3_dol = usrednione_3(final_pixel_pos_dol)
avg_3_gora = usrednione_3(final_pixel_pos_gora)


x_usr3 = []
x_usr5 = []
y_dol = []
y_gora = []
y_dol.append(0)
y_gora.append(0)
y_dol_usr3 = []
y_gora_usr3 = []
y_dol_usr3.append(0)
y_gora_usr3.append(0)
y_dol_usr5 = []
y_gora_usr5 = []
y_dol_usr5.append(0)
y_gora_usr5.append(0)

for i in range(1, len(final_pixel_pos_dol)):

    y_dol_temp = (final_pixel_pos_dol[i] * lamb)/(d * 45)
    y_gora_temp = (final_pixel_pos_gora[i] * lamb)/(d * m)
    y_dol.append(y_dol_temp)
    y_gora.append(y_gora_temp)
    


for i in range(1, len(avg_3_dol)):
    y_dol_avg_3 = (avg_3_dol[i] * lamb)/(d * 45)
    y_gora_avg_3 = (avg_3_gora[i] * lamb)/(d * m)
    y_dol_usr3.append(y_dol_avg_3)
    y_gora_usr3.append(y_gora_avg_3)
    


for i in range(1, len(avg_5_dol)):
    y_dol_avg_5 = (avg_5_dol[i] * lamb)/(d * 45)
    y_gora_avg_5 = (avg_5_gora[i] * lamb)/(d * m)
    y_dol_usr5.append(y_dol_avg_5)
    y_gora_usr5.append(y_gora_avg_5)

   
for i in range(len(y_dol_usr3)):
    t = t_start + i*(t_end-t_start)/(len(y_dol_usr3))
    x_usr3.append(t)


for i in range(len(y_dol_usr5)):
    t = t_start + i*(t_end-t_start)/(len(y_dol_usr5))
    x_usr5.append(t)



p = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s)")

p.dot(x, y_gora, size=15,legend_label=f"n_o", line_color="orange")
p.dot(x, y_dol, size=15,legend_label=f"n_e", line_color="green")
p.xaxis.axis_label = r"$$\color{black} T[°C]$$"
p.yaxis.axis_label = r"$$\color{black} Δn$$"
p.legend.label_text_font_size = '15pt'
p.legend.location =(520,350)

pusr3 = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s, usr-3)")

pusr3.dot(x_usr3, y_gora_usr3, size=15,legend_label=f"n_o", line_color="orange")
pusr3.dot(x_usr3, y_dol_usr3, size=15,legend_label=f"n_e", line_color="green")
pusr3.xaxis.axis_label = r"$$\color{black} T[°C]$$"
pusr3.yaxis.axis_label = r"$$\color{black} Δn$$"
pusr3.legend.label_text_font_size = '15pt'
pusr3.legend.location =(520, 350)

pusr5 = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s, usr-5)")

pusr5.dot(x_usr5, y_gora_usr5, size=15,legend_label=f"n_o", line_color="orange")
pusr5.dot(x_usr5, y_dol_usr5, size=15,legend_label=f"n_e", line_color="green")
pusr5.xaxis.axis_label = r"$$\color{black} T[°C]$$"
pusr5.yaxis.axis_label = r"$$\color{black} Δn$$"
pusr5.legend.label_text_font_size = '15pt'
pusr5.legend.location =(520, 350)

pall = figure( width=700, height=500, toolbar_location="right",
    title=f"zestawienie zmian współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s)")

pall.line(x, y_gora, line_width=2,legend_label=f"n_o", line_color="orange")
pall.line(x, y_dol, line_width=2,legend_label=f"n_e", line_color="green")
pall.line(x_usr3, y_gora_usr3, line_width=2,legend_label=f"n_o_usr3", line_color="yellow")
pall.line(x_usr3, y_dol_usr3, line_width=2,legend_label=f"n_e_usr3", line_color="purple")
pall.line(x_usr5, y_gora_usr5, line_width=2,legend_label=f"n_o_usr5", line_color="black")
pall.line(x_usr5, y_dol_usr5, line_width=2,legend_label=f"n_e_usr5", line_color="blue")
pall.xaxis.axis_label = r"$$\color{black} T[°C]$$"
pall.yaxis.axis_label = r"$$\color{black} Δn$$"
pall.legend.label_text_font_size = '15pt'
pall.legend.location =(470, 270)

show(column(p, pusr3, pusr5, pall))
