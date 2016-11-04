from __future__ import print_function
from neptune import Player
import numpy as np
import random
from deap import base, creator, tools
from deap.algorithms import eaSimple

# Define constants
max_days = 7
population_size = 100
gene_length = 50
n_generations = 100

# Be careful before touching this
crossover_pb = 0.3
mutate_pb = 0.1


def setup_test_player():
    player = Player('Primdal')
    player.money = 475
    player.add_star(50, name="Fez", infrastructure=(5, 5, 1))
    player.add_star(35, name="Marfark")
    player.add_star(30, name="Wasat")
    player.add_star(25, name="Cursa")
    player.add_star(15, name="Eltanin")
    player.add_star(10, name="Aladfar")
    return player


def run_simulation(action_list, max_days=max_days):
    player = setup_test_player()
    day = 0
    for nth_action, action in enumerate(action_list):
        star_idx, price = player.get_cheapest_upgrades()[action]
        star = player.stars[star_idx]
        can_i_buy_it = star.buy_upgrade(action)
        if not can_i_buy_it:
            player.update_day()
            day += 1
            if day >= max_days:
                return player
            else:
                star.buy_upgrade(action)


def score(player):
    return player.ships,


def evaluate_actions(actions):
    player = run_simulation(actions)
    return score(player)


def get_pretty_action_list(action_list, max_days=max_days):
    translator = {0: "Econ", 1: "Industry", 2: "Science"}
    player = setup_test_player()
    day = 0
    actual_actions = []
    for nth_action, action in enumerate(action_list):
        star_idx, price = player.get_cheapest_upgrades()[action]
        star = player.stars[star_idx]
        can_i_buy_it = star.buy_upgrade(action)
        if not can_i_buy_it:
            actual_actions.append('NEW DAY')
            player.update_day()
            day += 1
            if day >= max_days:
                return actual_actions[:nth_action+day]
            else:
                star.buy_upgrade(action)
        actual_actions.append('Buying {} on {}'.format(translator[action],
                                                       star.name))

if __name__ == '__main__':

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("action", random.randint, 0, 2)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.action, n=gene_length)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=2, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("evaluate", evaluate_actions)

    initial_pop = toolbox.population(n=population_size)
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("mean", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    hof = tools.HallOfFame(5)
    pop = eaSimple(initial_pop, toolbox, cxpb=crossover_pb, mutpb=mutate_pb,
                   ngen=n_generations, verbose=True, stats=stats,
                   halloffame=hof)
    best_actions = hof[0]  # First element of Hall of Fame has best fitness
    player = run_simulation(best_actions)
    actions = get_pretty_action_list(best_actions)
    print('------------\nBest Actions:\n')
    print(actions)
