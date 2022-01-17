def format_input(txt):
    txt = txt.split(" ")
    if 4 <= len(txt) <= 8:
        try:
            game, teams, point = txt[1].lower(), list(set(txt[2:-1])), int(txt[-1])

            if game not in ["bball", "soccer", "carrom", "dart", "foosball"]:
                return -1, -1, 'invalid game'
            
            for team in teams:
                if team not in ["a", "b", "c", "css", "shq"]:
                    return -1, -1, 'invalid team'

            teams = [i.upper() for i in teams]
            return game, teams, point
        
        except:
            return -1, -1, 'invalid point'
    else:
        return -1, -1, 'invalid format'

def display_total_scoreboard(lst):
    scoreboard = f"""
┌──────── •✧✧• ────────┐
{'OVERALL SCOREBOARD': ^24}
 {'Team': <5}{'Sport': <6}{'Mess': <5}{'Total': <6}
"""

    for i in lst:
        scoreboard += f" {i[0]: ^5}{i[1]: ^6}{i[2]: ^5}{i[3]: ^6} \n"
    
    scoreboard += "└──────── •✧✧• ────────┘\n"
    
    return scoreboard

def display_sport_scoreboard(lst):
    scoreboard = f"""
┌──────── •✧✧• ────────┐
{'SPORT SCOREBOARD': ^24}
{'Team': <5}{'BBall': <6}{'Soccer': <7}{'Total': <6}
"""

    for i in lst:
        scoreboard += f"{i[0]: ^5}{i[1]: ^6}{i[2]: ^7}{i[3]: ^6} \n"
    
    scoreboard += "└──────── •✧✧• ────────┘\n"
    
    return scoreboard

def display_mess_scoreboard(lst):
    scoreboard = f"""
┌──────── •✧✧• ────────┐
{'MESS SCOREBOARD': ^24}
{'': <4}{'Carrom': <7}{'Dart': <5}{'Fball': <6}{'T'}
"""

    for i in lst:
        scoreboard += f"{i[0]: ^5}{i[1]: ^6}{i[2]: ^5}{i[3]: ^6}{i[4]} \n"
    
    scoreboard += "└──────── •✧✧• ────────┘\n"
    
    return scoreboard