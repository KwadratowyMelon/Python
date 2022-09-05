import glob
from PIL import Image
import scipy.interpolate
import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import Div
from bokeh.palettes import Spectral


# stale globalne ktorych wartosc wpisac musi uzytkownik
# na początku scieżka relatywna do aktualnego umieszczenia programu
imagesPath = glob.glob("pomiary\\styczen\\1110_step_100s_stare\\*.jpg")
# temperatura pierwszego zarejestrowanego zdjęcia
t_start = 20.3
# temperatura ostatniego zarejestrowanego zdjęcia
t_end = 44.6
# nazwa badanego ciekłego kryształu
nazwa_cieklego_krysztalu = "6CHBT"
# step przyjęty podczas przeprowadzania pomiarów, nie wyklucza się że będzie on inny dla kryształów spoza zakresu badanych
step = 100
# odległość między środkami prążków, zmierzona z dok`ladnością co do piksela w programie graficznym`
m = 65

# inicjacja globalnych stałych i tablic

Xob = []
Yob = []
Dopob = []
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
y_stos = []
y_stos.append(0)
j = 0
lamb = 532 * pow(10,-9)
d = 50 * pow(10, -6)
x = []
Xarray = np.arange(1,1281)
Xref = np.arange(641,1281)
YaxisGora = []
YaxisDol = []
YaxisRef = []
wsp_gora = 0
wsp_dol = 0

# funkcja wczytująca jasność pikseli ze zdjęcia, zwracająca tablicę

def getColorValues(image, c):  # r = 0, g = 1, b = 2
    array = []
    pix = image.load()
    for i in range(image.size[0]):
        kolor = pix[i, c] 
        array.append(kolor)
    return array

# funkcja sprawdzająca czy jasny piksel znajduje się na kolejnym prążku, jeśli tak to dodaj obecne położenie do kolejnych mierzonych wartości
def correct_values(data):
    result = []
    result.append(0)
    for i in range(1, len(data)):
        val = data[i-1] - data[i]
        if abs(val) > (m / 2):
            val = 0
        result.append(result[i-1] + val)
    return result

#funkcja uśredniająca pięć sąsiednich wartości
def usrednione_5(data):
    usrednione = []
    i = 0
    while i < len(data) - 4:
        var = (data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4])/5
        usrednione.append(var)
        i += 5
    return usrednione

# funkcja uśredniająca trzy sąsiednie wartości
def usrednione_3(data):
    usrednione = []
    i = 0
    while i < len(data) - 2:
        var = (data[i]+data[i+1]+data[i+2])/3
        usrednione.append(var)
        i += 3
    return usrednione

# utworzenie pliku zawierającego tablicę wartości przedziału temperaturowego
with open("Zaxis.txt", "w+") as file:
        for i in range(len(imagesPath)):
            z = t_start + i*(t_end-t_start)/(len(imagesPath))
            x.append(z)
            file.write(f"{z} \n")
        file.close()

# utworznie pliku zawierającego tablicę wartości szerekości zdjęcia
with open("Xaxis.txt", "w+") as file:
    for i in range(len(Xarray)):
        file.write(f"{i} \n")
file.close()

# dla każdego zdjęcia w ścieżce wykonaj pętle
for path in imagesPath:
    Ygora = []
    Ydol = []
    Yref = []
    image = Image.open(path)
    # przybliżone wysokości na jakiej znajdują się prążki
    gora = int(image.size[1] / 4)
    ref = int(image.size[1] / 2)
    dol = int(3 * image.size[1] / 4)
    # pobranie wycinków zdjęć na zadanych wysokościach o grubości jednego piksela
    resultGora = image.crop((0, gora, image.size[0], gora + 1))
    resultDol = image.crop((0, dol, image.size[0], dol + 1))
    resultRef = image.crop((image.size[0]/2, ref, image.size[0], ref + 1))
    # pobranie wartości pikseli z wycinków przy pomocy wcześniej napisanej funkcji
    colorValuesGora = getColorValues(resultGora, 0)
    colorValuesDol = getColorValues(resultDol, 0)
    colorValuesRef = getColorValues(resultRef, 0)
    # utworzenie pliku tekstowego z wartościami wycinka górnego
    with open("GoraYmatrix.txt", "a+") as file:

        for i in range(image.size[0]):
            Ygora.append(colorValuesGora[i][1])
            converted_num = str(colorValuesGora[i][1])
            file.write(f"{converted_num} \t")
        file.write("\n")
        file.close()

    # utworznie pliku tekstowego z wartościami wycinka dolnego
    with open("DolYmatrix.txt", "a+") as file:
        for i in range(image.size[0]):
            Ydol.append(colorValuesDol[i][1])
            converted_num = str(colorValuesDol[i][1])
            file.write(f"{converted_num} \t")
        file.write("\n")
        file.close()

    # utworznie pliku tekstowego z wartościami wycinka środkowego
    with open("RefYmatrix.txt", "a+") as file:
        for i in range(int(image.size[0] - image.size[0]/2)):
            Yref = np.append(Yref, colorValuesRef[i][1])
            converted_num = str(colorValuesRef[i][1])
            file.write(f"{converted_num} \t")
        file.write("\n")
        file.close()

    # zastosowanie dopasowania funkcji wielomianowej do tablic wartości pikseli z wycinków
    interpolation_gora = scipy.interpolate.BarycentricInterpolator(Xarray, Ygora)
    interpolation_dol = scipy.interpolate.BarycentricInterpolator(Xarray, Ydol)
    interpolation_ref = scipy.interpolate.BarycentricInterpolator(Xref, Yref)
    # policzenie wartości przybliżonych dla dopasowania
    root_gora = interpolation_gora.__call__(Xarray)
    root_dol = interpolation_dol.__call__(Xarray)
    root_ref = interpolation_dol.__call__(Xref)
    # zlokalizownie położenia maksimum
    max_gora = np.argmax(root_gora)
    max_dol = np.argmax(root_dol)
    max_ref = np.argmax(root_ref)

    # utworzenie i dopisanie położenia maksimum górnych prążków opracowywanego zdjęcia
    with open("polozenie_max_gora.txt", "a+") as file:
        YaxisGora.append(max_gora)
        converted_num = str(max_gora)
        file.write(f"{converted_num} \n")
    file.close()

    # utworzenie i dopisanie położenia maksimum dolnych prążków opracowywanego zdjęcia
    with open("polozenie_max_dol.txt", "a+") as file:
        YaxisDol.append(max_dol)
        converted_num = str(max_dol)
        file.write(f"{converted_num} \n")
    file.close()

       # utworzenie i dopisanie położenia maksimum prążków wiązki referencyjnej opracowywanego zdjęcia
    with open("polozenie_max_ref.txt", "a+") as file:
        YaxisRef.append(max_ref)
        converted_num = str(max_ref)
        file.write(f"{converted_num} \n")
    file.close()


# skorygowanie otrzymanych położen maksimum funkcją wykrywającą przeskok między prązkami
final_pixel_pos_gora = correct_values(YaxisGora)
final_pixel_pos_dol = correct_values(YaxisDol)
final_pixel_pos_ref = correct_values(YaxisRef)

# policzenie i dodanie wartości utraconej w trakcie przeprowadzania pomiarów przy pomocy prążków referencyjncyh dla prążków górnych
for i in range(len(final_pixel_pos_ref)):
    final_pixel_pos_ref[i] = wsp_gora * final_pixel_pos_ref[i]

corrected_gora = np.add(final_pixel_pos_gora, final_pixel_pos_ref)

# policzenie i odjęcie wartości nabytej w trakcie przeprowadzania pomiarów przy pomocy prążków referencyjncyh dla prążków dolnych
for i in range(len(final_pixel_pos_ref)):
    final_pixel_pos_ref[i] = wsp_dol * final_pixel_pos_ref[i] #/ wsp_gora

corrected_dol = np.subtract(final_pixel_pos_dol,  final_pixel_pos_ref)

# uśrednienie wartości 
avg_5_dol = usrednione_5(final_pixel_pos_dol)
avg_5_gora = usrednione_5(final_pixel_pos_gora)
avg_5_gora = usrednione_5(final_pixel_pos_ref)

avg_3_dol = usrednione_3(final_pixel_pos_dol)
avg_3_gora = usrednione_3(final_pixel_pos_gora)
avg_3_gora = usrednione_3(final_pixel_pos_ref)


# zastosowanie wzoru na przesunięcie fazy dla serii danych:
# policzonego przesunięcia położenia maksimum prążków
for i in range(1, len(final_pixel_pos_dol)):

    y_dol_temp = (final_pixel_pos_dol[i] * lamb)/(d * m)
    y_gora_temp = (final_pixel_pos_gora[i] * lamb)/(d * m)
    y_dol.append(y_dol_temp)
    y_gora.append(y_gora_temp)

# z uwzględnieniem prążków referencyjncyh
for i in range(1, len(corrected_gora)):
    corrected_gora[i] = (corrected_gora[i] * lamb)/(d * m)
    corrected_dol[i] = (corrected_dol[i] * lamb)/(d * m)

# uśrednionych 
for i in range(1, len(avg_3_dol)):
    y_dol_avg_3 = (avg_3_dol[i] * lamb)/(d * m)
    y_gora_avg_3 = (avg_3_gora[i] * lamb)/(d * m)
    y_dol_usr3.append(y_dol_avg_3)
    y_gora_usr3.append(y_gora_avg_3)
    
for i in range(1, len(avg_5_dol)):
    y_dol_avg_5 = (avg_5_dol[i] * lamb)/(d * m)
    y_gora_avg_5 = (avg_5_gora[i] * lamb)/(d * m)
    y_dol_usr5.append(y_dol_avg_5)
    y_gora_usr5.append(y_gora_avg_5)


# dopasowanie serii temperatur do danych uśrednionych
for i in range(len(y_dol_usr3)):
    t = t_start + i*(t_end-t_start)/(len(y_dol_usr3))
    x_usr3.append(t)


for i in range(len(y_dol_usr5)):
    t = t_start + i*(t_end-t_start)/(len(y_dol_usr5))
    x_usr5.append(t)

# utworzenie i opisanie wykresow przy pomocy wczesniej policzonych oraz otrzymanych danych
p = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s)")

p.dot(x, y_gora, size=15,legend_label=f"n_o", line_color="orange")
p.dot(x, y_dol, size=15,legend_label=f"n_e", line_color="green")
p.xaxis.axis_label = r"$$\color{black} T[°C]$$"
p.yaxis.axis_label = r"$$\color{black} Δn$$"
p.legend.label_text_font_size = '15pt'
p.legend.location =(5,350)

pop = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s)")

pop.dot(x, corrected_gora, size=15,legend_label=f"n_o", line_color="orange")
pop.dot(x, corrected_dol, size=15,legend_label=f"n_e", line_color="green")
pop.xaxis.axis_label = r"$$\color{black} T[°C]$$"
pop.yaxis.axis_label = r"$$\color{black} Δn$$"
pop.legend.label_text_font_size = '15pt'
pop.legend.location =(5,350)

pusr3 = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s, usr-3)")

pusr3.dot(x_usr3, y_gora_usr3, size=15,legend_label=f"n_o", line_color="orange")
pusr3.dot(x_usr3, y_dol_usr3, size=15,legend_label=f"n_e", line_color="green")
pusr3.xaxis.axis_label = r"$$\color{black} T[°C]$$"
pusr3.yaxis.axis_label = r"$$\color{black} Δn$$"
pusr3.legend.label_text_font_size = '15pt'
pusr3.legend.location =(5, 350)

pusr5 = figure(
    width=700, height=500, toolbar_location="right",
    title=f"zmiana współczynników załamania {nazwa_cieklego_krysztalu} w zmiennej temperaturze (step_{step}s, usr-5)")

pusr5.dot(x_usr5, y_gora_usr5, size=15,legend_label=f"n_o", line_color="orange")
pusr5.dot(x_usr5, y_dol_usr5, size=15,legend_label=f"n_e", line_color="green")
pusr5.xaxis.axis_label = r"$$\color{black} T[°C]$$"
pusr5.yaxis.axis_label = r"$$\color{black} Δn$$"
pusr5.legend.label_text_font_size = '15pt'
pusr5.legend.location =(5, 350)


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
p.xaxis.axis_label_text_font_size = '13pt'
p.yaxis.axis_label_text_font_size = '13pt'
p.xaxis.major_label_text_font_size = '10pt'
p.yaxis.major_label_text_font_size = '10pt'
p.legend.label_text_font_size = '13pt'
p.title.text_font_size = '13pt'
pall.legend.location =(470, 160)

# wyswietlenie wykresow w kolumnie
show(column(p, pop, pusr3, pusr5,  pall))