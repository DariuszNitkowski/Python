import tkinter as tk
from tkinter import font
import requests

"""    if weather["wind"]["speed"]*1.94>
        if weather["wind"]["deg"]<135:
            wiatr="Tylko Hel ze wzgledu na kierunek"
        elif 135<=weather["wind"]["deg"]<=225:
            wiatr="Może być Hel ale może być Suchy róg bo wieje od południa!"
        elif 225<=<270:
            wiatr="Może być Hel ale może też być Okartowo"""

def get_weather(city):
    key="fdacbbeafbb50b3784ff0f37592e4b34"
    url="http://api.openweathermap.org/data/2.5/weather"
    params={"APPID":key, "q":city, "units":"metric"}
    response=requests.get(url, params=params)
    weather=response.json()
    lable["text"]=weather_response(weather)


def weather_response(weather):
    try:
        place=weather["name"]
        wind_speed=round(weather["wind"]["speed"] * 1.94, 0)
        wind_direction=weather["wind"]["deg"]
        temprature=weather["main"]["temp"]
        return "Miejsce: %s \nPrędkość wiatru: %s \nKierunek: %s \nTemperatura: %s"%(place,wind_speed, wind_direction,temprature)
    except:
        return "Nie moge znaleźć pogody"
window=tk.Tk()

canvas=tk.Canvas(window, width=500, height=400, bg="#ffb3ff")
canvas.pack()
background_image=tk.PhotoImage(file="pogoda.png")
background_lable=tk.Label(window, image=background_image)
background_lable.place(relwidth=1, relheight=1)


frame=tk.Frame(window)
frame.place(relx=0.05, rely=0.05,relwidth=0.9, relheight=0.1)
enter=tk.Entry(frame, bd=5, fg="blue", font=("Courier", 12))
enter.place(relx=0, rely=0, relwidth=0.7, relheight=1)
button=tk.Button(frame, command=lambda : get_weather(enter.get()), text="Podaj pogodę") # ttuaj w nazwie funkcji bez nawiasów bo jesli z nawiasami to od razu wykona!
#tak samo żeby wykorzystać wynik z pola zapisu enter musze zastosować nazwe klawisza.get a to zapisać w funkcji lambda, bo zapisanie tego w funkcji z nawiasami od razu
# wyswietli zawartosć
button.place(relx=0.7, relwidth=0.3, relheight=1)


frame_tekst=tk.Frame(window, bd=5, bg="blue")
frame_tekst.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.75, )
lable=tk.Label(frame_tekst, font=("@MS UI Gothic", 17), anchor="nw", justify="left", bd=4)
lable.place(relwidth=1, relheight=1)

window.mainloop()