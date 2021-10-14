naziv: GetFilmInfo
autor: Marko Zec
verzija: 0.9
datum: 26.7.2021
jezik: Python
paketi/moduli: deep_translator, imdb, requests

Opis programa:
Preuzimac informacija i naslovnih slika za filmove

Rad programa:
Program koristi IMDbPy modul koji preko IMDB api-a dohvaca podatke o filmovima. Prilikom pokretanja program uspostavlja internetsku vezu sa IMDB bazom i dohvaca informacije koje nakon toga (ovisno o korisnikovom odabiru) sprema u obliku tekstualne datoteke i naslovne slike u jpg formatu na lokaciju specificiranu od strane korisnika. U tekstualnoj datoteci info.txt nalaze se informacije o filmu poput naslova, godine, trajanja, ocjene, zanra, glumaca i radnje. Program podrzava 2 jezika: hrvatksi i engleski. Ukoliko korisnik odabere hrvatski jezik, koristi se deep-translate modul i nakon dohvacanja radnje filma, automatski se prevodi na hrvatski jezik prije pohrane na disk. Za dobivanje naslovne slike koristi se requests modul koji koristeci dobiveni cover-url dohvaca sadrzaj. Program hvata iznimke i u trenutacnoj verziji je relativno stabilan.   

Nedostaci:
Ponekad dolazi do rusenja programa jer se desi pogreska unutar imdbpy modula

Buduca verzija:
U verziji 1.0 planiram bolje organizirati pojedine segmente koda ("pocistiti kod"), te uvesti funkcionalnost automatskog skaliranja naslovne slike pomocu PIL i os modula kako bi sve spremljene naslovne slike imale istu velicinu i na taj nacin izbjegle situacije u kojima se na disk pohranjuju naslovne slike u 5k rezuluciji od po nekoliko megabajta.

Instalacija:
Za pokretanje programa na racunalu je potreban python3 kao i menadzer paketa pip. 
Prije prvog pokretanja potrebno je pokrenuti 'Instalacija_paketa.bat' skriptu koja ce instalirati programu potrebne pakete uz pomoc requirements.txt datoteke.