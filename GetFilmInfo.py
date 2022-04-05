try:
    import socket, time, os
    from tkinter import filedialog
    from deep_translator import GoogleTranslator
    import imdb
    import requests
except ImportError:
    print("Nedostaju potrebni moduli. Pokreni skriptu 'Instalacija_paketa.bat'")
    print("Missing dependency modules. Run 'Instalacija_paketa.bat' script"); input()
    raise SystemExit(0)

os.system("") #omogucuje koristenje ansii escape sekvenca (boje) u windowsima
ZUTA = '\033[93m'
CRVE = '\033[91m'
STOP = '\033[0m'

    
def Provjera_Internetske_veze():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except Exception:
        print("Nema internetske veze!/No internet connection!")
        return False


def lista_u_string(lista):
        string = ""
        for l in lista:
            if (lista.index(l) == len(lista)-1): string += l
            else: string += l + ", "
        return string


def formatiraj_broj(broj):
    broj = float('{:.3g}'.format(broj))
    magnituda = 0
    while abs(broj) >= 1000:
        magnituda += 1
        broj /= 1000.0
    return '{}{}'.format('{:f}'.format(broj).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnituda])


def izadi_nastavi(jezik):
    odluka = input('\nPonoviti izvodjenje? (da/ne): ' if (jezik==1) else '\nRepeat program? (yes/no): ')
    if (odluka.lower() in ('da', 'd', 'yes', 'y')): return 'nastavi'
    else: return 'izadi'

obrisiKonzolu = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")

def main():
    internet = Provjera_Internetske_veze()
    if(internet == False):
        input("\nPritisni enter za izlazak/Press enter to exit")
        raise SystemExit(0)
        
    imdb_baza = imdb.IMDb()
    pogreska = False #za pogreske koje mozda nastanu

    print("1 - Hrvatski | 2 - English")
    try:
        jezik = int(input('Odaberi jezik/Select language (1/2): '))
        if (jezik == 0 or jezik > 2): raise Exception
    except Exception:
        jezik = 1
        
    while (True): #GLAVNA PETLJA
        try:
            if (jezik == 1):
                ime_filma = input("\nUnesi naslov filma: ")
                godina_filma = int(input("Unesi godinu: "))
            else:
                ime_filma = input("\nEnter movie title: ")
                godina_filma = int(input("Enter year: "))  
        except ValueError:
            godina_filma = 0
        if len(ime_filma) == 0: continue
        
        filmovi = imdb_baza.search_movie(ime_filma)

        print("\nPretrazivanje...\n") if (jezik == 1) else print("\nSearching...\n")            

        try:
            # ---- trazenje
            pronasao = False
            for film in filmovi:
                if (film['title'].lower() == ime_filma.lower() and film['year'] == godina_filma):
                    pronasao = True
                    film = imdb_baza.get_movie(film.movieID)
                    break

            if (pronasao == False):
                i = 0
                while (True):
                    film = imdb_baza.get_movie(filmovi[i].movieID)
                    try:
                        if (film.get('localized title').lower() == ime_filma and film['year'] == godina_filma): break
                        if (film.get('original title').lower() == ime_filma and film['year'] == godina_filma): break
                    except: pass
                    print(('Jesi mislio: ' if (jezik==1) else 'Did you mean: ') + film['title']+' ('+str(film['year'])+')?')
                    odgovor = input('(da/ne): ' if (jezik==1) else '(yes/no): ')
                    if (odgovor.lower() in ('da', 'd', 'yes', 'y')): print(); break
                    else: i += 1
        except Exception:
            print("Nista nije pronadjeno!") if (jezik == 1) else print("Found nothing!")
            continue

        try:
            serija = False
            # ----- prikupljanje podataka
            naslov = film.get("title")
            try: originalni_naslov = film.get('original title')
            except: originalni_naslov = ''
            try: lokalizirani_naslov = film.get('localized title')
            except: lokalizirani_naslov = ''
            godina = film.get("year")
            trajanje = film.get("runtimes")
            ocjena = film.get("rating")
            broj_glasova = film.get("votes")
            zanrovi = film.get("genres")
            direktor = film.get("director")
            pisac = film.get("writer")
            glumci = film.get("cast")
            radnja = film.get("plot")[0]
            if 'cover url' in film:
                poster_url = film['cover url']
                poster_url = poster_url[:poster_url.rindex('@')+1]
            try: ime_direktora = [d['name'] for d in direktor]
            except: ime_direktora = [p['name'] for p in pisac]; serija = True
            imena_glumaca = [glumac['name'] for glumac in glumci[:3]]
     
            # ----- postavljanje stringova
            try:
                trajanje_min = trajanje[0]
                trajanje_min = int(trajanje_min)
                sati = trajanje_min // 60
                a = sati * 60
                minute = trajanje_min - a
                s_tranjanje = str(sati) + "h " + str(minute) + "min " + "(" + str(trajanje_min) + "min)" 
                s_ocjena = str(ocjena)
                s_broj_glasova = str(formatiraj_broj(broj_glasova))
                s_direktor = ime_direktora[0]
                s_zanrovi = lista_u_string(zanrovi)
                s_glumci = lista_u_string(imena_glumaca)
                lradnja = radnja.split("::")
                s_radnja = lradnja[0]
            except: pass

            # ----- prevod i printanje na konzolu
            if (serija): print('TV Serija\n' if (jezik==1) else 'TV Series\n')
            if(jezik == 1):
                s_radnja_prevedeno = GoogleTranslator(source='english', target='croatian').translate(s_radnja)
                try:
                    if (len(lokalizirani_naslov) != 0 and lokalizirani_naslov != naslov):
                        hr_naslov = "Naslov: " + lokalizirani_naslov + " (" + naslov + ")"; print(ZUTA + hr_naslov)
                    else: hr_naslov = "Naslov: " + naslov; print(ZUTA + hr_naslov)
                except: hr_naslov = "Naslov: " + naslov; print(ZUTA + hr_naslov)
                hr_godina = "Godina: " + str(godina); print(hr_godina)
                hr_trajanje = "Trajanje: " + s_tranjanje; print(hr_trajanje)
                hr_IMDb_ocjena = "IMDb ocjena: " + s_ocjena + " (" + s_broj_glasova + " glasova)"; print(hr_IMDb_ocjena)              
                hr_zanr = "Zanr: " + s_zanrovi; print(hr_zanr)
                hr_direktor = ('Pisac: ' if (serija) else 'Direktor: ') + s_direktor; print(hr_direktor) 
                hr_glavne_uloge = "U glavnim ulogama: " + s_glumci; print(hr_glavne_uloge)
                hr_radnja = "\nRadnja: " + s_radnja_prevedeno; print(hr_radnja + STOP)
            else:
                try:
                    if (originalni_naslov == naslov): en_naslov = "Title: " + naslov
                    elif (len(originalni_naslov) != 0): en_naslov = "Title: " + naslov + ' (' + originalni_naslov + ')' 
                except: en_naslov = "Title: " + naslov
                print(ZUTA + en_naslov)
                en_godina = "Year: " + str(godina); print(en_godina)
                en_trajanje = "Duration: " + s_tranjanje; print(en_trajanje)
                en_IMDb_ocjena = "IMDb rating: " + s_ocjena + " (" + s_broj_glasova + " votes)"; print(en_IMDb_ocjena)
                en_zanr = "Genre: " + s_zanrovi; print(en_zanr)
                en_direktor = ('Creator: ' if (serija) else 'Director: ') + s_direktor; print(en_direktor)
                en_glavne_uloge = "Cast: " + s_glumci; print(en_glavne_uloge)
                en_radnja = "\nPlot: " + s_radnja; print(en_radnja + STOP)
        except Exception:
            print(CRVE + '\nDesila se pogreska!\n' + STOP if (jezik == 1) else CRVE + '\nAn error occured!\n' + STOP)
            pogreska = True

        spremi = False
        if (not pogreska):
            if(jezik == 1):
                spremanje = input("\nSpremiti informacije i naslovnu sliku filma? (da/ne): ")
                if (spremanje.lower() == 'da' or spremanje.lower() == 'd'): spremi = True
                else:
                    akcija = izadi_nastavi(jezik)
                    if (akcija=='izadi'): break
                    else: obrisiKonzolu(); continue
            else:
                spremanje = input("\nSave movie info and cover art? (yes/no): ")
                if (spremanje.lower() == 'yes' or spremanje.lower() == 'y'): spremi = True
                else:
                    akcija = izadi_nastavi(jezik)
                    if (akcija=='izadi'): break
                    else: obrisiKonzolu(); continue
        else:
            akcija = izadi_nastavi(jezik)
            if (akcija=='izadi'): break
            else: obrisiKonzolu(); continue

        # ----- spremanje tekst. datoteke i slike
        if (spremi):
            tekst_prozora = "Odaberi gdje spremiti" if (jezik == 1) else "Select where to save"
                
            putanja_spremanja = filedialog.askdirectory(title=tekst_prozora)
            if (len(putanja_spremanja) != 0):
                with open(putanja_spremanja+'/info.txt', 'w', encoding='utf-8') as dat:
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

                #slika
                try:
                    poster = requests.get(poster_url).content
                    with open(putanja_spremanja+'/folder.jpg', 'wb') as slika:
                        slika.write(poster)
                except:
                    if (jezik == 1): print(CRVE + '\nPogreska: Slika se ne moze dohvatiti' + STOP)
                    else: print(CRVE + '\nError: No image available' + STOP)

                print("\nSpremljeno") if (jezik == 1) else print("\nSaved")
                akcija = izadi_nastavi(jezik)
                if (akcija=='izadi'): break
                else: obrisiKonzolu(); continue
            else:
                akcija = izadi_nastavi(jezik)
                if (akcija=='izadi'): break
                else: obrisiKonzolu(); continue


if __name__=='__main__':
    main()
    print('\nIzlazim.../Exiting...')
    time.sleep(1)
