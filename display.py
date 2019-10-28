import os

def print_album_info(album):
    artist_index = 0
    name_index = 1

    print('Album: {} by {}'.format(album[name_index], album[artist_index]))
    print(' | '.join(album[2:]))

def print_title(columns_wight, albums_data):
    options=["ARTIST","ALBUM", "YEAR", "GENRE", "DURATION"]
    print("_"*(sum(columns_wight)+len(albums_data[0])))
    for col_name in range(len(options)):
        print(options[col_name]+" "*(columns_wight[col_name]-len(options[col_name])), end="|")
    print("")



def print_albums_list(albums_data):
    options=["ARTIST","ALBUM", "YEAR", "GENRE", "DURATION"]
    columns_wight=[]
    for column in range(len(albums_data[0])):
        buff=len(options[column])
        for item in albums_data:
            if len(item[column])>int(buff):
                buff=len(item[column])
        columns_wight.append(buff)
    clear()
    print("List of aritists")
    print_title(columns_wight, albums_data)
    print("_"*(sum(columns_wight)+len(albums_data[0])))
    for line in albums_data:
        for column in range(len(albums_data[0])):
            print(line[column]+" "*(columns_wight[column]-len(line[column])), end="|")
        print("|")
        print("-"*(sum(columns_wight)+len(albums_data[0])))
    print("\n")
    
            
        
            
            # print("|" + row[item]) 
            # + " "*(columns_wight[item]-len(row[item])))

# ddałem atrybut text zeby wyswietlac dodatkowe infromacje dla uzytkownika w wybranym przez siebie
# miejscu.
def print_program_menu(menu_commands, text):
    clear()
    print("Menu:")
    for option in menu_commands:
        print(str(menu_commands.index(option)+1) + '----->' + option)
    print("\n"*2)
    print("Choose the number for options or press 0 for exit")
    print("\n"*2)
    print(text)

# tworze odzielna dla arrow nawigati funkcje wyswietlania menu bo tutaj bedzie bez cyfr i 
# musze chyba drukować bez petli. póki co narazie nie mam pomysłu jak zrobic w pętli by 
# uwzględnić zmieniające się printy w zależności od kliknięcia kursora.
# do zrobienia:
# muszę key_sens ustawic tak by sie zmieniło w zaleznosci od strzałki w górę lub dół a wtedy 
# key_sens bedzie podawało indeks. drugie z tym związane to printowanie menu ale tylko
# jeden elemnt o okreslonym przez key_sens indeksie printowane z dodatkami zmieniajacymi kolor
# odebranie strzałki w prawo jako wyboru a nastepnie zdefiniowanie menu z dwoma warunkami:
# key_sens jako numer i strzałka w prawo jako warunkek do zaistnienia okreslonej funkcji
def print_program_menu_arrow_nawigation(options, text, menu_index, printing_addons):
    clear()
    print("\n"*35)
    for option in range(len(options)):
        print(" "*35+printing_addons[option][0],options[option],printing_addons[option][1])
    print("\n"*5)
    print(" "*47,text)
    print("\n"*2)
    print(" "*5+"Press arrow keys (up and down) to nawigate and right arrow to choose the option")
    
    

    
def print_command_result(messege):
    vertical_spacing = 2
    clear()
    print(vertical_spacing * '\n' + "{}".format(messege))
    pause()

# def print_back():
#     print("\n"*5)
#     print("To get back to main menu press (m), to quit press (0)")

def print_error(error):
    print(error)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    print('\n\t', end='')
    input("Press ENTER...")
    clear()
