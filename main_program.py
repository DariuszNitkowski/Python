"""
The main program should use functions from music_reports and display modules
"""
import os
import file_handling 
import music_reports
import display
import msvcrt
ARTIST = 0
ALBUM = 1
YEAR = 2
GENRE = 3
DURATION = 4
arrow_up=[]
arrow_down=[]



def delete_album_by_artist_and_album_name(albums_data, artist, album_name):
    
    """
    Deletes album of given name by given artist from list and updates data file

    :param list albums: currently existing albums
    :param str artist: artist who recorded the album
    :param str album_name: name of album to be deleted

    :returns: updated albums' list
    :rtype: list
    """
    
    for album in albums_data:
        if artist==album[ARTIST] and album_name==album[ALBUM]:
            albums_data.remove(album)
    return albums_data



def main():
    # importuje plik i zapisuje w lokalnej dla tego modułu liście
    albums_data=file_handling.import_data("albums_data.txt")
    working=True
    check=True
    text=""
    # loopa zeby menu było wyświetlane non stop, nawet jesli ValueError to znaczy jesli input
    # nie bedzie int. text jest po to zeby wyswietlac okreslony komunikat w dowolnie wybranym miejscu
    # w przypadku dobrze wybranej opcji zamieniam text na pusty string zeby komunika nie byl wysiwetlany
    while working and check:
        try:
            display.print_program_menu(["Show table",
                                        "Delete album",
                                        "Display oldest album", 
                                        "Get albums by genre",
                                        "What is the oldest album by genre",
                                        "For arrow keys navigation"], text)  
            choice=int(input("What is your choice?:"))
            if choice==1: 
                display.print_albums_list(albums_data)
                display.pause()
                text=""
            elif choice==2:
                display.print_albums_list(albums_data)
                artist=input("What is name of artist you want to delete: ")
                album_name=input("What is name of album you want to delete: ")
                delete_album_by_artist_and_album_name(albums_data, artist, album_name)                
                text=""            
            elif choice==3:
                display.print_command_result(music_reports.get_last_oldest(albums_data))
                text=""
            elif choice==4:
                try:
                    genre=input("What is the genre?: ")
                    display.print_albums_list(music_reports.get_albums_by_genre(albums_data, genre))
                    display.pause()
                    text=""
                except (ValueError, IndexError, TypeError):
                    text="\033[41;33mNo such genre\33[m"
            elif choice==5:
                try:
                    genre=input("What is the genre?: ")
                    display.print_command_result(music_reports.get_last_oldest_of_genre(albums_data, genre))
                    text=""
                except (ValueError, IndexError, TypeError):
                    text="\033[41;33mNo such genre\33[m"
            elif choice==6:
                arow_nawigation_menu()
            elif choice==0:
                display.clear()
                working=False
        except ValueError:
            text="\033[41;33mGive proper number\33[m"
    
        


#for windows 'Matches:'+'\033[0;33m'+str(123)+'\033[0;0m'
        


# to printuje żółty tekst na czerwonym tle!!
# print("\033[41;33mHello World!\033[m")
# a to żóły na niebieskim
# print("\033[44;33mHello World!\033[m")
# a to piękny czarny na czerwonym
# print("\033[44;30mHello World!\033[m")
# to białe tło czarne literki
# print("\033[47;30mHello World!\033[m")
# zmienia się po nawiasie kwadratowym. 
# instrukcja:
# print("\033[ab;cdmHello World!\033[m")
# a musi byc 4 ka zeby bylo tlo. b okresla kolor tla. c musi byc 3 zeby byl kolor literki, d okresla
# kolor. kolory to 0 black 1 red 2 green 3 yellow 4 blue 5 magenta 6 cyan 7 white 9 default


# rozwiązanie do menu: moze nie najpiekniejsze ale stworzenie listy z tekstem przednim i tylnym
# ktory bedzie updatowany indeksem z key_sens a nastepnie printowany razem z lista options.
# umieszczam arrow up na samym poczatku przed lupa nawet zeby podswietlone menu zostało w tym samym
# miejscu po powrocie z wyników! poprawi to wygląd
def arow_nawigation_menu():
    albums_data=file_handling.import_data("albums_data.txt")
    working=True
    check=False
    text=""
    menu_index=0
    menu_lenght=7
    # while not check and working:"\33[46;37m","\33[m"
    while working and not check:
        arrow_choice=[]
        menu_index=((7000-len(arrow_up)+len(arrow_down))%menu_lenght)#7k gdyby ktos chcial naciska up arrow
        printing_addons=[["",""],["",""],["",""],["",""],["",""],["",""]]#lista z brakujacym elementem ktora bedzie dodrukowywana do menu
        printing_addons.insert(menu_index, ["==>>","<<=="])# brakujacy element o konkretnym indeksie ktory bedzie zmieniał kolor czcionki
        display.print_program_menu_arrow_nawigation(
                               ["             Show table              ",
                                "            Delete album             ",
                                "         Display oldest album        ", 
                                "          Get albums by genre        ",
                                "  What is the oldest album by genre  ",
                                "      For number keys navigation     ",
                                "                Exit                 "], text, menu_index, printing_addons)
        arrow_sensing(arrow_choice)
        if menu_index==0 and len(arrow_choice)>0:
            display.print_albums_list(albums_data)
            display.pause()
            text=""
        elif menu_index==1 and len(arrow_choice)>0:
            display.print_albums_list(albums_data)
            artist=input("What is name of artist you want to delete: ")
            album_name=input("What is name of album you want to delete: ")
            delete_album_by_artist_and_album_name(albums_data, artist, album_name)                
            text=""
        elif menu_index==2 and len(arrow_choice)>0:
            display.print_command_result(music_reports.get_last_oldest(albums_data))
            text=""
        elif menu_index==3 and len(arrow_choice)>0:
            try:
                genre=input("What is the genre?: ")
                display.print_albums_list(music_reports.get_albums_by_genre(albums_data, genre))
                display.pause()
                text=""
            except (ValueError, IndexError, TypeError):
                text="\033[41;33mNo such genre\33[m"
        elif menu_index==4 and len(arrow_choice)>0:
            try:
                genre=input("What is the genre?: ")
                display.print_command_result(music_reports.get_last_oldest_of_genre(albums_data, genre))
                text=""
            except (ValueError, IndexError, TypeError):
                text="\033[41;33mNo such genre\33[m"
        elif menu_index==5 and len(arrow_choice)>0:
            check=True
        elif menu_index==6 and len(arrow_choice)>0:
            display.clear()
            exit()
            

        

        
        


def arrow_sensing(arrow_choice):
    key = msvcrt.getch()
    if key==b"H":
        arrow_up.append(".")#to przy kazdym nacisnieciu strzalki w gore doda element do listy
    elif key==b"P":
        arrow_down.append(".")#gdy w dół doda element do drugiej listy. obliczy roznice i poda indeks
    elif key==b"M":
        arrow_choice.append(".")#jesli w prawo to wybor. dodatkowo indeks i mam wybór
    
""""
    Calls all interaction between user and program,
    Calls all interaction between user and program, handles program menu
    and user inputs. It should repeat displaying menu and asking for
    input until that moment.

    You should create new functions and call them from main whenever it can
    make the code cleaner"""
    


if __name__ == '__main__':
    main()
