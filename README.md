# Trainspotters
Vak: [Programmeertheorie 2022](theorie.mprog.nl) <br>
Gekozen case: [RailNL](https://theorie.mprog.nl/cases/railnl) <br>
Teamnaam: Trainspotters <br>
Studenten: Mijntje Meijer, Sam Bijhouwer, Maik Larooij

## Caseomschrijving

RailNL wil een nieuwe lijnvoering maken voor hun intercitytreinen. Binnen een bepaald tijdsframe moeten er een aantal trajecten worden uitgezet waarbij de kwaliteit van de lijnvoering zo hoog mogelijk is. Dat betekent het verbinden van zoveel mogelijk stations met zo min mogelijk trajecten en minuten. De case bestaat uit twee delen:

- Het maken van een lijnvoering voor de provincies Noord- en Zuid-Holland. De 22 belangrijkste stations moeten worden verbonden met maximaal 7 trajecten binnen een tijdsframe van 2 uur.
- Het maken van een lijnvoering voor heel Nederland. De 61 belangrijkste stations moeten worden verbonden met maximaal 20 trajecten binnen een tijdsframe van 3 uur.

Om de kwaliteit van de lijnvoering te testen is de volgende doelfunctie opgesteld:
```
K = p*10000 - (T*100 + Min)
```
Waarin K = de kwaliteit van de lijnvoering, p = de fractie van alle gereden verbindingen van het totaal aantal verbindingen, T = het aantal trajecten en Min = het aantal minuten van alle trajecten samen.

## Aan de slag

### Vereisten
De code is geschreven in Python 3.9. De benodigde packages om de code te kunnen draaien staan in `requirements.txt`. Door middel van het volgende commando zijn deze te installeren via pip:
```
pip install -r requirements.txt
```
Of via conda:
```
conda install --file requirements.txt
```

### Gebruik

Het programma kan op de volgende manier een algoritme draaien:

```
python main.py --scale --algorithm
```

Bijvoorbeeld het random algoritme op Holland:

```
python main.py --scale Holland --algorithm random
```

Met het volgende commando kunnen de opties worden bekeken:

```
python main.py -h
```