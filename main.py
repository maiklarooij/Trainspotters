# -----------------------------------------------------------
# main.py
#
# Used to run algorithms.
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from gooey import Gooey, GooeyParser

from src.algorithms.breadthfirst import BreadthFirst
from src.algorithms.genetic import GeneticAlgorithm
from src.algorithms.greedy import Greedy
from src.algorithms.hillclimber import Hillclimber
from src.algorithms.randomise import Random
from src.classes.graph import Graph
from src.visualisation.visualise import TrainMap

scale_choices = ["Holland", "Nationaal"]
algorithm_choices = ["random", "greedy", "bf", "hillclimber", "genetic"]
hillclimber_choices = ["true", "false"]
selection_choices = ["elitism", "rws", "tournament"]
breeding_choices = ["1point", "2point", "uniform"]


@Gooey(program_name="RailNL algorithm arguments GUI", navigation="Tabbed", tabbed_groups=True, use_cmd_args=True)
def main():

    # Command line arguments
    p = GooeyParser(description="A GUI to help you pick optional arguments for the algorithms")

    # All algorithms arguments
    p.add_argument("scale", help="Scale to run algorithms on", choices=scale_choices)
    p.add_argument("algorithm", help='Algorithm to run. Options = "random", "greedy", "bf", "hillclimber", "genetic".', choices=algorithm_choices)

    bfs_group = p.add_argument_group("BFS options")
    genetic_group = p.add_argument_group("Genetic Algorithm options")
    hillclimber_group = p.add_argument_group("Hillclimber Algorithm options")

    # Breadth-first algorithm optional argument
    bfs_group.add_argument("-bm", "--beam", help="Number of options to keep after each iteration", default=14, type=int)

    # Genetic algorithm optional arguments
    genetic_group.add_argument("-gs", "--genes_size", help="Number of random genes (=routes) to generate for GA", default=1000, type=int)
    genetic_group.add_argument("-ps", "--pop_size", help="Number of random combinations of genes (=routemaps) to generate for GA",
                               default=1000, type=int)
    genetic_group.add_argument("-mr", "--mutation_rate", help="Chance of mutations", default=0.2, type=float, widget="DecimalField")
    genetic_group.add_argument("-gn", "--generations", help="Number of generations", default=100, type=int)
    genetic_group.add_argument("-hc", "--hillclimber", help="Option to use hillclimber in genetic algorithm",
                               default="false", type=str, choices=hillclimber_choices)
    genetic_group.add_argument("-sl", "--selection", help="Choose a selection strategy.", default="elitism", type=str, choices=selection_choices)
    genetic_group.add_argument("-br", "--breeding", help="Choose a breeding strategy.", default="1point", type=str, choices=breeding_choices)

    # Hillclimber algorithm optional arguments
    hillclimber_group.add_argument("-re", "--restarts", help="Number of times the hillclimber algorithm does a restart",
                                   default=10, type=int)
    hillclimber_group.add_argument("-r", "--r", help="Number of random routes the hillclimber algorithm generates to try as replacement",
                                   default=100, type=int)

    hillclimber_option = {"true": True, "false": False}

    args = p.parse_args()

    # Scale = 'Nationaal' or 'Holland'
    # Algorithm = 'random', 'greedy', 'bf', 'genetic'
    scale = args.scale
    algorithm = args.algorithm

    # Make test graph based on scale
    test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv", scale)
    algorithms = {"random": Random(test_graph).run,
                  "greedy": Greedy(test_graph).run,
                  "bf": BreadthFirst(test_graph, args.beam).run,
                  "genetic": GeneticAlgorithm(
                    test_graph,
                    args.generations,
                    args.genes_size,
                    args.pop_size,
                    args.mutation_rate,
                    hillclimber_option[args.hillclimber],
                    args.selection,
                    args.breeding).run,
                  "hillclimber": Hillclimber(test_graph, args.restarts, args.r).run}

    print(f"Running {algorithm} algorithm... Please wait!")

    # Run algorithm
    solution = algorithms[algorithm]()

    # Generate results
    solution.generate_output(test_graph.total_connections, algorithm, scale)
    TrainMap(solution, test_graph, algorithm).export()

    print(f"All done! Check out the results in the results/{algorithm} folder!")


if __name__ == "__main__":
    main()
