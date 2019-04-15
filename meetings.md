# Meetings notes

## Meeting 1.
* **DATE: 2019-02-13, 14:00**
* **ASSISTANTS: Mika Oja**
* **GRADE:** *To be filled by course staff*

### Minutes

General discussion about the current state of the project.
During the meeting we went through the requirements of the first deadline and checked that the project was advancing properly. One key-point was to clarify more the API-use in machine point of view (in automation, etc.). Although the subject was discussed in preliminary planning, the subject was not originally included in the documentation.

There was also discussion about the quality of resources used in this project: required scale and unimportance of business logic. The aim of the course is not business logic, but API and hypermedia implementation. The conclusion was that the project's current state is very good.

### Action points
The action points of the meeting were the following:
* Current state of the project
* Relevance of the RESTful technology/architecture
* Quality, scalability and size of the resources
* Importance of business logic
* How to mark code as your own
* The most important points of the project
* Django and Django REST Framework implementation
* API-use from machine point of view

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE: 2019-02-28, 14:30**
* **ASSISTANTS: Mika Oja**
* **GRADE:** *To be filled by course staff*

### Minutes
Intermediate model - ei tarvitse created, createid

Mikalta ehdotus:
User, movie, comment, review, neljä pääresurssia
Siivotaan osittain pois turhia resursseja, 
keskitytään siihen mikä on kiinnostavaa

Marshmallow jos haluaa automaattisempaa (?)
Hypermedia testit tulee testiosioon DL4
Nelosessa käsitellään kolmosen asioita, hypermediaa
Kolmosessa dokumentaatio on päätyö
Ohjaaja testasi django rest framework

Kritiikki / ”Nihkeys”: 
“Litteä” url hierarkia. miten restissä: movies/movieid/comment/commentid, nestataan urlit, urli hierarkia.

Hypermedia tyyppiä hiotaan, data/control epäselvä, ei eroa, ei speksattu hypermedia formaatti jos ei käytetä olemassa olevaa, suurin osa liittyy tälle puolelle 

Hypermedia linkit, katsotaan esimerkkejä, mason html, explisiittisesti selvitetty
 
Toinen kritiikki: kaikki metodit get, jos machine client etsiii controlleja, controlleissa pitäisi määrittää metodit, schema pitää määrittää jos post, schema määrittää mikä on validi, kaikki 3 deadline

API design on puheenaiheena, kolmannen harkan implementoinnista, ilman automaatiota, meidän osalta serialiseria pitää hienosäätää (paljon t. jaakko), Mikan mielestä “ei ongelma”.

Client:
Clientin suhteen, aika automatisoitu, melkein sama jos käyttäisi hypermedia clienttia, ei riitä autogeneroitu client, voi tehdä esim jonkin näköinen client, joka tekee jotain spesifimpää, kannattaisi tehdä erillinen, ei tarvitse käyttää kaikkea apista; 

Kolmannen deadlinen jälkeen mietitään clientiä, panosta kolmanteen deadlineen

Speksata oma hypermedia formaatti vai mitä, suosittelee masonia

Kakkos harkan asioita kannattaa käydä läpi
URL puu enemmän puuksi

Kakkosdeadline hyvä

Kolmonen dokumentaatiota, ei kiire implementoida


### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE: 2019-03-28, 15:30**
* **ASSISTANTS: Mika Oja**
* **GRADE:** *To be filled by course staff*

### Minutes
Patchia ei tartte jos ei ole pakko, patch on vähän huono metodi, voi tehdä, mutta ei paras
Enemmän työtä ja tietoa 

Patchille käyttöidea: movie detail, many to many suhde pariin asiaan, patch append ja poista, put komennolla ei mene nätisti, patchillä nätimpi. Linkit resursseja toinen tapa, massiivinen kartta jo valmiiksi toisaalta

MoviesIds, put, delete, suhde joko on olemassa tai ei. Hierarkia selvä ylös alas, horisontaaliset vaikeampia, mikä on mekaniikka, mikä category omistaa mitä, connection resurssit yksi vaihtoehto. Patch append lisää kategoria pop

Mihin riittää resurssit

Olisi hyvä kun on category niin pääsisi kategoriasta näkemään mitkä leffat on kategoriassa. Voi olla resurssi joka sisältää listan linkeistä leffoihin.

Kommentille voi nimetä uudeksi author, käytä standardeja kun mahdollista.

Suositus: Patchit kannattaa poistaa paitsi yhdet joilla kategorioita hallitaan.

Mainitaan wikitekstissä että mietitään patch uudestaan

Formaatti Hal + json

Kertoo clientille että kontekstissa ei ole mitään

Get actors, voisi sisältää suoraan listaan, count embedded

Hal:in isoin rajoite: ei tuo interaktiivisempia materiaaleja

Client harjoitus materiaalista selviää mikä on hyvä

Ei muuta, karsitaan turhia resursseja implementaatiota varten, 

Mieti hypermediaa


### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*


## Final meeting
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*
