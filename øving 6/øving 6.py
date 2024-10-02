#Meteorologisk institutt
#en time mellom hver index
Lufttemperatur = [16.1, 16, 16, 15.9, 16.3, 15.8, 15.8, 15.9, 16.1, 16.5, 17, 16.2, 15.8, 16.4, 15.8, 16.2, 15.5, 15.1, 14.7, 13.8, 13.1, 13.2, 12.4, 12.2, 12.1, 11.8, 11.8, 12.1, 12.3, 12.5, 12.3, 12.3, 13.4, 13.4, 13.5, 14.4, 13.7, 14.1, 13.8, 13.8, 12.5, 12.3, 12.4, 11.5, 11.8, 12, 11.8, 11.5, 11.9, 11.5, 10.8, 10.9, 11.2, 11.6, 12.2, 12.8, 13.3, 13.4, 13.5, 14.3, 14.4, 14.5, 14.3, 14.5, 14.9, 13.7, 13.9, 14.1, 13.8, 13.9, 14.2, 14.5]
Lufttrykk = [1013.7, 1013.1, 1012.9, 1012.2, 1011.3, 1011, 1010.6, 1010.2, 1010.2, 1010, 1009.9, 1010.2, 1009.9, 1009.3, 1009.6, 1009.3, 1009.4, 1009.3, 1009.2, 1009.4, 1009.7, 1010, 1010.4, 1010.9, 1011.1, 1011.3, 1011.3, 1011.3, 1011.3, 1011.4, 1011.6, 1011.9, 1012.4, 1012.6, 1012.9, 1013.2, 1013.7, 1014.1, 1014.6, 1015, 1015.4, 1015.7, 1016.1, 1016.4, 1017, 1017.7, 1018.2, 1018.8, 1019.3, 1019.8, 1020, 1020.4, 1020.6, 1020.7, 1021.3, 1021.5, 1021.6, 1021.8, 1021.9, 1021.6, 1021.5, 1021.5, 1021.4, 1020.6, 1019.8, 1019.7, 1019.3, 1018.6, 1018.1, 1017.4, 1017.1, 1016.5]

#trykk og temp logg
#10 sekund mellom hver index
def trykk_templogg():
    with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as file:
        data = file.readlines()
    tid_i_sekunder = []
    barometer_trykk = []
    absolutt_trykk = []
    tempuratur = []
    for line in data:
        line = line.replace(',', '.')
        parts = line.strip().split(';')
        if len(parts) >= 5:
            tid_i_sekunder.append(float(parts[1]))
            barometer_trykk.append(float(parts[2]))
            absolutt_trykk.append(float(parts[3]))
            tempuratur.append(float(parts[4]))
        else:
            tid_i_sekunder.append(None)
            barometer_trykk.append(None)
            absolutt_trykk.append(None)
            tempuratur.append(None)
            
    return tid_i_sekunder, barometer_trykk, absolutt_trykk, tempuratur

tid, barometer, asolutt, temp = trykk_templogg()
print(tid)