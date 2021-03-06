# Pseudocode algorithms

## Random algorithm

```
def random_solution(graph):
    initialize routemap
    pick random number of routes N

    for each N do
        initialize route
        initialize candidates with distance 0

        while candidates
            add random station to route
            candidates = []

            for each neighbor of picked station do
                if neigbor not visited and does not exceed total time
                    add neighbor, distance to neighbor to candidates

        add route to routemap
```

## Greedy algorithm

```
def greedy_solution(graph):
    initialize routemap

    while not all stations visited and not max routes reached
        get station with most connections as start station

        while candidates (for route)
            search candidate with highest increase in score
            add candidate to route
        
        add route to routemap
```    

## Breadth-first search algorithm

```
def breadth_first(graph):
    initialize routemap

    while improvements and not max routes reached

        for every station, initialize route with start station

        while options
            for every option (route)
                get new candidates for route
                for every candidate, measure increase

            options = top x candidates
        
        add most increasing route to routemap
```

## Genetic algorithm

```
def genetic(graph):
    create n random routes
    population = create m random combinations of routes

    for every generation:

        select(population) (standard the best half of population)
        crossover(population)
        mutate(population)
        calculate fitness score for every chromosome in population

    create routemap from best chromosome in population
```

## Hillclimbing algorithm

```
def hillclimbing(graph, start_state, restarts):
    create random solution or generate from start_state

    for every restart:
        for every route in solution:

            generate 1000 random routes
            calculate new score for each random route
            replace route with highest score

```