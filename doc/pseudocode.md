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

