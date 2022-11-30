import random as rd
import statistics as stats
import numpy as np


def main_compute(mode, data, team_size):
    message = []
    if mode == 0:
        team_list = standard_compute(data, team_size)
        message.append("Standard Team Assignment")
    if mode == 1:
        team_list = random_compute(data, team_size)
        message.append("Random Team Assignment")
        print(team_list)
    if mode == 2:
        team_list = mil_compute(data, team_size)
        message.append("Best of 1 Million Random Team Assignments")

    player_names = [*data.keys()]
    global_elo = []
    # noinspection PyUnboundLocalVariable
    for team in team_list:
        message.append("\n")
        message.append("Team " + str(team_list.index(team) + 1) + ":")
        team_elo = []
        for player in team:
            message.append("↳ " + str(player_names[player]))
            team_elo.append(data[player_names[player]])
        current_team_elo = sum(team_elo) / len(team_elo)
        message.append("= Average Team Elo: " + str(current_team_elo))
        global_elo.append(current_team_elo)
    message.append("\n")
    message.append("=> Group Elo: " + str(sum(global_elo) / len(global_elo)))
    message.append("=> Group StDev: " + str(stats.stdev(global_elo)))
    return '\n'.join(message)


def standard_compute(data, team_size):
    return [[]]


def random_compute(data, team_size):
    index = [*range(len(data))]
    rd.shuffle(index)
    casted = cast_teams(index, team_size)
    return casted


def cast_teams(index, team_size):
    return [index[i:i + team_size] for i in range(0, len(index), team_size)]


def mil_compute(data, team_size):
    length = len(data)
    repetition = 1000000

    stuff = np.tile(np.arange(length), (repetition, 1))
    rng = np.random.default_rng()
    temp = rng.permuted(stuff, axis=1, out=stuff)

    output = np.reshape(temp, (repetition, int(length / team_size), team_size))
    np.ascontiguousarray(output, dtype=np.ubyte)
    redone = np.sort(output, kind='heapsort')
    order = redone[:, :, 0].argsort()
    rearranged = np.take_along_axis(redone, order[:, :, None], axis=1)

    unique = np.unique(rearranged, axis=0)

    remapper = replace_dict_keys_with_incremental_value(data)

    remapped = np.vectorize(remapper.__getitem__)(unique)

    stds = np.empty(len(remapped))
    for i in range(len(remapped)):
        iteration = remapped[i]
        stds[i] = np_calculate_iteration_mean_and_stdev(iteration)

    calculated = np.argmin(stds)
    return unique[calculated].tolist()


def np_calculate_iteration_mean_and_stdev(iteration):
    # Needs to Calculate Stdev for each iteration, e.g.:
    # [[1108 1220 1231 1231]
    #  [1266 1273 1285 1349]
    #  [1358 1362 1519 1621]
    #  [1467 1543 1647 1851]]
    return np.std(np.apply_along_axis(np.sum, 1, iteration))


def replace_dict_keys_with_incremental_value(data):
    new = {}
    current = 0
    for values in data.values():
        new[current] = values
        current += 1
    return new