try:
    import socket
    from tkinter import *
    from tkinter import filedialog
    from deep_translator import GoogleTranslator
    import imdb
    import requests
    import crg
except ImportError:
    print("Nedostaju potrebni moduli. Pokreni skriptu 'Instalacija_paketa'")
    input()
    raise SystemExit(0)
except Exception:
    pass
    
def Provjera_Internetske_veze():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except Exception:
        print("Nema internetske veze!/No internet connection!")
        return False


internet = Provjera_Internetske_veze()
if(internet == False):
    input("\nPritisni enter za izlazak/Press enter to exit")
    raise SystemExit(0)
    

imdb_baza = imdb.IMDb()
pogreska = False #za pogreske koje mozda nastanu kod pretrazivanja

print("1 - Hrvatski | 2 - Engleski")
try:
    jezik = int(input('Odaberi jezik/Select language (1/2): '))
    if (jezik == 0 or jezik > 2):
        raise Exception
except Exception:
    jezik = 1

try:
    if (jezik == 1):
        ime_filma = input("\nUnesi ime filma: ")
        godina_filma = int(input("Unesi godinu: "))
        print()
    else:
        ime_filma = input("\nEnter movie name: ")
        godina_filma = int(input("Enter year: "))
        print()   
except Exception:
    pass
   
filmovi = imdb_baza.search_movie(ime_filma)
if (jezik == 1):
    print("Pretrazivanje...\n")
else:
    print("Searching...\n")

try:
    #film = imdb.Movie.Movie()
    pronasao = False
    for film in filmovi:
        if film['title'].lower() == ime_filma.lower() and film['year'] == godina_filma:
            pronasao = True
            film = imdb_baza.get_movie(film.movieID)
            break

    if (pronasao == False):
        try:
            film = imdb_baza.get_movie(filmovi[0].movieID)
        except Exception as e:
            print(e)
except Exception:
    pogreska = True
    if (jezik == 1):
        print("Nista nije pronadjeno!")
    else:
        print("Found nothing!")

#print(sorted(movie.keys())) --> lista sve kljuceve (info. tipove)
#print(movie.get('plot')[0])
try:
    naslov = film.get("title")
    godina = film.get("year")
    trajanje = film.get("runtimes")
    ocjena = film.get("rating")
    broj_glasova = film.get("votes")
    zanrovi = film.get("genres")
    direktor = film.get("director")
    glumci = film.get("cast")
    radnja = film.get("plot")[0]
except Exception:
    pogreska = True

try:    
    if 'cover url' in film:
        film_ima_poster = True
        poster_url = film['cover url']
        poster_url = poster_url[:poster_url.rindex('@')+1]
        #print(poster_url)
except Exception:
    pass

try:
    ime_direktora = [d['name'] for d in direktor]
    imena_glumaca = [glumac['name'] for glumac in glumci[:3]]
except Exception:
    pogreska = True

def list_to_string_w_commas(list):
    string = ""
    for item in list:
        if (list.index(item) == len(list)-1):
            string += item
        else:
            string += item + ", "
    return string
    
def human_format(num):
    try:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    except Exception:
        pass
    

try:
    #postavljanje stringova
    trajanje_min = trajanje[0]
    trajanje_min = int(trajanje_min)
    sati = trajanje_min // 60
    a = sati * 60
    minute = trajanje_min - a
    s_tranjanje = str(sati) + "h " + str(minute) + "min " + "(" + str(trajanje_min) + "min)" 

    s_ocjena = str(ocjena)

    s_broj_glasova = str(human_format(broj_glasova))


    s_direktor = ime_direktora[0]


    s_zanrovi = list_to_string_w_commas(zanrovi)
    s_glumci = list_to_string_w_commas(imena_glumaca)


    lradnja = radnja.split("::")
    s_radnja = lradnja[0]
        
    if(jezik == 1):
        #prevod
        s_radnja_prevedeno = GoogleTranslator(source='english', target='croatian').translate(s_radnja)

        hr_naslov = "Naslov: " + naslov
        #print("Naslov:", naslov)
        print(hr_naslov)
        hr_godina = "Godina: " + str(godina)
        #print("Godina:", godina)
        print(hr_godina)
        hr_trajanje = "Trajanje: " + s_tranjanje
        #print("Trajanje:", s_tranjanje)
        print(hr_trajanje)
        hr_IMDb_ocjena = "IMDb ocjena: " + s_ocjena + " (" + s_broj_glasova + " glasova)"
        #print("IMDb ocjena:", s_ocjena + " (" + s_broj_glasova + " votes)")
        print(hr_IMDb_ocjena)
        hr_zanr = "Zanr: " + s_zanrovi
        #print("Zanr:", s_zanrovi)
        print(hr_zanr)
        hr_direktor = "Direktor: " + s_direktor
        #print("Direktor:", s_direktor)
        print(hr_direktor)
        hr_glavne_uloge = "U glavnim ulogama: " + s_glumci
        #print("U glavnim ulogama:", s_glumci)
        print(hr_glavne_uloge)
        hr_radnja = "\nRadnja: " + s_radnja_prevedeno
        #print("\nRadnja: " + s_radnja_prevedeno)
        print(hr_radnja)
        #input()
    else:
        '''
        print("Title:", naslov)
        print("Year:", godina)
        print("Duration:", s_tranjanje)
        print("IMDb rating:", s_ocjena + " (" + s_broj_glasova + " votes)")
        print("Genre:", s_zanrovi)
        print("Director:", s_direktor)
        print("Cast:", s_glumci)
        print("\nPlot: " + s_radnja)
        '''
        en_naslov = "Title: " + naslov
        print(en_naslov)
        
        en_godina = "Year: " + str(godina)
        print(en_godina)
        
        en_trajanje = "Duration: " + s_tranjanje
        print(en_trajanje)
        
        en_IMDb_ocjena = "IMDb rating: " + s_ocjena + " (" + s_broj_glasova + " votes)"
        print(en_IMDb_ocjena)
        
        en_zanr = "Genre: " + s_zanrovi
        print(en_zanr)
        
        en_direktor = "Director: " + s_direktor
        print(en_direktor)
        
        en_glavne_uloge = "Cast: " + s_glumci
        print(en_glavne_uloge)
  
        en_radnja = "\nPlot: " + s_radnja
        print(en_radnja)
except Exception:
    pass

if (not pogreska):
    if(jezik == 1):
        spremanje = input("\nSpremiti info i naslovnu sliku filma? (da/ne): ")
        if (spremanje.lower() == 'ne' or spremanje.lower() == 'n'):
            if(jezik==1):
                input("Pritisni enter za izlazak iz programa")
            else:
                input("Press enter to exit")
            raise SystemExit(0)
    else:
        spremanje = input("\nSave movie info and cover? (yes/no): ")
        if (spremanje.lower() == 'no' or spremanje.lower() == 'n'):
            if(jezik==1):
                input("Pritisni enter za izlazak iz programa")
            else:
                input("Press enter to exit")
            raise SystemExit(0)
else:
    if(jezik==1):
        input("Pritisni enter za izlazak iz programa")
    else:
        input("Press enter to exit")
    raise SystemExit(0)

#spremanje tekst. datoteke in slike
if (jezik == 1):
    tekst_prozora = "Odaberi gdje spremiti info i naslovnu sliku filma"
else:
    tekst_prozora = "Select where to save movie info and cover"
    
prozor = Tk()  
prozor.withdraw() #da se ne otvori sivi tk prozor sa filedialogom 
putanja_spremanja = filedialog.askdirectory(title=tekst_prozora)

with open(putanja_spremanja+'/info.txt', 'w') as dat:
    if (jezik == 1):
        dat.write(hr_naslov+'\n')
        dat.write(hr_godina+'\n')
        dat.write(hr_trajanje+'\n')
        dat.write(hr_IMDb_ocjena+'\n')
        dat.write(hr_zanr+'\n')
        dat.write(hr_direktor+'\n')
        dat.write(hr_glavne_uloge+'\n')
        dat.write(hr_radnja)
    else:
        dat.write(en_naslov+'\n')
        dat.write(en_godina+'\n')
        dat.write(en_trajanje+'\n')
        dat.write(en_IMDb_ocjena+'\n')
        dat.write(en_zanr+'\n')
        dat.write(en_direktor+'\n')
        dat.write(en_glavne_uloge+'\n')
        dat.write(en_radnja)

#SLIKA
poster = requests.get(poster_url).content
with open(putanja_spremanja+'/folder.jpg', 'wb') as slika:
	slika.write(poster)
    
if (jezik == 1):
    print("Spremljeno")
else:
    print("Saved")
    
print()    
if(jezik==1):
    input("Pritisni enter za izlazak iz programa")
else:
    input("Press enter to exit")
    