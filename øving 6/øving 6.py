
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
tid_i_sekunder, trykk, absolutt_trykk, temperatur = [], [], [], []
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as fila:
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
# Sirdal
def les_data():
    tid, temperatur, trykk = [], [], []
    with open('temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt', 'r') as fila:
        for line in fila.readlines()[1:]:
            line = line.replace(',', '.').strip().split(';')
            if len(line) >= 5 and line[0] == "Sirdal - Sinnes":
                try:
                    tid.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                    temperatur.append(float(line[3]))
                    trykk.append(float(line[4]))
                except ValueError:
                    continue
    return tid, temperatur, trykk

# Sauda
def les_data():
    tid, temperatur, trykk = [], [], []
    with open('temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt', 'r') as fila:
        for line in fila.readlines()[1:]:
            line = line.replace(',', '.').strip().split(';')
            if len(line) >= 5 and line[0] == "Sauda":
                try:
                    tid.append(datetime.strptime(line[2], '%d.%m.%Y %H:%M'))
                    temperatur.append(float(line[3]))
                    trykk.append(float(line[4]))
                except ValueError:
                    continue
    return tid, temperatur, trykk

# Beregn tid i datetime-format for første fil
start_tid = datetime(2021, 6, 11, 14, 23)
tid_datetime = [start_tid + timedelta(seconds=t) for t in tid_i_sekunder]

# Les data fra den andre filen
dato_tid, temperatur2, trykk2 = les_data('temperatur_trykk_met_samme_rune_time_datasett.csv.txt')

# Beregn gjennomsnittstemperatur
gjennomsnittstemperatur = moving_average(temperatur, 30)

# Definer start- og sluttidspunkt for temperaturfallet
start_fall_tid = datetime(2021, 6, 11, 17, 31)
slutt_fall_tid = datetime(2021, 6, 12, 3, 5)

# Finn indeksene for start- og sluttidspunkt i begge datasettene
start_index1 = tid_datetime.index(min(tid_datetime, key=lambda d: abs(d - start_fall_tid)))
slutt_index1 = tid_datetime.index(min(tid_datetime, key=lambda d: abs(d - slutt_fall_tid)))
start_index2 = dato_tid.index(min(dato_tid, key=lambda d: abs(d - start_fall_tid)))
slutt_index2 = dato_tid.index(min(dato_tid, key=lambda d: abs(d - slutt_fall_tid)))

# Opprett linjer som interpolerer mellom temperaturen på de to tidspunktene i begge datasettene
linje_tid1 = [tid_datetime[start_index1], tid_datetime[slutt_index1]]
linje_temp1 = [temperatur[start_index1], temperatur[slutt_index1]]
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

# Tempuratur Sirdal

# Tempuratur Sauda


# Trykk plot
plt.subplot(4, 1, 2)
plt.plot(tid_datetime, trykk, label="Trykk (hPa) fra Fil 1", color='orange')
plt.plot(tid_datetime, absolutt_trykk, label="Absolutt Trykk (hPa)", color='blue')
plt.plot(dato_tid, trykk2, label="Lufttrykk (hPa) fra Fil 2", color='green')
plt.title("Trykk over Tid")
plt.xlabel("Tid")
plt.ylabel("Trykk (hPa)")
plt.grid(True)
plt.legend()

# Histogram plot
plt.subplot(4, 1, 3)
bins = np.arange(min(min(temperatur), min(temperatur2)), max(max(temperatur), max(temperatur2)) + 1, 1)
plt.hist(temperatur, bins=bins, alpha=0.5, label="Temperatur fra Fil 1", color='blue', edgecolor='black')
plt.hist(temperatur2, bins=bins, alpha=0.5, label="Temperatur fra Fil 2", color='green', edgecolor='black')
plt.title("Histogram over Temperaturer")
plt.xlabel("Temperatur (°C)")
plt.ylabel("Antall målinger")
plt.legend()

# Trykkdifferanse plot
plt.subplot(4, 1, 4)
plt.plot(tid_for_trykkdifferanse, gjennomsnitt_trykkdifferanse, label="Gjennomsnittlig Trykkdifferanse", color='purple')
plt.title("Trykkdifferanse (Absolutt Trykk - Barometrisk Trykk)")
plt.xlabel("Tid")
plt.ylabel("Trykkdifferanse (hPa)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()



# Funksjon for å finne tidspunktene som har samme dag og time i begge datasett
def match_times(tid1, tid2):
    matched_indices = []
    for t1 in tid1:
        # Hente dato og time (uten minutter og sekunder)
        tid1_justert = t1.replace(minute=0, second=0, microsecond=0)
        
        # Finn nærmeste tid i tid2
        closest_time = min(tid2, key=lambda t2: abs(t2 - tid1_justert))
        tid2_justert = closest_time.replace(minute=0, second=0, microsecond=0)
        
        # Hvis de justerte tidene stemmer overens, legg til indekset
        if tid1_justert == tid2_justert:
            matched_indices.append((tid1.index(t1), tid2.index(closest_time)))
    
    return matched_indices

# Finn matchende tidspunkter
matched_indices = match_times(tid_datetime, dato_tid)

# Beregn temperatur- og trykkforskjellen for matchende tidspunkter
temperatur_diff = []
trykk_diff = []
for idx1, idx2 in matched_indices:
    temp_diff = abs(temperatur[idx1] - temperatur2[idx2])  # Temperaturforskjell
    press_diff = abs(trykk[idx1] - trykk2[idx2])  # Trykkforskjell
    temperatur_diff.append(temp_diff)
    trykk_diff.append(press_diff)

# Finn minimum og maksimum forskjell
min_temp_diff_idx = np.argmin(temperatur_diff)
max_temp_diff_idx = np.argmax(temperatur_diff)
min_press_diff_idx = np.argmin(trykk_diff)
max_press_diff_idx = np.argmax(trykk_diff)

# Tidspunktene der forskjellen er minst og størst
min_temp_diff_time = tid_datetime[matched_indices[min_temp_diff_idx][0]]
max_temp_diff_time = tid_datetime[matched_indices[max_temp_diff_idx][0]]
min_press_diff_time = tid_datetime[matched_indices[min_press_diff_idx][0]]
max_press_diff_time = tid_datetime[matched_indices[max_press_diff_idx][0]]

# Beregn gjennomsnittlig forskjell
average_temp_diff = np.mean(temperatur_diff)
average_press_diff = np.mean(trykk_diff)

# Print resultatene
print(f"Minimum temperaturforskjell: {temperatur_diff[min_temp_diff_idx]} °C ved tid {min_temp_diff_time}")
print(f"Maximum temperaturforskjell: {temperatur_diff[max_temp_diff_idx]} °C ved tid {max_temp_diff_time}")
print(f"Minimum trykkforskjell: {trykk_diff[min_press_diff_idx]} hPa ved tid {min_press_diff_time}")
print(f"Maximum trykkforskjell: {trykk_diff[max_press_diff_idx]} hPa ved tid {max_press_diff_time}")
print(f"Gjennomsnittlig temperaturforskjell: {average_temp_diff} °C")
print(f"Gjennomsnittlig trykkforskjell: {average_press_diff} hPa")


