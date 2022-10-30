import random as rd
import statistics as stats


def main_compute(mode, data, team_size):
    message = []
    if mode == 0:
        team_list = standard_compute(data, team_size)
    if mode == 1:
        team_list = random_compute(data, team_size)
        message.append("Random Team Assignment")

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
        current_team_elo = sum(team_elo)/len(team_elo)
        message.append("= Average Team Elo: " + str(current_team_elo))
        global_elo.append(current_team_elo)
    message.append("\n")
    message.append("=> Group Elo: " + str(sum(global_elo)/len(global_elo)))
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
