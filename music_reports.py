import display
ARTIST = 0
ALBUM = 1
YEAR = 2
GENRE = 3
DURATION = 4

def get_albums_by_genre(albums_data, genre):
    """
    Get albums by genre

    :param list albums: albums' data
    :param str genre: genre to filter by


    :returns: all albums of given genre
    :rtype: list
    """
    # przekształciłem funkcje i jest bardzo podobna do późniejszej. 
    genre_list=[]
    for album in albums_data:
        if genre==album[GENRE]:
            genre_list.append(album)
    return genre_list
    
        


def get_genre_stats(albums_data):
    """
    Get albums' statistics showing how many albums are in each genre
    Example: { 'pop': 2, 'hard rock': 3, 'folk': 20, 'rock': 42 }

    :param list albums: albums' data
    :returns: genre stats
    :rtype: dict
    """
    # zmieniłem funckje całkowicie. funkcja towrzy liste do której dodaje wszystkie genre,
    # a nastepnie z listy tworze słownik z wartosciami które są liczone dla ilości kluczy.
    genre_list=[]
    for album in albums_data:
        genre_list.append(album[GENRE])
    dictionary_genre={key: genre_list.count(key) for key in genre_list}
    return dictionary_genre
    # for album in albums_data:
    #     if not album[GENRE] in result:
    #         result[album[GENRE]] = 1
    #     else:
    #         result[album[GENRE]] += 1
    # return result


def get_last_oldest(albums_data):
    """
    Get last album with earliest release year.
    If there is more than one album with earliest release year return the last
    one of them (by original list's order)

    :param list albums: albums' data
    :returns: last oldest album
    :rtype: list
    """
    # bierze pierwsza podliste z listy i porównuje indeks roku dla niej i kazdej nastepnej.
    # jesli nastepna wartosc jest nizsza jest mniejsza to ta zastepuje rezultat ktory jest porownywany
    # do pozostałych elementów. 
    result = albums_data[ARTIST]
    for album in albums_data:
        if int(album[YEAR]) <= int(result[YEAR]):
            result = album
    return result



def get_last_oldest_of_genre(albums_data, genre):
    """
    Get last album with earliest release year in given genre

    :param list albums: albums' data
    :param str genre: genre to filter albums by
    :returns: last oldest album in genre
    :rtype: list
    """
    # najpierw tworzy liste wierszy w których indeks jest równy inputowi genre. nastepnie
    # przeszukuje ta liste po indeksie rok i wyszukuje najstarszą(tak jak w przypadku funkcji wyżej)
    # przy złym genre nie drukuje pierwszej z listy tylko dzieki try, except wyświetla info
    genre_list=[]
    for album in albums_data:
        if genre==album[GENRE]:
            genre_list.append(album)
    result=genre_list[0]
    for album in genre_list:
        if int(album[YEAR]) <= int(result[YEAR]):
            result = album
    return result
    


def get_longest_album(albums_data):
    """
    Get album with biggest value in length field

    :param list albums: albums' data
    :returns: longest album
    :rtype: list
    """
    # result = albums[0]
    # for album in albums:
    #     if to_time(album[DURATION]) > to_time(result[DURATION]):
    #         result = album
    # return result
    # zakomentowałem całą funckje proponowana dlatego ze to time u mnie zwraca całą tabele. 
    # wolę zasotosować część funkcji: stworzyć listę z czasami przekonwertowanymi na sekundy,
    #  wydobyć indeks czasu najdłuższego, a następnie zwrócić album o tym indeksie
    durations=[]
    SEC_IN_MIN=60
    for album in albums_data:
        min_sec=[]
        min_sec=album[DURATION].split(":")
        durations.append(int(min_sec[0])*SEC_IN_MIN + int(min_sec[1]))
    return albums_data[durations.index(max(durations))]


def to_time(albums_data):
    """
    converts time in format "minutes:seconds" (string) to seconds (int)
    """
    # przez pentle zaminiea indeks duration prostym rownaniem. Zamienia intigery po sumie na str
    # zeby przy drukowaniu tabeli fukcja print table mogla obliczyc szerokosc kolumny. Dla inta 
    # len nie działa!
    SEC_IN_MIN=60
    for album in albums_data:
        min_sec=[]
        min_sec=album[DURATION].split(":")
        album[DURATION]=str(int(min_sec[0])*SEC_IN_MIN + int(min_sec[1]))
    return albums_data



def get_total_albums_length(albums_data):
    """
    Get sum of lengths of all albums in minutes, rounded to 2 decimal places
    Example: 3:51 + 5:20 = 9.18

    :param list albums: albums' data
    :returns: total albums' length in minutes
    :rtype: float
    """
    # durations = map(lambda album: to_time(album[DURATION]), albums_data)
    # total = sum(durations)
    # return int(total / 60) + ((total % 60)/ 60)
    # stosuje sporą część funkcji get_longest_album, sumuje i przeliczam na minuty. używam modulo do 
    # obliczenia resztek
    durations=[]
    SEC_IN_MIN=60
    for album in albums_data:
        min_sec=[]
        min_sec=album[DURATION].split(":")
        durations.append(int(min_sec[0])*SEC_IN_MIN + int(min_sec[1]))
    dur_sum_in_minutes=sum(durations)/SEC_IN_MIN
    return round(float((dur_sum_in_minutes//SEC_IN_MIN)+((dur_sum_in_minutes%SEC_IN_MIN)/60)), 2)
