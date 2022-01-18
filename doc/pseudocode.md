# Pseudocode algorithms

## Random algorithm

```
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
