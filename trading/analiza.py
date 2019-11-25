import pandas as pd
from matplotlib import pyplot

class Analiza():
    def __init__(self, nazwa_pliku):
        self.dane=pd.DataFrame()
        self.dane=pd.read_csv(nazwa_pliku, index_col="data")
        self.dane.columns=self.dane.columns.str.strip() #zabiera białe znaki z nagłówków
        self.dane["rodzaj trejdu"]=self.dane["rodzaj trejdu"].str.strip() # zabiera białe znaki z danych tabeli
        self.dane["narastajaco"]=""
        self.dane["zysk pkt"]=""
        self.dane.iloc[0,4]=0
        self.dane.iloc[0, 3]=0 # dodaje wartości w pandzie o indeksie 0 dla wierszy i indeksie 3 dla  kolumn. ciekwa ze data nie jest brana pod uwage w liczeniu jako ze jest indeksem chyba!
        self.formatowanie()

    def formatowanie(self):
        dane=self.dane
        for i in range(1,len(dane)):
            dane.iloc[i,3]=dane.iloc[i,2]+dane.iloc[i-1,3]

        for i in range(1,len(dane)):
            dane.iloc[i,4]=dane.iloc[i,2]/dane.iloc[i,0]


    def rodzaj(self, od, do, rodzaj_trejdu): # to definicja do wyciągania, filtorwania
        dane=self.dane
        okres=dane.loc[od:do]
        if rodzaj_trejdu=="a":
            return okres
        elif rodzaj_trejdu in ["m","d","k","on","s"]:
            f=okres["rodzaj trejdu"]==rodzaj_trejdu
            return(okres[f])

    @classmethod
    def rysuj(cls, zbior, kolumna):
        zbior[kolumna].plot(figsize=(8,5))
        pyplot.show()

    @classmethod
    def suma(cls, zbior):
        print(sum(zbior["wynik"]))


if __name__=="__main__":
    start=Analiza("baza.csv")

#_____________________________________________________________________
badany_okres_od=02.01   # miesiac.dzien
badany_okres_do=09.09   # miesiac.dzien
rodzaj_trejdu="a"   # m,k,d,on,s, a (dla all)
kolumna="wynik"     #wynik, narastajaco, zysk_pkt
zbior=(Analiza.rodzaj(start,badany_okres_od,badany_okres_do, rodzaj_trejdu))
#print(zbior)
#rysuj=Analiza.rysuj(zbior,kolumna)
#suma=Analiza.suma(zbior)








