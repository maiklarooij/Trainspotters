# Experiment

Deze folder bevat een script voor het draaien van een experiment. Het bevat de volgende experimenten:

## Random experiment

Dit experiment draait een x (standaard 100.000) aantal keren het random algoritme en schrijft de uitkomst van elke run naar een csv bestand in de folder `results/random/experiment`.

## Breadth-first experiment

Dit experiment draait voor verschillende beam waarden (tussen 2 en 100) het breadth-first algoritme en schrijft de uitkomst van elke run naar een csv bestand in de folder `results/bf/experiment`.

## Hillclimber experiment

Dit experiment draait voor verschillende configuraties het hillclimber algoritme: `restarts = [1, 5, 10, 20]` en `r_values = [100, 500, 1000]`. De uitkomst wordt geschreven naar een csv bestand in de folder `results/hillclimber/experiment`.

## Genetic experiment

Dit experiment draait voor verschillende configuraties (324 in totaal) het genetisch algoritme:

- `breedings = ["1point", "2point"]`
- `selections = ["elitism", "tournament", "rws"]`
- `generations = [50, 100, 200]`
- `mutate_rates = range(0, 12, 2)`
- `genes_and_pop_size = [100, 500, 1000]`

De uitkomst van elke run wordt geschreven naar een csv bestand in de folder `results/genetic/experiment`.