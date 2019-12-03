import requests
from flask import Flask, render_template, request
import re
from datetime import datetime
#_________________Zmienne___________________________
app=Flask(__name__)
min_dlug_autora=2
min_dlug_tytulu=2
dlugosc_jez=2
dlugosc_isbn=[10,13]
blad=False
wynik = []
bledy=[]
nowa_ksiazka = {}
ksiazki_google = []
lista_bib=[]
dane=[]

# trzeba poprawic formatowanie bo wywala błedy przy haśle python np. moze wyszukiwanie tych indeksów w całym wybranym słowniku?
# pierwsza duża litera w nazwisku tytule przy dodawaniu do zbioru
#_________________________Funkcje__________________________

def import_biblioteki(url):
    global dane
    pobierz = requests.get(url)
    dane = pobierz.json()
    dane = dane["items"]


def formatowanie(lista, zbior): # to definiuje jaka lista ma byc tworzona i jaki zbior ma byc formatowany
    for i in range(len(zbior)):
        slownik = {}
        if 'title' in zbior[i]['volumeInfo']:
            slownik["Tytuł"]=zbior[i]['volumeInfo']['title']
        if "authors" in zbior[i]['volumeInfo']:
            zmienna=zbior[i]['volumeInfo']['authors']
            autrs=""
            for at in zmienna:
                autrs=autrs+at+" "
            slownik["Autorzy"]=autrs
        if 'publishedDate' in zbior[i]['volumeInfo']:
            slownik["DataPublikacji"] = zbior[i]['volumeInfo']['publishedDate'][:10]
        if 'identifier' in zbior[i]['volumeInfo']['industryIdentifiers']:
            slownik["ISBN"] = zbior[i]['volumeInfo']['industryIdentifiers'][0]['identifier']
        if 'pageCount' in zbior[i]['volumeInfo']:
            slownik["IloStron"] = str(zbior[i]['volumeInfo']['pageCount'])
        if 'thumbnail' in zbior[i]['volumeInfo']['imageLinks']:
            slownik["Okładka"] = zbior[i]['volumeInfo']['imageLinks']['thumbnail']
        if 'language' in zbior[i]['volumeInfo']:
            slownik["Język"] = zbior[i]['volumeInfo']['language']
        lista.append(slownik)




def dodaj():
    if not blad:
        global nowa_ksiazka
        nowa_ksiazka={}
        nowa_ksiazka["Tytuł"]=request.form.get("Tytuł")
        nowa_ksiazka["Autorzy"]=request.form.get("Autor")
        nowa_ksiazka["DataPublikacji"]=request.form.get("Data")
        nowa_ksiazka["ISBN"]=request.form.get("ISBN")
        nowa_ksiazka["IloStron"]=request.form.get("Stron")
        nowa_ksiazka["Okładka"]=request.form.get("LinkOkladki")
        nowa_ksiazka["Język"]=request.form.get("Język")
        lista_bib.append(nowa_ksiazka)
        return nowa_ksiazka

def walidator(autor, jezyk, isbn, dataod, datado,stron, okladka):
    global wynik
    global bledy
    global blad
    wynik = []
    bledy=[]
    blad=False
    male_znaki="abcdefghijklmnoqprstuwxyz"
    szczegolne_znaki='[@_!#$%^&*()<>?/\|}{~:]'

    if len(autor)!=0:
        zabronione_znaki = re.compile(szczegolne_znaki)
        if autor.isdigit() or not (zabronione_znaki.search(autor) == None):
            blad=True
            bledy.append("Nazwisko autora zawiera niedozwolone znaki")
    if len(jezyk)!=0:
        for i in jezyk:
            if not i in male_znaki or jezyk.isdigit():
                blad=True
                bledy.append("Błędnie wpisany język. Dwa znaki, tylko małe litery")
    if len(isbn)!=0:
        if  not len(str(isbn)) in dlugosc_isbn and not isinstance(isbn,int):
            blad=True
            bledy.append("Błędny nr ISBN. 10 lub 13 cyfr")
    if len(dataod)!=0 or len(datado)!=0:
        now = datetime.now()
        rok = now.strftime("%Y")
        miesiac = now.strftime("%M")
        dzien = now.strftime("%d")
        dzis = rok + "-" + miesiac + "-" + dzien
        if dataod>datado or dataod>dzis:
            blad=True
            bledy.append("Błędnie wybrane daty. Pierwsza musi być późniejsza, nie później niż {}".format(dzis))
    if len(stron)!=0:
        zmienna_strony=int(stron)
        if not isinstance(zmienna_strony,int):
            blad=True
            bledy.append("Liczba stron musi być liczbą całkowitą")
    if len(okladka)!=0:
        try:
            r = requests.head(okladka)
            if not (r.status_code == requests.codes.ok):
                blad=True
                bledy.append("Pod tym linkiem brak zdjęcia")
        except:
            blad = True
            bledy.append("Pod tym linkiem brak zdjęcia")



def szukaj(autor, tytul, jezyk, isbn, dataod, datado):
    if not blad:
        for i in range(len(lista_bib)):
            if len(autor)>0:
                zmienna=""
                for autorzy in lista_bib[i]["Autorzy"]:
                    zmienna+=autorzy
                print(zmienna, autor)
                if autor.upper() in zmienna.upper():
                    wynik.append(lista_bib[i])
            if len(tytul)>0:
                if tytul.upper() in lista_bib[i]["Tytuł"].upper():
                    wynik.append(lista_bib[i])
            if len(jezyk)>0:
                if jezyk.upper() in lista_bib[i]["Język"].upper():
                    wynik.append(lista_bib[i])
            if len(isbn)>0:
                if int(isbn)==int(lista_bib[i]["ISBN"]):
                    wynik.append(lista_bib[i])
            if len(datado)==0 and len(dataod)==0:
                pass
            elif len(datado)==0:
                datado="brak daty granicznej"
                if str(dataod)<lista_bib[i]["DataPublikacji"] and str(datado)>lista_bib[i]["DataPublikacji"]:
                    wynik.append(lista_bib[i])





#______________ Routes______________

@app.route("/")
@app.route("/home", methods=["POST", "GET"])
def home():
    import_biblioteki("https://www.googleapis.com/books/v1/volumes?q=Hobbit")
    formatowanie(lista_bib, dane)
    return render_template("home.html", lista_bib=lista_bib)

#________________Szukanie z głównej_____________
@app.route("/result", methods=["POST","GET"])
def wyszukaj():
    tytul=request.form.get("Tytuł")
    autor = request.form.get("Autor")
    jezyk=request.form.get("Język")
    isbn=request.form.get("ISBN")
    dataod=request.form.get("dataod")
    datado=request.form.get("datado")
    stron=""
    okladka=""
    walidator(autor, jezyk, isbn, dataod, datado, stron, okladka)
    szukaj(autor, tytul, jezyk, isbn, dataod, datado)
    return render_template("result.html", wynik=wynik, bledy=bledy)

#_______________Szukanie z google__________________

@app.route("/googlebiblioteka", methods=["GET"]) # prznosze sie na strone z polem wyszukiwania w google
def google_biblioteka():
    return render_template("googlebiblioteka.html")


@app.route("/googleresult", methods=["POST"]) # przesyłam inputa i zwracam google result
def szukaj_google():
    global ksiazki_google
    key = "AIzaSyB_E4cpGiAChUwbyjqyKxaLYSvFeK7qgQo"
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"key": key, "q": ""}
    params["q"]=request.form.get("googlesearch")
    response = requests.get(url, params=params)
    nowe_google = response.json()
    nowe_google = nowe_google["items"]
    ksiazki_google = []
    formatowanie(ksiazki_google, nowe_google) # dwa argumenty. do jakiej listy dodawac i jaki zbior
    return render_template("googleresult.html", ksiazki_google=ksiazki_google)

@app.route("/addedgoogle", methods=["POST"])
def dodanie_google():
    lista_bib.extend(ksiazki_google)
    return render_template("home.html", lista_bib=lista_bib)

#________________________ Dodawanie ręczne______________________

@app.route("/add", methods=["GET"]) # przenosze sie na pole dodowania recznego
def formularz_dodawania():
    return render_template("add.html")


@app.route("/addresult", methods=["POST"]) # odnosząc sie do nowej strony przekazuje zmienne do pythona i zwracam albo wynik albo wracam jesli błąd
def dodawanie():
    global bledy
    bledy=[]
    tytul=request.form.get("Tytuł")
    autor=request.form.get("Autor")
    dataod=request.form.get("Data")
    datado="brak"
    isbn=request.form.get("ISBN")
    stron=request.form.get("Stron")
    okladka=request.form.get("LinkOkladki")
    jezyk=request.form.get("Język")
    for i in lista_bib:
        if isbn==i["ISBN"]:
            bledy.append("Książka o takim numerze ISBN jest już w zbiorze")
            return render_template("add.html", bledy=bledy)
    walidator(autor, jezyk, isbn, dataod,datado,stron,okladka)

    if blad:
        return render_template("add.html", bledy=bledy)
    else:
        dodaj()
        return render_template("addresult.html", wynik=nowa_ksiazka)


if __name__=="__main__":
    app.run(debug=True)





