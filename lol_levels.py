# File:         lol_levels.py
# Author:       Joinemm
# Date:         24/09/18
# Version:      1.2
# License:      GNU General Public License v3.0
# Description:  Calculates the days it takes to reach summoner level 30
#               in league of legends with the given parameters


def main():
    # user inputs and their validation
    current_level = int(input("Current level (1-30): "))
    while current_level < 1 or current_level >= 30:
        print("Error: Invalid level!")
        current_level = int(input("Current level (1-30): "))

    games_per_day = int(input("Games per day: "))
    while games_per_day < 1:
        print("Games played must be at least 1")
        games_per_day = int(input("Games per day: "))

    game_time = int(input("Average Game duration in minutes: "))
    winrate = float(input("Winrate % (0-100): ")) * 0.01
    boost = int(input("xp boosts? (0 = none, 1 = win boost, 2 = day boost, 3 = both): "))

    # check boosts
    winboost, durboost = check_boosts(boost)

    # calculate the values
    days_to_30, games_to_30 = calculate_days(current_level, games_per_day, game_time, winrate, durboost, winboost)

    print("It will take {:.1f} days to reach lvl 30, a total of {:} games".format(days_to_30, games_to_30))
    if winboost or durboost:
        boostcost = 0
        if winboost:
            boostcost += boosts_cost_win(games_to_30*winrate)
        if durboost:
            boostcost += boost_cost_duration(days_to_30)
        print("The boosts will cost {:}RP, which is ".format(boostcost))
    print()
    input("Press enter to exit")


def exp_formula(win, minutes, seconds=0):
    time = seconds + minutes * 60  # the total number of seconds elapsed in a game
    if win:
        xp_per_s = 0.11
        base_xp = 6.6
    else:
        xp_per_s = 0.09
        base_xp = 5.4
    xp = (time * xp_per_s + base_xp)
    return int(round(xp))


def calculate_days(level, games_per_day, game_time, winrate, boost_dur, boost_win):
    # average xp per day based on winrate
    xp_per_day = ((games_per_day * exp_formula(True, game_time) * winrate)
                  + (games_per_day * exp_formula(False, game_time) * (1 - winrate)))

    # add xp boosts if active
    if boost_dur:
        xp_per_day += xp_boost_duration((exp_formula(True, game_time) * winrate
                                        + exp_formula(False, game_time) * (1 - winrate)), games_per_day)
    if boost_win:
        xp_per_day += xp_boost_win(games_per_day*winrate)

    # first win of the day only starts at level 15, check if level 15 is reached
    if level < 15:
        days_to_15 = (exp_dictionary(15) - exp_dictionary(level)) / float(xp_per_day)

        # only get first win of the day if you win games
        if winrate > 0:
            days_15_to_30 = (exp_dictionary(30) - exp_dictionary(15)) / float(xp_per_day + 400)
        else:
            days_15_to_30 = (exp_dictionary(30) - exp_dictionary(15)) / float(xp_per_day)

        days = days_to_15 + days_15_to_30

    # level 15 is reached -> apply first win of the day to all games
    else:
        if winrate > 0:
            days = (exp_dictionary(30) - exp_dictionary(level)) / float(xp_per_day + 400)
        else:
            days = (exp_dictionary(30) - exp_dictionary(level)) / float(xp_per_day)

    games = int(round(days * games_per_day))
    return days, games


def xp_boost_duration(game_xp, games_total):
    # double xp for every game
    return game_xp * games_total


def xp_boost_win(games_won):
    # additional 210xp for every win, losses give nothing
    return games_won * 210


def check_boosts(boost):
    # checks if any boosts are selected
    if not (boost == 0 or boost > 3):
        if boost == 3:
            winboost = True
            durboost = True
        elif boost == 2:
            winboost = False
            durboost = True
        elif boost == 1:
            winboost = True
            durboost = False
        else:
            winboost = False
            durboost = False

        return winboost, durboost
    else:
        return False, False


def boost_cost_duration(days):
    # calculates the amount of RP needed for the boosts
    costs = {
        1: 290,
        3: 520,
        7: 1020,
        14: 1846,
        30: 3490
    }
    return dictionary_scraper(costs, days)


def boosts_cost_win(wins):
    # calculates the amount of RP needed for the boosts
    costs = {
        3: 290,
        5: 390,
        10: 670,
        15: 990,
        25: 1590,
        40: 2240
    }
    return dictionary_scraper(costs, wins)


def riot_points_cost(rp):
    # calculates the amount of currency needed to buy the required amount of RP
    costs = {
        350: 2.50,
        750: 5.00,
        1580: 10.00,
        3250: 20.00,
        5725: 35.00,
        8250: 50.00
    }
    return dictionary_scraper(costs, rp)


def dictionary_scraper(dictionary, value):
    # goes through a dictionary of costs and adds them together to be the most cost effective
    total = 0
    for x in sorted(dictionary, reverse=True):
        while value >= x:
            total += int(dictionary.get(x))
            value -= x
    return total


def exp_dictionary(level):
    # hardcoded xp thresholds per level since I couldn't figure out the formula
    experience = {
        1: 0,
        2: 144,
        3: 288,
        4: 480,
        5: 720,
        6: 1056,
        7: 1488,
        8: 2016,
        9: 2640,
        10: 3360,
        11: 4176,
        12: 5088,
        13: 6072,
        14: 7128,
        15: 8256,
        16: 9600,
        17: 11040,
        18: 12576,
        19: 14256,
        20: 16080,
        21: 18048,
        22: 20160,
        23: 22368,
        24: 24816,
        25: 27120,
        26: 29616,
        27: 32112,
        28: 34704,
        29: 37392,
        30: 40560
    }
    return float(experience.get(level))


main()
