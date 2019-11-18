# trading 2.4 tego samego dnia wersja wyżej... dlaczego? bo dodałem feed ze strony internetowej a dokładniej z investing!!!
# poprawnie spiocha, zastąpienie time.sleep timeoutem żeby móc go przerywać gdy zamykam! działa!
# dodanie importu do archiwum oraz drobne poprawki w strategii z "sila". wyłącznik feeda poza godzinami otwarcia daxa
# dodanie usuwania bazy po czasie(za_szybko_w_czasie)
# dodanie expiry zeby unikać trejdowania do 13 tej tego dnia
# trading 2,5 dodanie ratio pomiędzy dax a cac
import requests
import winsound
import datetime, time 
import os
import threading
from alpha_vantage.timeseries import TimeSeries


typ=""
alfa_feed_message=""
inv_feed_message=" Investing feed"
h_l_message=""
wersja="Trading 2.5" 
holidays=[527,704,902,1014,1111,1128,1225]
mocne_dane=[410,426,503,522,530,603,606,607,619,627,701,705,710,725,726,731,801,802,821,829,906,912,918,926,1004,1009,1024,1030,1101,1120,1127,1206,
       1211,1212,1220]
expiry=[816,920,1018,1115,1220]
alfa_feed_pause=True
investing_feed_pause=False
working=True
check_user=True
check_programisty=False
check_zamkniecie=True
pietnastka_rano=False
blisko_ekstremow=False
blisko_zamkniecia=False
kontry=True
sila=False
pytanie1=True
kasowanie_feeda=False
maksymalne_odch=100
minimalne_odch=maksymalne_odch/2
ogranicznie_czasu=15
amerykanie=12.3
blisko_danych=10/100
ekstrema=10
low=0
high=0
luka=0
check_zniesienia=0
zniesienia=[0.01]
dzienny_trend=0
odleglosc_do_SL=22
SL=0 
kierunek=0
opo = []
wsp = []
dane={}
Haje=[]
haj_time=[]
low_time=[]
Lowy=[]
pkt_dax=[]
time_dax=[]
kierunki=[]
ratio_list=[]
za_szybko_w_czasie=0.3
konwentor_feeda=12000
odswiezanie_feeda=5.0 
current=0
cac=0
roznica_czasu=6 # to do feeda. alfa feed dokładnie
spioch=0
ratio_min=0
ratio_max=1000


print(wersja+typ+alfa_feed_message+inv_feed_message+h_l_message)
print("\n"*2)
zamkniecie=int(input("Jaka cena zamknięcia?"))
usa=False
usa_kierunek=0
if int(input("USA odjechały? Ewentualnie HangSeng? press1"))==1:
    usa=True
    while not usa_kierunek==-1 and not usa_kierunek==1:
        usa_kierunek=int(input("Kupili (1)? Sprzedali(-1)?"))
trend=int(input("Główny kierunek? Rynek niedźwiedzia-1; Neutralny 0; Rynek byka 1\n"))
if trend==1 or trend==-1:
    if int(input("Czy rynek silny?. Wciśnij 1 dla tak"))==1:
        sila=True

            
def checklista():
    global low
    global high
    global check_user
    global check_programisty
    global working
    global za_wczesnie
    za_wczesnie=False
    zegarek()
    if czas<18:
        wyczysc()
        zegarek()
        if brak_feeda:
            print("Wprowadź feed, bo ten co masz jest sprzed pół godziny conajmniej\n")
            pause()
        while low>=high or low==0 or high==0: 
            print("Wprowadź low/high")
            print(low,"/",high)
            print("Aktualny low: ",low)
            zmienna_low=int(input("Jaki low? Wciśnij 0 żeby nie zmieniać:"))
            if zmienna_low!=0:
                low=zmienna_low
            print("Aktualny high: ",high)
            zmienna_high=int(input("Jaki high? Wciśnij 0 żeby nie zmieniać:"))
            if zmienna_high!=0:
                high=zmienna_high
        wyczysc()
        if czas<10:
            za_wczesnie=True
        if amerykanie<czas<=ogranicznie_czasu:
            print("\n" * 10)
            print("Uważaj bo amerykanie grasują, przy trejdzie patrz na SP500!!!")
            pause()
        elif czas>=ogranicznie_czasu:
            print("\n" * 10)
            print("Jest po {} tej, czego tutaj szukasz".format(ogranicznie_czasu))
            pause()
            check_user=False
            working=False
            e.set()
            exit()
        for i in expiry:
            if data==i:
                print("Dzisiaj wygaśnięcie opcji na dax! ty sie trzymaj z daleka przynajmniej do 13 tej. \nJeśli wejdziesz w pozycje to tylko połowa. Rynek generuje dużo błędnych sygnałów")
                print("\n"*2)
                pause()
        for i in holidays:
            if data==i:
                print("Dzisiaj bank holiday w usa! Uważaj, zagrożenie choppy day!")
                print("\n"*2)
                pause()
            elif data==i+1:
                print("Wczoraj był bank holiday w usa! Uważaj, ciągle jest zagrożenie choppy day!")
                print("\n"*2)
                pause()
        for i in mocne_dane:
            if data==i:
                print("Dzisiaj mocne dane! To może zmienić kształt dnia (mała zmienność, choppy)")
                print("\n"*2)
                pause()
        dict_sorted=dict(sorted(dane.items()))
        for key, value in dict_sorted.items():
            if value==2:
                print("Mocne dane dzisiaj, pamiętaj o tym bo to daje efekt na cały dzień. Godzina mocnych danych: {}".format(key))
                print("\n" * 2)
                pause()
        if len(dict_sorted)>0:
            for key, value in dict_sorted.items():
                if key>czas:
                    if key-czas-blisko_danych<=0 and value>0:
                        print("\n" * 10)
                        print("Za blisko danych kolego, wróc PO!!!")
                        pause()
                    elif key-czas-blisko_danych<=0 and value==0:
                        print("\n" * 10)
                        print("Mało istotne dane blisko, miej to na uwadze!")
                        pause()
                        dalej()
                    else:
                        dalej()
        else:
            dalej()


def dalej():
    choppy = int(input("Press 1 dla choppy market, 0 dla nie."))
    if choppy==1:
        print("\n" * 10)
        print("choppy market, daj se siana!!!")
        exit()
    pytania()
    test_ekstremow()
    filtr_zmiennosci()
    test_zniesienia()
    strategia()
                    
    

def zegarek():
    global czas
    global data
    global minuty
    global sekundy
    global dzien
    now = datetime.datetime.now()
    godzina = int(now.strftime("%H"))
    minuty = int(now.strftime("%M"))
    sekundy = int(now.strftime("%S"))
    dzien = int(now.day)
    czas = float(godzina + (minuty /100))
    data = ((100*now.month)+now.day)
    
    

def pytania():
    global kierunek
    global kierunki
    global SL
    global pietnastka_rano
    global pietnastka
    global srednie
    global zyskownosc
    global Haje
    global Lowy
    global haj_time
    global low_time
    zyskownosc=None
    pietnastka=False
    kierunek=0
    SL=0
    test_pietnastki=int(input("Trzy 15tki z rzędu? wciśnij (1)"))
    if czas<10.3 and test_pietnastki==1:
        pietnastka_rano=True
    if test_pietnastki==1:
        pietnastka=True
    if int(input("Czy średnie przecięte lub przeciąć się mogą za 5 minut? Wciśnij (1)"))==1:
        srednie=True
    else:
        srednie=False
    while not (kierunek==1 or kierunek==-1):
        kierunek=int(input("Kupno (1), sprzedaż (-1)\n"))
    while SL==0:
        SL=int(input("Gdzie Stop Loss?"))
    Haje.append(SL)
    Lowy.append(SL)
    zegarek()
    haj_time.append(czas)
    low_time.append(czas)
    kierunki.append(kierunek)
    if len(kierunki)>1:
        if int(kierunki[-2])==int(kierunek):
            zmienna=int(input("Drugi trejd w te samą stronę... Czy poprzedni był zyskowny? Wciśnij 1 dla zysku, 0 dla straty \n"))
            if zmienna==1:
                zyskownosc=True
            elif zmienna==0:
                zyskownosc=False
            else:
                zyskownosc=None
    
    
def test_ekstremow():
    global low
    global high
    global wsp
    global opo
    global luka
    global check_zamkniecie
    global blisko_ekstremow
    global blisko_zamkniecia
    blisko_zamkniecia=False
    blisko_ekstremow=False
    if SL!=0 and SL>high:
        high=SL
    elif SL!=0 and SL<low:
        low=SL
    zmienna=[]
    for i in range(len(wsp)): 
        if wsp[i]<=low:
            zmienna.append(wsp[i])
    wsp=zmienna
    wsp.sort(reverse=True)
    zmienna=[]
    for i in range(len(opo)):
        if opo[i]>=high:
            zmienna.append(opo[i])
    opo=zmienna
    opo.sort()
    check=0    
    while len(wsp)<2 or len(opo)<2 or check==0:
        while len(wsp)<2:              
            print("\n" * 10)        
            print("Brak wsparć!! Uzupełnij dane. Brakuje {} wsparć.".format(2-len(wsp)))
            pause()
            add_wsparcia()
        while len(opo)<2:
            print("\n" * 10)
            print("Brak oporów!!! Uzupełnij dane. Brakuje {} oporów.".format(2-len(opo)))
            pause()
            add_opory()
        while max(wsp)>=min(opo):
            print("Popraw wsparcia i opory bo cyfry się nie zgadzają")
            wsp=[]
            opo=[]
            add_wsparcia()
            print("\n"*2)
            add_opory()
        zmienna=[]
        for i in range(len(wsp)): 
            if wsp[i]<=low:
                zmienna.append(wsp[i])
        wsp=zmienna
        wsp.sort(reverse=True)
        zmienna=[]
        for i in range(len(opo)):
            if opo[i]>=high:
                zmienna.append(opo[i])
        opo=zmienna
        opo.sort()
        check+=1
                
    if low!=wsp[0]: 
        wsp.append(low)
        wsp.sort(reverse=True)
    if high!=opo[0]:
        opo.append(high)
        opo.sort()

    if high<zamkniecie: 
        luka=(high-zamkniecie)
    elif low>zamkniecie:
        luka=(low-zamkniecie)
    else:
        luka=0

    while check_zamkniecie:
        if high<zamkniecie: 
            opo.append(zamkniecie)
            opo.sort()
        elif low>zamkniecie:
            wsp.append(zamkniecie)
            wsp.sort(reverse=True)
        check_zamkniecie=False
    if ((SL==low and SL-wsp[1]<ekstrema and kierunek==1) or (SL!=low and SL-wsp[0]<ekstrema and kierunek==1)) or \
       ((SL==high and opo[1]-SL<ekstrema and kierunek==-1) or (SL!=high and opo[0]-SL<ekstrema and kierunek==-1)):
        blisko_ekstremow=True
    if luka!=0 and ((luka>0 and SL-zamkniecie<20) or (luka<0 and zamkniecie-SL<20)):
        blisko_zamkniecia=True
       
    
    
def filtr_zmiennosci():
    global Lowy
    global Haje
    global low_time
    global haj_time
    global pkt_dax
    global time_dax
    global wariant1
    global wariant2
    global wariant3
    global wariant4
    global wariant5
    global kontra
    global duza_kontra
    global mala_kontra
    global kontynuacja
    global dzienny_trend
    global pytanie1
    global za_szybko
    wariant1=False
    wariant2=False
    wariant3=False
    wariant4=False
    wariant5=False
    kontra=False
    duza_kontra=False
    mala_kontra=False
    kontynuacja=False
    za_szybko=False 
    if (high-low)<minimalne_odch and (zamkniecie-low)<1.3*minimalne_odch and (high-zamkniecie)<1.3*minimalne_odch and \
       not usa and 11<czas<amerykanie and not pietnastka and not pietnastka_rano:
        wariant5=True 
    elif (high-low)<minimalne_odch and (zamkniecie-low)<1.3*minimalne_odch and (high-zamkniecie)<1.3*minimalne_odch and \
       (usa or pietnastka or pietnastka_rano or not 11<czas<amerykanie):
        wariant4=True 
    elif (zamkniecie-low>maksymalne_odch or high-zamkniecie>maksymalne_odch) and high-low>maksymalne_odch:
        wariant1=True 
    elif (zamkniecie-low>maksymalne_odch or high-zamkniecie>maksymalne_odch) and high-low<maksymalne_odch:
        wariant2=True 
    elif not(zamkniecie-low>maksymalne_odch or high-zamkniecie>maksymalne_odch) and high-low>maksymalne_odch:
        wariant3=True 
    index_czasu_low=[] 
    index_czasu_high=[]
    index_czasu_pkt=[] # to dla investing feed
    for i in range(len(low_time)): # musi być taki długi bo mam format HH.MM a przeciez 6.59 i 7 to nie różnica 41 minut!
        if (int(czas)+((czas-int(czas))*1.66666666666667))-(int(low_time[i])+((low_time[i]-int(low_time[i]))*1.66666666666667))<=(int(za_szybko_w_czasie)+((za_szybko_w_czasie-int(za_szybko_w_czasie))*1.66666666666667)): 
            index_czasu_low.append(i)

    for i in range(len(haj_time)):
        if (int(czas)+((czas-int(czas))*1.66666666666667))-(int(haj_time[i])+((haj_time[i]-int(haj_time[i]))*1.66666666666667))<=(int(za_szybko_w_czasie)+((za_szybko_w_czasie-int(za_szybko_w_czasie))*1.66666666666667)): 
            index_czasu_high.append(i)

    for i in range(len(time_dax)):
        if (int(czas)+((czas-int(czas))*1.66666666666667))-(int(time_dax[i])+((time_dax[i]-int(time_dax[i]))*1.66666666666667))<=(int(za_szybko_w_czasie)+((za_szybko_w_czasie-int(za_szybko_w_czasie))*1.66666666666667)):
            index_czasu_pkt.append(i)

    for i in index_czasu_pkt:
        if kierunek==1 and (int(pkt_dax[i])-SL>=minimalne_odch):
            za_szybko=True
        elif kierunek==-1 and (SL-int(pkt_dax[i])>=minimalne_odch):
            za_szybko=True

    for i in index_czasu_low:
        if kierunek==-1 and (SL-int(Lowy[i])>=minimalne_odch):
            za_szybko=True
    for i in index_czasu_high:
        if kierunek==1 and (int(Haje[i])-SL>=minimalne_odch):
            za_szybko=True

    if kasowanie_feeda: # to poniżej do kasowania bazy feedów jeśli czas powyżej (za_szybko_w_czasie)
        zmienna_dax=[] 
        zmienna_czas=[]
        for i in range(len(index_czasu_low)):
            zmienna_dax.append(Lowy[index_czasu_low[i]])
            zmienna_czas.append(low_time[index_czasu_low[i]])
        Lowy=zmienna_dax
        low_time=zmienna_czas
        
        zmienna_dax=[]
        zmienna_czas=[]
        for i in range(len(index_czasu_high)):
            zmienna_dax.append(Haje[index_czasu_high[i]])
            zmienna_czas.append(haj_time[index_czasu_high[i]])
        Haje=zmienna_dax
        haj_time=zmienna_czas

        zmienna_dax=[]
        zmienna_czas=[]
        for i in range(len(index_czasu_pkt)):
            zmienna_dax.append(pkt_dax[index_czasu_pkt[i]])
            zmienna_czas.append(time_dax[index_czasu_pkt[i]])
        pkt_dax=zmienna_dax
        time_dax=zmienna_czas

    if not high-low>maksymalne_odch and (not pietnastka or kierunek==usa_kierunek) and not za_szybko and not za_wczesnie:
        kontra=True 
    if kierunek==trend and high-low>minimalne_odch:
        duza_kontra=True
    if zamkniecie-low>maksymalne_odch or high-zamkniecie>maksymalne_odch or high-low>maksymalne_odch or pietnastka or za_szybko or za_wczesnie:
        mala_kontra=True
    if not wariant5: 
        kontynuacja=True
    if (high-low>maksymalne_odch or pietnastka_rano) and pytanie1:
        dzienny_trend=int(input("W jakim kierunku idzie dax lub jaki był ostatni ruch? (dla liczenia zniesienia) 1byki, -1 niedźwiedzie, 0 bez trendu\n"))
        pytanie1=False
    

    

def test_zniesienia():
    global check_zniesienia
    global zniesienia
    global zniesienie
    zniesienie=0
    if check_zniesienia==0:
        if (pietnastka_rano or high-low>maksymalne_odch) and dzienny_trend==1:
            zniesienie=(high-SL)/(high-low)
            zniesienia.append(zniesienie)
        elif (pietnastka_rano or high-low>maksymalne_odch) and dzienny_trend==-1:
            zniesienie=(SL-low)/(high-low)
            zniesienia.append(zniesienie)
    if max(zniesienia)>0.61:
        check_zniesienia=1
        zniesienia=[0.01]
    
        
    
def strategia():
    global kontry
    wyczysc()
    if blisko_zamkniecia:
        print("\n"*5)
        print("Za blisko zamknięcia!!! Duże prawdopodobieństwo że rynek będzie zamykał lukę")
        pause() 
    if blisko_ekstremow and not (wariant5 and kierunek==trend) and not (wariant4 and usa_kierunek==kierunek) and kierunek==1:
        print("\n"*5)
        print("Za blisko ekstremów!!! Chyba ze Dax na poziomie min {}pkt.".format(wsp[0]+20))
        pause()
    elif blisko_ekstremow and not (wariant5 and kierunek==trend) and not (wariant4 and usa_kierunek==kierunek) and kierunek==-1:
        print("\n"*5)
        print("Za blisko ekstremów!!! Chyba ze Dax na poziomie max {}pkt.".format(opo[0]-20))
        pause()
    if srednie and not (wariant5 and kierunek==trend) and not (wariant4 and usa_kierunek==kierunek): 
        print("\n" * 5)
        print("Średnie przecięte, zaczekaj na lepszy moment")
        pause()
        pause()
    if kierunek==1 and blisko_ekstremow:
        print("DAX pomiędzy: ",(wsp[0]+20),"-",SL+odleglosc_do_SL) 
    elif kierunek==-1 and blisko_ekstremow:
        print("Dax pomiędzy: ", SL-odleglosc_do_SL,"-",(opo[0]-20))
    elif kierunek==1:
        print("DAX musi być poniżej: ",SL+odleglosc_do_SL)
    elif kierunek==-1:
        print("Dax musi być powyżej: ", SL-odleglosc_do_SL)
    if za_wczesnie:
        print("Zdecydowanie za wczesnie na kontre! Tylko kontynuacja lub negacja! ewentualnie mała kontra ale przy wyraźnych przesłankach")
        print_stopka()
    elif wariant5 and (usa_kierunek==kierunek or trend==kierunek):
        print("Żadnej kontynuacji")
        print("Tylko kontra! Również pomimo wsparć i oporów czy średnich. \nRSI może być liźnięte")
        print_stopka()
    elif wariant1:
        if ((kierunek==1 and trend==1 and sila) or (dzienny_trend==1 and kierunek==1 and not sila)) and check_zniesienia==0:
            print("Kontra long dozwolona, rynek trenduje-miej to na uwadze.")
            print_stopka()
        elif ((kierunek==-1 and trend==-1 and sila) or (dzienny_trend==-1 and kierunek==-1 and not sila)) and check_zniesienia==0:
            print("Kontra szort dozwolona, rynek trenduje-miej to na uwadze.")
            print_stopka()
        elif check_zniesienia==1:
            print("Zniosło większość ruchu więc nawet kontra w kierunku rynku jest z bardzo dużym ryzykiem!")
            kontry=False
            print_stopka()
        else:
            print("Rynek trenduje, żadnej kontry!")
            kontry=False
            print_stopka()
    elif pietnastka_rano:
        if kierunek==1 and trend==1 and check_zniesienia==0: 
            print("Kontra long dozwolona, zagrożenie dnia neutralnego.")
            print_stopka()
        elif kierunek==-1 and trend==-1  and check_zniesienia==0:
            print("Kontra szort dozwolona, zagrożenie dnia neutralnego.")
            print_stopka()
        elif check_zniesienia==1:
            print("Zniosło większość ruchu więc kontra jedynie na ekstremach")
            print_stopka()
        else:
            print("Kontra dozwolona pod warunkiem, że zgodna z ogólnym lub dziennym trendem. \nPoza tym masz na stole dzień neutralny i dzień trendu więc moze być mocno w każdą stronę. Uważaj!!!")
            print_stopka()
    elif wariant4 and (usa_kierunek==kierunek or trend==kierunek):
        print("Ok... \nPamiętaj o jakości świeczki (żadna szpulka czy doji")
        print_stopka()
    elif za_szybko:
        print("Za duże zmiany w czasie{} minut!".format(int(za_szybko_w_czasie*100)))
        print_stopka()
    else:
        print("Ok... \nPamiętaj o jakości RSI (nieliźnięte a wyraźne ekstremum) \ni świeczki (żadna szpulka czy doji)!")
        print_stopka()
        

def print_stopka():
    print("\n")
    if kontra and duza_kontra and kontry:
        print("Możesz kontrą-całą pozycją, jak również dużą kontrą jeżeli RSI30 na odpowiednim poziomie")
    elif kontra and kontry:
        print("Możesz kontrą, całą pozycją")
    elif duza_kontra and kontry:
        print("Możesz tylko dużą kontrą lub małą kontrą")
    elif mala_kontra and kontry:
        print("Tylko mała kontra!")
    if kontynuacja:
        print("Szukaj kontynuacji")
        if wariant4:
            print("Uważaj jednak na kontynuację bo zmienność śmieszna i ryzyko, że kontynuacja nie będzie dobrym pomysłem")
    if kontynuacja and sila and trend==1 and kierunek==-1:
        print("Kontynuacja long to jest coś na co powinineś patrzeć")
    elif kontynuacja and sila and trend==-1 and kierunek==1:
        print("Kontynuacja short to jest coś na co powinineś patrzeć")
    if not zyskownosc==None and not zyskownosc and (wariant5 or wariant4):
        print("Wcześniejszy sygnał był zły. Weryfikuj swoje postrzeganie co do dnia i naprawdę patrz na kontynuację chłopie!")
    if za_szybko:
        print("Zdecydowanie niezalecany trejd kontry ze względu na dużą zmienność w czasie{} minut!".format(int(za_szybko_w_czasie*100)))
        if usa_kierunek!=0 and kierunek!=usa_kierunek:
            print("Dodatkowo niezgodne z ruchem USA!")
        if trend!=0 and kierunek!=trend:
            print("Dodatkowo niezgodne z głównym trendem")
    if sila and kierunek==trend:
        print("Kontra w tym kierunku jak najbardziej. Wszak duża siła rynku i zgodne z trendem \nNie śpiesz się z braniem pieniądza!!!")
    elif sila and kierunek!=trend:
        print("Nie wchodź, zły pomysł! Granie przeciwko mocno trendującemu rynkowi")
    print("\n"*2)
    if srednie==1 and wariant5:
        print("Średnie przecięte ale niska zmienność i brak okoliczności świadczących o trendzie dlatego możesz pominąć ten fakt")
    elif srednie==1 and wariant4 and kierunek==usa_kierunek:
        print("Średnie przecięte ale niska zmienność i kierunek zgodny z USA dlatego możesz pominąć ten fakt")
    if blisko_ekstremow and wariant5:
        print("Bliskie ekstrema ale z racji niskiej zmienności i braku sygnałów świadczących o kierunku możesz pominąć ten fakt")
    elif wariant4 and blisko_ekstremow and usa_kierunek==kierunek:
        print("Blisko ekstremum ale kierunek zgodny z USA")  
    if usa:
        print("USA odjechały!")
    if usa and not (zamkniecie-low>maksymalne_odch or high-zamkniecie>maksymalne_odch or high-low>maksymalne_odch):
        print("Uważaj na wystrzał! Stany pojechały a na dax nie ma dużych zmian")
    if pietnastka:
        print("Trzy 15 tki w rzędzie!")
    if pietnastka_rano:
        print("Poranne trzy 15 tki w rzędzie! podejrzenie dnia neutralnego, dnia trendu lub wariantu dnia normalnego")
    if luka>0 or luka<0:
        print("Niezamknięta luka zamknięcia! Wielkość {} pkt!".format(luka))
    if zamkniecie-low>maksymalne_odch or high-zamkniecie>maksymalne_odch:
        print("Duża zmienność od wczorajszego zamknięcia! Powyżej {} pkt!".format(maksymalne_odch))
    if high-low>maksymalne_odch:
        print("Duża zmienność dzienna (między high i low)! Powyżej {} pkt!".format(maksymalne_odch))
    if not pytanie1 and check_zniesienia==0:
        print("Zniesienie zarejestrowanego kierunku wynosi: ",round(max(zniesienia),2))
    elif not pytanie1 and check_zniesienia==1:
        print("Zniesiono 60% wcześniejszego mocnego ruchu więc dzień trendu to nie jest, chyba ze w drugą stroną")
    pause()
    
   

   
def print_menu():
    wyczysc()
    print("1. Wsparcia")
    print("2. Opory")
    print("3. Dax update")
    print("4. Wyswietl wprowadzone dane")
    print("5. Wprowadź czas danych rynkowych")
    print("6. Wyświetl i zmień ustawienia")
    print("7. Import/eksport")
    print("8. Przełącz użytkownik/programista")
    print("9. Zamknij")
    print("0. Checklista")


def print_wsparcia_menu():
    wyczysc()
    print("1. Wprowadź wsparcia")
    print("2. Dodaj wsparcie")
    print("3. Zastąp najbliższe wsparcie")
    print("4. Wyświetl wsparcia")
    print("5. Usuń najbliższe wsparcie")
    

def add_wsparcia():
    zmienna = 1
    while zmienna != 0:
        wsp.append(int(input("Dodaj poziomy wsparć, wciśnij 0 żeby zakończyć")))
        zmienna = wsp[-1]
    del (wsp[-1])
    wsp.sort(reverse=True)



def print_opory_menu():
    wyczysc()
    print("1. Wprowadź opory")
    print("2. Dodaj opór")
    print("3. Zastąp najbliższy opór")
    print("4. Wyświetl opory")
    print("5. Usuń najbliższy opór")
    

def add_opory():
    zmienna = 1
    while zmienna != 0:
        opo.append(int(input("Dodaj poziomy oporów, wciśnij 0 żeby zakonczyc")))
        zmienna = opo[-1]
    del (opo[-1])
    opo.sort()


def print_feed_menu():
    wyczysc()
    print("1. Wprowadź H/L ręcznie")
    print("2. Wstrzymaj/wznów feed z Alfa Vintage (opóźniony o 15 minut)")
    print("3. Wstrzymaj/wznów feed z Investing")
    print("4. Wyświetl feed")
    

def investing_feed():
    global Haje
    global Lowy
    global haj_time
    global low_time
    global current
    global pkt_dax
    global time_dax
    url='https://www.investing.com/indices/germany-30-chart'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
    rt = requests.get(url, headers=headers)
    rt.encoding
    tekst=str(rt.text[53600:200000]) 
    znajdz_current=tekst.find('last" id="last_last" dir="ltr">')
    current=tekst[znajdz_current+31:znajdz_current+37]
    if len(current)>0:
        current=int(current.replace(",",""))
    else:
        current=0
    zegarek()
    if czas>9:
        pkt_dax.append(current-konwentor_feeda)
        time_dax.append(czas)
    else:
        pkt_dax.append(current-konwentor_feeda)
        time_dax.append(7.0)
    
def investing_cac():
    global cac
    url='https://www.investing.com/indices/france-40'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
    r = requests.get(url, headers=headers)
    r.encoding
    tekst_cac=str(r.text[53600:200000]) 
    znajdz_current_cac=tekst_cac.find('last" id="last_last" dir="ltr">')
    cac=tekst_cac[znajdz_current_cac+31:znajdz_current_cac+36]
    if len(cac)>0:
        cac=int(cac.replace(",",""))
    else:
        cac=0
    
    
        
def alfa_feed():
    global Haje
    global Lowy
    global haj_time
    global low_time
    data_feed = TimeSeries(key='W6TKOTM8IVYDUIQU').get_intraday(symbol="^GDAXI",interval='5min', outputsize='compact')
    dane=list((data_feed[-2]).values())[0]
    godzina_feeda=(list((data_feed[-2]).keys())[0].split(" "))[1].split(":")[0]
    minuta_feeda=(list((data_feed[-2]).keys())[0].split(" "))[1].split(":")[1]
    dzien_feeda=(list((data_feed[-2]).keys())[0].split(" "))[0].split("-")[2]
    godzina_feeda=int(godzina_feeda)
    minuta_feeda=int(minuta_feeda)
    dzien_feeda=int(dzien_feeda)
    czas_feeda=float(roznica_czasu+godzina_feeda+(minuta_feeda/100))
    close=dane["4. close"]
    low=dane["3. low"]
    low=float(low)
    low=int(low)
    high=dane["2. high"]
    high=float(high)
    high=int(high)
    if dzien==dzien_feeda and haj_time[-1]!=czas_feeda:
        Haje.append(high-konwentor_feeda)
        Lowy.append(low-konwentor_feeda)
        haj_time.append(float(czas_feeda))
        low_time.append(float(czas_feeda))
    elif dzien!=dzien_feeda and haj_time[-1]!=czas_feeda:
        Haje.append(high-konwentor_feeda)
        Lowy.append(low-konwentor_feeda)
        haj_time.append(float(7.00))
        low_time.append(float(7.00))
    else:
        pass
        
    

def manual_feed():
    global Haje
    global Lowy
    global haj_time
    global low_time
    global high
    global low
    global wsp
    global opo
    global luka
    print("Wprowadź low/high jako punkt odniesienia do zmienności")
    zmienna=int(input("Jaki low? Wciśnij 0 żeby nie zmieniać:"))
    if zmienna!=0:
        zmienna_time=float(input("O której godzinie? Format HH.MM"))
        Lowy.append(zmienna)
        low_time.append(round(float(zmienna_time),2))
    if (zmienna<low or low==0) and zmienna!=0:
        low=zmienna
        if len(wsp)>0:
            if wsp[0]!=low:
                wsp.append(low)
            zmienna=[]
            if len(wsp)>0:
                for i in range(len(wsp)): 
                    if wsp[i]<=low:
                        zmienna.append(wsp[i])
                wsp=zmienna
                wsp.sort(reverse=True)
    zmienna=int(input("Jaki high? Wciśnij 0 żeby nie zmieniać:"))
    if zmienna!=0:
        zmienna_time=float(input("O której godzinie? Format HH.MM"))
        Haje.append(zmienna)
        haj_time.append(round(float(zmienna_time),2))
    if zmienna>high and zmienna!=0:
        high=zmienna
        if len(opo)>0:
            if opo[0]!=high:
                opo.append(high)
            zmienna=[]
            if len(opo)>0:
                for i in range(len(opo)):
                    if opo[i]>=high:
                        zmienna.append(opo[i])
                opo=zmienna
                opo.sort()
    if high<zamkniecie: 
        luka=(high-zamkniecie)
    elif low>zamkniecie:
        luka=(low-zamkniecie)
    else:
        luka=0

def feed_check():
    global h_l_message
    global brak_feeda
    brak_feeda=False
    zegarek()
    if (len(haj_time)==0 or len(low_time)==0) and len(time_dax)==0:
        h_l_message="   Nie ma danych dla hajów i/lub lowów"
        max_time_high=0
        max_time_low=0
    elif not len(time_dax)==0:
        if len(haj_time)==0:
            max_time_high=max(time_dax)
        else:
            max_time_high=max(max(haj_time), max(time_dax))    
        if len(low_time)==0:
            max_time_low=max(time_dax)
        else:
            max_time_low=max(max(low_time), max(time_dax))
        h_l_message="   Update haja {}h".format(max_time_high)+" lowa {}h".format(max_time_low)
    else:
        max_time_high=max(haj_time)
        max_time_low=max(low_time)
        h_l_message="   Update haja {}h".format(max_time_high)+" lowa {}h".format(max_time_low)
    if czas-max_time_high>0.3 or czas-max_time_low>0.3:
        brak_feeda=True
        
            
def print_dane():
    dict_sorted=dict(sorted(dane.items()))
    print("\n" * 5)
    print("Wprowadzone dane:")
    print("\n" * 2)
    print("Poziom zamknięcia: ",zamkniecie)
    print("low-",low,"\t high-",high)
    if high!=0 and low!=0 and luka!=0:
        print("Luka: ",luka)
    if high!=0 and low!=0:
        print("Zmienność dzienna: ", high-low)
    if high!=0 and low!=0:
        print("Zmienność od zamknięcia: ", max(high-zamkniecie, zamkniecie-low))
    print("wsparcia:", wsp)
    print("Opory:", opo)
    if usa:
        print("Stany odjechały! Uwaga na trend na Dax!!!")
    else:
        print("Stany neutralne!")
    print("Trejdujesz do godziny: ",ogranicznie_czasu)
    if len(dict_sorted)==0:
        print("Nie wprowadziłeś żadnych godzin dla danych fundamentalnych")
    else:
        print("Dane o godzinie:")
        for key in dict_sorted:
            print(key, end="  ")
    pause()


def ustawienia():
    global minimalne_odch
    global maksymalne_odch
    global ogranicznie_czasu
    global blisko_danych
    global ekstrema
    global pietnastka_rano
    global odleglosc_do_SL
    global pytanie1
    global check_zniesienia
    global odswiezanie_feeda
    global kasowanie_feeda
    global ratio_min
    global ratio_max
    wyczysc()
    print("Zmiana ustawień")
    print("\n" * 2)
    print("Obecne ustawienia to:")
    print("\n" * 2)
    print("Tradowanie do godziny:", ogranicznie_czasu)
    print("Maksymalne odchylenie: ", maksymalne_odch)
    print("Minimalne odchylenie: ", minimalne_odch)
    print("Maksymalna odległość do SL: ",odleglosc_do_SL) 
    print("Ilość minut przed danymi dozwolone do tradowania:", int(blisko_danych*100))
    print("Bezpieczna odległość od wsparć/oporów: {} pkt".format(ekstrema))
    print("Feed odświeżany co {} (Format MM.SS).".format(odswiezanie_feeda))
    print("Kasowanie feeda po {} minutach".format(int(za_szybko_w_czasie*100)),kasowanie_feeda)
    print("Alarm na ratio między Dax a Cac: ", ratio_min,"-",ratio_max)
    if pietnastka_rano:
        print("Trzy 15tki rano były!")
    print("\n"*3)
    print("Wybierz 0 żeby nie zmieniać parametru")
    print("\n"*2)
    zmienna=float(input("Tradowanie do godziny: "))
    if zmienna!=0:
        ogranicznie_czasu=zmienna
    zmienna=int(input("Ile pkt zmienności maksymalnego odchylenia: "))
    if zmienna!=0:
        maksymalne_odch=zmienna
    minimalne_odch=maksymalne_odch/2
    zmienna=int(input("Ile pkt zmienności minimalnego odchylenia: "))
    if zmienna!=0:
        minimalne_odch=zmienna
    zmienna=int(input("Jaka maksymalna odległość od SL? "))
    if zmienna!=0 and zmienna<30:
        odleglosc_do_SL=zmienna
    zmienna=int(input("Ile minut do danych akceptowalne: "))
    if zmienna!=0:
        blisko_danych=zmienna/100
    zmienna=int(input("Ile punktów od ekstremów akceptowalne: "))
    if zmienna!=0:
        ekstrema=zmienna
    zmienna=float(input("Co ile czasu chcesz odświeżać feeda?. Format MM.SS!"))
    if zmienna!=0:
        odswiezanie_feeda=round(float(zmienna),2)
    zmienna=int(input("1 dla kasowania feeda jeśli czas dłuższy niż {} minuty. 2. żeby nie kasować".format(int(za_szybko_w_czasie*100))))
    if zmienna==1:
        kasowanie_feeda=True
    elif zmienna==2:
        kasowanie_feeda=False
    zmienna=int(input("Trzy piętnastki z rana? wybierz (1). dla nie wybierz(2)"))
    if zmienna==1:
        pietnastka_rano=True
    elif zmienna==2:
        pietnastka_rano=False
        pytanie1=True
        check_zniesienia=0
    zmienna=float(input("Jakie dolne widełki ratio Dax/Cac?: "))
    if zmienna!=0:
        ratio_min=zmienna
    zmienna=float(input("Jakie górne widełki ratio Dax/Cac?: "))
    if zmienna!=0:
        ratio_max=zmienna
        

def add_dane():
    x=1
    while x!= 0:
        godzina_danych=float(input("o której godzinie? Format HH.MM!"))
        priorytet=int(input(" jaki priorytet? 0 mało istotne, 1 ważne, 2 kluczowe dane!"))
        print (godzina_danych," priorytet", priorytet)
        dane.update({round(float(godzina_danych),2):priorytet})
        try:
            x=int(input("Wciśnij 0 żeby zakończyć wprowadzanie"))
        except ValueError:
            pass
        
        
def importuj():
    global wsp
    global opo
    wsp=[]
    opo=[]
    plik=open("darek.csv", "r").readlines(0)
    dane=str(plik[0]).split(";")
    wsparcia=dane[0].split("-")
    opory=dane[1].split("-")
    for i in range(len(wsparcia)-1):
        wsp.append(int(wsparcia[i]))
    for i in range(len(opory)-1):
        opo.append(int(opory[i]))


def eksportuj():
    global zapisz
    global wsp
    global opo
    zapisz=open("darek.csv", "w")
    now = datetime.datetime.now()
    czas_zapisu="Dzień "+str(now.day)+" Godzina: "+str(now.strftime("%H"))+":"+str(now.strftime("%M"))
    wsparcia=""
    opory=""
    for i in wsp:
        wsparcia=wsparcia+str(i)+"-"
    for i in opo:
        opory=opory+str(i)+"-"
    return wsparcia+";"+opory+";"+"Czas zapisu: "+czas_zapisu


def wyczysc():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(wersja+typ+alfa_feed_message+inv_feed_message+h_l_message)
        print("\n"*2)

def pause():
    print('\n\t', end='')
    input("Press ENTER...")
    wyczysc()

def main():
    global check_user
    global check_programisty
    global working
    global alfa_feed_pause
    global investing_feed_pause
    global alfa_feed_message
    global inv_feed_message
    while check_user:
        try:
            zegarek()
            feed_check()
            print_menu()
            choice = int(input("Jaki jest Twój wybór?"))
            if choice==1:
                wyczysc()
                print_wsparcia_menu()
                wsparcia_choice = int(input("Jaki jest Twój wybór?"))
                if wsparcia_choice==1:
                    add_wsparcia()
                    pause()
                elif wsparcia_choice==2:
                    print(wsp)
                    wsp.append(int(input("jakie jest wsparcie które chcesz dodać")))
                    wsp.sort(reverse=True)
                    print(wsp)
                    pause()
                elif wsparcia_choice == 3:
                    print(wsp)
                    wsp[0]=int(input("Jakie jest wsparcie na które chcesz zmienić"))
                    wsp.sort(reverse=True)
                    print(wsp)
                    pause()
                elif wsparcia_choice == 4:
                    print(wsp)
                    pause()
                elif wsparcia_choice==5:
                    print(wsp)
                    if int(input("Wciśnij 0 żeby usunąć"))==0:
                        del (wsp[0])
                        print(wsp)

            elif choice==2:
                wyczysc()
                print_opory_menu()
                opory_choice = int(input("Jaki jest Twój wybór?"))
                if opory_choice == 1:
                    add_opory()
                    pause()
                elif opory_choice == 2:
                    print(opo)
                    opo.append(int(input("jaki jest opór który chcesz dodać")))
                    opo.sort()
                    print(opo)
                    pause()
                elif opory_choice == 3:
                    print(opo)
                    opo[0] = int(input("Jaki jest opór na który chcesz zmienić"))
                    opo.sort()
                    print(opo)
                    pause()
                elif opory_choice == 4:
                    print(opo)
                    pause()
                elif opory_choice == 5:
                    print(opo)
                    if int(input("Wciśnij 0 żeby usunąć"))==0:
                        del (opo[0])
                        print(opo)
                        pause()

            elif choice==5:
                add_dane()

            elif choice==4:
                print_dane()

            elif choice==6:
                ustawienia()

            elif choice==7:
                wyczysc()
                print("Import/eksport danych")
                impeks=int(input("0. Pobierz dane \n1. Zapisz \n"))
                if impeks==0:
                    try:
                        plik=open("darek.csv", "r").readlines(0)
                        dane=str(plik[0]).split(";")
                        czas_zapisu=dane[2]
                        print(czas_zapisu)
                        if int(input("Jesteś pewny żeby ładować dane? Wciśnij 1 dla potwierdzenia \n"))==1:
                            importuj()
                            print("Dane zostały pobrane")
                            pause()
                    except:
                        ValueError
                        print("Problem z pobraniem danych. Brak bliku lub zły format danych")
                        pause()
                elif impeks==1:
                    print("\n"*2)
                    if int(input("Jesteś pewny żeby zapisać dane? Wciśnij 1 dla potwierdzenia \n"))==1:
                        try:
                            eksportuj()
                            zapisz.write(str(eksportuj()))
                            zapisz.close()
                            print("Dane zostały zapisane.")
                            pause()
                        except:
                            ValueError
                            print("Błąd, pewnie brak folderu archiwum w folderze D:/Trading")
                            pause()
                                       
            elif choice==3:
                wyczysc()
                print_feed_menu()
                update=int(input(""))
                if update==1:
                    manual_feed()
                elif update==2 and alfa_feed_pause:
                    alfa_feed_pause=False
                    alfa_feed_message=" Alfa feed"
                elif update==2 and not alfa_feed_pause:
                    alfa_feed_pause=True
                    alfa_feed_message=""
                elif update==3 and investing_feed_pause:
                    investing_feed_pause=False
                    inv_feed_message=" Investing feed"
                elif update==3 and not investing_feed_pause:
                    investing_feed_pause=True
                    inv_feed_message=""
                elif update==4:
                    wyczysc()
                    investing_feed()
                    investing_cac()
                    print("Haje",Haje[-17:])
                    print("Lowy",Lowy[-17:])
                    print("Haj time",haj_time[-17:])
                    print("Low time",low_time[-17:])
                    print("Dane z investing")
                    print("Obecny poziom daxa: ", current, "Cac", cac)
                    if current>0 and cac>0:
                        print("ratio dax/cac", ((current/cac)-2)*1000)
                    print("Inv:", pkt_dax[-17:])
                    print("Time:", time_dax[-17:])
                    print("Lista ratio:",ratio_list)
                    pause()
                    
            elif choice==9:
                wyczysc()
                if int(input("Pewnyś, że chcesz zamknąć? Wciśnij (8)!\n"))==8:
                    check_user=False
                    working=False
                    e.set() # to do zmuszenia śpiocha do obudzenia sie i przy working false zamknięcia backgroundu
            elif choice==8:
                check_user=False
                check_programisty=True
                
                
            elif choice==0:
                checklista()
        except ValueError:
            print("Podaj prawidłowy numer")
            pause()
            


def main_programisty():
    global check_user
    global check_programisty
    global working
    global alfa_feed_pause
    global investing_feed_pause
    global alf_feed_message
    global inv_feed_message
    while check_programisty:
        zegarek()
        feed_check()
        print_menu()
        choice = int(input("Jaki jest Twój wybór?"))
        if choice==1:
            wyczysc()
            print_wsparcia_menu()
            wsparcia_choice = int(input("Jaki jest Twój wybór?"))
            if wsparcia_choice==1:
                add_wsparcia()
                pause()
            elif wsparcia_choice==2:
                print(wsp)
                wsp.append(int(input("jakie jest wsparcie które chcesz dodać")))
                wsp.sort(reverse=True)
                print(wsp)
                pause()
            elif wsparcia_choice == 3:
                print(wsp)
                wsp[0]=int(input("Jakie jest wsparcie na które chcesz zmienić"))
                wsp.sort(reverse=True)
                print(wsp)
                pause()
            elif wsparcia_choice == 4:
                print(wsp)
                pause()
            elif wsparcia_choice==5:
                print(wsp)
                if int(input("Wciśnij 0 żeby usunąć"))==0:
                    del (wsp[0])
                    print(wsp)

        elif choice==2:
            wyczysc()
            print_opory_menu()
            opory_choice = int(input("Jaki jest Twój wybór?"))
            if opory_choice == 1:
                add_opory()
                pause()
            elif opory_choice == 2:
                print(opo)
                opo.append(int(input("jaki jest opór który chcesz dodać")))
                opo.sort()
                print(opo)
                pause()
            elif opory_choice == 3:
                print(opo)
                opo[0] = int(input("Jaki jest opór na który chcesz zmienić"))
                opo.sort()
                print(opo)
                pause()
            elif opory_choice == 4:
                print(opo)
                pause()
            elif opory_choice == 5:
                print(opo)
                if int(input("Wciśnij 0 żeby usunąć"))==0:
                    del (opo[0])
                    print(opo)
                    pause()
        elif choice==5:
            add_dane()

        elif choice==4:
            print_dane()

        elif choice==6:
            ustawienia()

        elif choice==7:
            wyczysc()
            print("Import/eksport danych")
            impeks=int(input("0. Pobierz dane \n1. Zapisz \n"))
            if impeks==0:
                plik=open("darek.csv", "r").readlines(0)
                dane=str(plik[0]).split(";")
                czas_zapisu=dane[2]
                print(czas_zapisu)
                if int(input("Jesteś pewny żeby ładować dane? Wciśnij 1 dla potwierdzenia \n"))==1:
                    importuj()
                    print("Dane zostały pobrane")
                    pause()
            elif impeks==1:
                print("\n"*2)
                if int(input("Jesteś pewny żeby zapisać dane? Wciśnij 1 dla potwierdzenia \n"))==1:
                    eksportuj()
                    zapisz.write(str(eksportuj()))
                    zapisz.close()
                    print("Dane zostały zapisane.")
                    pause()
                                       
        elif choice==3:
            wyczysc()
            print_feed_menu()
            update=int(input(""))
            if update==1:
                manual_feed()
            elif update==2 and alfa_feed_pause:
                alfa_feed_pause=False
                alfa_feed_message=" Alfa feed"
            elif update==2 and not alfa_feed_pause:
                alfa_feed_pause=True
                alfa_feed_message=""
            elif update==3 and investing_feed_pause:
                investing_feed_pause=False
                inv_feed_message=" Investing feed"
            elif update==3 and not investing_feed_pause:
                investing_feed_pause=True
                inv_feed_message=""
            elif update==4:
                wyczysc()
                investing_feed()
                investing_cac()
                print("Haje",Haje[-17:])
                print("Lowy",Lowy[-17:])
                print("Haj time",haj_time[-17:])
                print("Low time",low_time[-17:])
                print("Dane z investing")
                print("Obecny poziom daxa: ", current, "Cac", cac)
                if current>0 and cac>0:
                    print("ratio dax/cac", ((current/cac)-2)*1000)
                print("Inv:", pkt_dax[-17:])
                print("Time:", time_dax[-17:])
                print("Lista ratio:",ratio_list)
                pause()
            
        elif choice==9:
            wyczysc()
            if int(input("Pewnyś, że chcesz zamknąć? Wciśnij (8)!\n"))==8:
                check_programisty=False
                working=False
                e.set() # to do zmuszenia śpiocha do obudzenia sie i przy working false zamknięcia backgroundu
        elif choice==8:
            check_programisty=False
            check_user=True
            
        elif choice==0:
            checklista()

                      
    


def foreground():
    global typ
    while check_user or check_programisty:
        typ=" użytkownika"
        main()
        typ=" programisty"
        main_programisty()

      
def background(): 
    global alfa_feed_message
    global inv_feed_message
    global alfa_feed_pause
    global investing_feed_pause
    global current
    global spioch
    global ratio_list
    while working:
        feed_error=False
        if not alfa_feed_pause:
            try:
                alfa_feed()
            except:
                ValueError
                frequency = 400
                duration = 700 
                winsound.Beep(frequency, duration)
                feed_error=True
        if not investing_feed_pause:
            try:
                investing_feed()
                """investing_cac()
                if current>0 and cac>0:
                    ratio_list.append(round((((current/cac)-2)*1000),2))
                    if ratio_min<(((current/cac)-2)*1000)>ratio_max:
                        for i in range(5):
                            frequency = 1200
                            duration = 400 
                            winsound.Beep(frequency, duration)
                            e.wait(timeout=10)"""
            except:
                ValueError
                frequency = 400
                duration = 700 
                winsound.Beep(frequency, duration)
                feed_error=True
                current=0
        if (not alfa_feed_pause or not investing_feed_pause) and not feed_error and False:# wyłączam to żeby pikał jak 
            frequency = 700  
            duration = 300  
            winsound.Beep(frequency, duration)
        zegarek()
        if odswiezanie_feeda<1 and not feed_error:
            spioch=(odswiezanie_feeda*60*1.6666666667)-((minuty*60+sekundy)%((odswiezanie_feeda*60*1.6666666667)))
        elif not feed_error:
            spioch=(odswiezanie_feeda*60)-((minuty*60+sekundy)%((odswiezanie_feeda*60)))
        if alfa_feed_pause and investing_feed_pause:
            spioch=30
        elif czas<9:
            alfa_feed_pause=True
            investing_feed_pause=True
            spioch=30
            alfa_feed_message=""
            inv_feed_message=""
        elif feed_error:
            spioch=30
        e.wait(timeout=spioch)
        if czas>15 and not alfa_feed_pause:
            alfa_feed_pause=True
            alfa_feed_message=""
        
        
       
e=threading.Event() # to do przerwania śpiocha (e.set() zmusi do pójścia na początek pętli. tej pętli w backgroundzie)       
b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)
b.start()
f.start()



