# Trainspotters [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Vak: [Programmeertheorie 2022](theorie.mprog.nl) <br>
Gekozen case: [RailNL](https://theorie.mprog.nl/cases/railnl) <br>
Teamnaam: Trainspotters <br>
Studenten: Sam Bijhouwer, Maik Larooij

## Caseomschrijving

RailNL wil een nieuwe lijnvoering maken voor hun intercitytreinen. Binnen een bepaald tijdsframe moeten er een aantal trajecten worden uitgezet waarbij de kwaliteit van de lijnvoering zo hoog mogelijk is. Dat betekent het verbinden van zoveel mogelijk stations met zo min mogelijk trajecten en minuten. De case bestaat uit twee delen:

- Het maken van een lijnvoering voor de provincies Noord- en Zuid-Holland. De 22 belangrijkste stations moeten worden verbonden met maximaal 7 trajecten binnen een tijdsframe van 2 uur.
- Het maken van een lijnvoering voor heel Nederland. De 61 belangrijkste stations moeten worden verbonden met maximaal 20 trajecten binnen een tijdsframe van 3 uur.

Om de kwaliteit van de lijnvoering te testen is de volgende doelfunctie opgesteld:
```
K = p*10000 - (T*100 + Min)
```
Waarin K = de kwaliteit van de lijnvoering, p = de fractie van alle gereden verbindingen van het totaal aantal verbindingen, T = het aantal trajecten en Min = het aantal minuten van alle trajecten samen.

## Gebruik

### Vereisten
De code is geschreven in Python 3.9. De benodigde packages om de code te kunnen draaien staan in `requirements.txt`. Door middel van het volgende commando zijn deze te installeren via pip:
```
pip install -r requirements.txt
```
Of via conda:
```
conda install --file requirements.txt
```

### Commando

Het programma kan op de volgende manier een algoritme draaien:

```
python main.py --scale (or -s) --algorithm (or -a)
```

Bijvoorbeeld het random algoritme op Holland:

```
python main.py -s Holland -a random
```

Het genetisch algoritme heeft een aantal parameters die kunnen worden gekozen:

- `-gs`: Aantal random genes (routes) om te genereren
- `-ps`: Aantal random combinaties van routes om te genereren
- `-mr`: Mutatiekans
- `-gn`: Aantal generaties (aantal iteraties) van het algoritme
- `-hc`: Optie om Hillclimber te gebruiken als mutatieoptie
- `-sl`: Selectiemethode ('rws', 'elitism' of 'tournament')
- `-br`: Breeding-methode ('1point', '2point' of 'uniform')

```
python main.py -s Nationaal -a genetic -gs -ps -mr -gn -hc -sl -br
```

Voor hulp bij het draaien van het programma probeer:

```
python main.py -h
```

### Structuur

De mappen in deze repository:
- /code: bevat de code van dit project
    - /code/algorithms: bevat de algoritmes
    - /code/classes: bevat de benodigde classes
    - /code/visualisation: bevat code om visualisaties te maken
- /data: bevat de input data van dit project
- /doc: bevat belangrijke documenten, zoals pseudocodes en ondersteunende plaatjes
- /milestones: bevat milestones en twee notebooks met verkenning
- /results: bevat resultaten, zowel interactieve visualisaties als statische plots

## Auteurs

"Trainspotters" is een project voor de Universiteit van Amsterdam gemaakt door:

- Sam Bijhouwer
- Maik Larooij