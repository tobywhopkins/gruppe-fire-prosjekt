import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

def les_data(filnavn):
    tid, temperatur, trykk = [], [], []
    with open(filnavn, 'r') as fila:
        for line in fila.readlines()[1:]:
            line = line.replace(',', '.').strip().split(';')
            if len(line) >= 5:
                try:
                    tid.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                    temperatur.append(float(line[3]))
                    trykk.append(float(line[4]))
                except ValueError:
                    continue
    return tid, temperatur, trykk

def moving_average(data, n):
    return np.convolve(data, np.ones((n,))/n, mode='valid')

# Les trykk og temperaturdata fra den første filen
fil = 'C:/Users/Bruker/Downloads/datafiler/trykk_og_temperaturlogg_rune_time.csv.txt'
tid_i_sekunder, trykk, absolutt_trykk, temperatur = [], [], [], []
with open(fil, 'r') as fila:
    for line in fila:
        line = line.replace(',', '.')
        deler = line.strip().split(';')
        if len(deler) >= 5 and all(deler[1:5]):
            try:
                tid_i_sekunder.append(float(deler[1]))
                trykk.append(float(deler[2]) * 10)
                absolutt_trykk.append(float(deler[3]) * 10)
                temperatur.append(float(deler[4]))
            except ValueError:
                continue

# Les data fra de andre værstasjoner
fil2 = 'C:/Users/Bruker/Downloads/temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt'

# Sirdal
def les_data_sirdal(filnavn):
    tid, temperatur_sirdal, trykk = [], [], []
    with open(filnavn, 'r') as fila:
        for line in fila.readlines()[1:]:
            line = line.replace(',', '.').strip().split(';')
            if len(line) >= 5 and line[0] == "Sirdal - Sinnes":
                try:
                    tid.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                    temperatur_sirdal.append(float(line[3]))
                    trykk.append(float(line[4]))
                except ValueError:
                    continue
    return tid, temperatur_sirdal, trykk

# Sauda
def les_data_sauda(filnavn):
    tid, temperatur_sauda, trykk = [], [], []
    with open(filnavn, 'r') as fila:
        for line in fila.readlines()[1:]:
            line = line.replace(',', '.').strip().split(';')
            if len(line) >= 5 and line[0] == "Sauda":
                try:
                    tid.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                    temperatur_sauda.append(float(line[3]))
                    trykk.append(float(line[4]))
                except ValueError:
                    continue
    return tid, temperatur_sauda, trykk

# Adjust the start time to 06.10.2021
start_tid = datetime(2021, 6, 10, 0, 0)
tid_datetime = [start_tid + timedelta(seconds=t) for t in tid_i_sekunder]

# Les data fra den andre filen
dato_tid, temperatur2, trykk2 = les_data('C:/Users/Bruker/Downloads/datafiler/temperatur_trykk_met_samme_rune_time_datasett.csv.txt')

# Les data fra Sirdal og Sauda
tid_sirdal, temperatur_sirdal, trykk_sirdal = les_data_sirdal(fil2)
tid_sauda, temperatur_sauda, trykk_sauda = les_data_sauda(fil2)

# Beregn gjennomsnittstemperatur
gjennomsnittstemperatur = moving_average(temperatur, 30)

# Definer start- og sluttidspunkt for temperaturfallet within the new range
start_fall_tid = datetime(2021, 6, 10, 0, 0)
slutt_fall_tid = datetime(2021, 6, 13, 23, 59)

# Finn indeksene for start- og sluttidspunkt i begge datasettene
start_index1 = tid_datetime.index(min(tid_datetime, key=lambda d: abs(d - start_fall_tid)))
slutt_index1 = tid_datetime.index(min(tid_datetime, key=lambda d: abs(d - slutt_fall_tid)))
start_index2 = dato_tid.index(min(dato_tid, key=lambda d: abs(d - start_fall_tid)))
slutt_index2 = dato_tid.index(min(dato_tid, key=lambda d: abs(d - slutt_fall_tid)))

# Opprett linjer som interpolerer mellom temperaturen på de to tidspunktene i begge datasettene
linje_tid1 = [tid_datetime[start_index1], tid_datetime[slutt_index1]]
linje_temp1 = [temperatur[start_index1], temperatur[slutt_index1]]
linje_temp_sirdal = [temperatur_sirdal[start_index1], temperatur_sirdal[slutt_index1]]
linje_temp_sauda = [temperatur_sauda[start_index1], temperatur_sauda[slutt_index1]]
linje_tid2 = [dato_tid[start_index2], dato_tid[slutt_index2]]
linje_temp2 = [temperatur2[start_index2], temperatur2[slutt_index2]]

# Beregn differansen mellom absolutt trykk og barometrisk trykk
trykkdifferanse = [barometrisk - absolutt for absolutt, barometrisk in zip(absolutt_trykk, trykk)]

# Beregn glidende gjennomsnitt for trykkdifferansen (10 forrige og 10 neste)
gjennomsnitt_trykkdifferanse = moving_average(trykkdifferanse, 21)  # 10 forrige og 10 neste, derfor 21 totalt

# Juster tid slik at lengden på tid og gjennomsnitt_trykkdifferanse er lik
tid_for_trykkdifferanse = tid_datetime[10:-10]  # Fjern de første og siste 10 elementene for å matche glidende gjennomsnitt

# Plotting
plt.figure(figsize=(12, 10))

# Temperatur plot
plt.subplot(4, 1, 1)
plt.plot(tid_datetime, temperatur, label="Temperatur (°C) fra Fil 1", color='blue')
plt.plot(tid_datetime[29:], gjennomsnittstemperatur, label="Gjennomsnittstemperatur (°C)", color='orange')
plt.plot(dato_tid, temperatur2, label="Temperatur (°C) fra Fil 2", color='green')
plt.plot(linje_tid1, linje_temp1, label="Temperaturfall (Fil 1)", color='red', linestyle='--')
plt.plot(linje_tid2, linje_temp2, label="Temperaturfall (Fil 2)", color='purple', linestyle='--')
plt.title("Temperatur over Tid")
plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.grid(True)
plt.legend()

# Temperatur Sirdal
plt.subplot(4, 1, 2)
plt.plot(tid_sirdal, temperatur_sirdal, label="Temperatur (°C) fra Sirdal", color='blue')
plt.plot(linje_tid1, linje_temp_sirdal, label="Temperaturfall (Sirdal)", color='red', linestyle='--')
plt.title("Temperatur over Tid (Sirdal)")
plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.grid(True)
plt.legend()

# Temperatur Sauda
plt.subplot(4, 1, 3)
plt.plot(tid_sauda, temperatur_sauda, label="Temperatur (°C) fra Sauda", color='blue')
plt.plot(linje_tid1, linje_temp_sauda, label="Temperaturfall (Sauda)", color='red', linestyle='--')
plt.title("Temperatur over Tid (Sauda)")
plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.grid(True)
plt.legend()

# Trykk plot
plt.subplot(4, 1, 4)
plt.plot(tid_datetime, trykk, label="Trykk (hPa) fra Fil 1", color='orange')
plt.plot(tid_datetime, absolutt_trykk, label="Absolutt Trykk (hPa)", color='blue')
plt.plot(dato_tid, trykk2, label="Lufttrykk (hPa) fra Fil 2", color='green')
plt.title("Trykk over Tid")
plt.xlabel("Tid")
plt.ylabel("Trykk (hPa)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
