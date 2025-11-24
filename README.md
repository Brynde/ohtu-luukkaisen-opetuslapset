# ohtu-luukkaisen-opetuslapset

https://docs.google.com/spreadsheets/d/1-FlkctWyJTgW-eF1vH_Z0ssMxPyceTmeGw08CQMjLpU/edit?usp=sharing 

## Asennusohjeet:

Vaatimukset:

  - Python
  
  - Poetry

Lataa ohjelma git clone komennolla

```
git clone git@github.com:Brynde/ohtu-luukkaisen-opetuslapset.git
```

Navigoi hakemistoon johon latasit ohjelman

Luo virtuaaliympäristö ja asenna poetry riippuvuudet

```
eval $(poetry env activate)

poetry install
```

Luo sovelluksen tietokanta

```
python3 src/db_helper.py
```

Käynnistä sovellus
```
python3 src/index.py
```
## Definiton of done:

 - Ominaisuus toiminnallisuudet toimivat halutulla tavalla
 - Koodi on vertaisarvioitu dailyssä
 - Kaikki testit on suoritettu hyväksytysti
 - Dokumentaatio on ajantasalla
 - Ryhmä on hyväksynyt ominaisuuden
 - Ominaisuus on valmis tuotantoon