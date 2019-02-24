from tkinter import *
import espn_scrape as es

league = 'http://www.espn.in/football/teams/'

LEAGUES = ['Select',
           '1. La Liga',
           '2. English Premier League',
           '3. Bundesliga',
           '4. Serie A',
           '5. Ligue 1',
           ]

TEAMS = ['Select',
         '1. La Liga',
         '2. English Premier League',
         '3. Bundesliga',
         '4. Serie A',
         '5. Ligue 1',
         ]

root = Tk()
root.geometry("700x500")
root.title('Get scores')
topFrame = Frame(root)
topFrame.pack(fill=X)

theLabel = Label(topFrame, text='Hey there')

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

def theUsual():
    team_list = es.get_all_teams('http://www.espn.in/football/teams/_/league/esp.1')
    soup = es.set_team(team_list['Barcelona'])
    output = es.get_games(soup, 'The Usual -- Barcelona')
    matches = Label(bottomFrame, text=output)
    matches.config(font=("Ariel", 10))
    matches.grid(row=0, columnspan=3, padx=10, pady=10)


def get_league(value):
    global league
    league = es.get_all_leagues(value[0])
    teams = StringVar(topFrame)
    all_teams = es.get_all_teams(league).keys()
    all_teams_1 = list(all_teams)
    all_teams_1.insert(0, 'Select')
    teams.set(all_teams_1[0]) # default value
    global entry_1
    entry_1.grid_forget()
    entry_1 = OptionMenu(topFrame, teams, *all_teams_1, command=get_games)
    entry_1.grid(row=3, column=1, padx=10, pady=10)

def get_games(value):
    team_list = es.get_all_teams(league)
    soup = es.set_team(team_list[value])
    output = es.get_games(soup, value)
    global matches
    matches.grid_forget()
    matches = Label(bottomFrame, text=output)
    matches.config(font=("Ariel", 10))
    matches.grid(row=0, columnspan=3, padx=10, pady=10)

button_1 = Button(topFrame, text="The usual?", fg='red', command=theUsual)
button_1.config(font=("Ariel", 10))

label_0 = Label(topFrame, text='What league does your favourite team play in?')
leagues = StringVar(topFrame)
leagues.set(LEAGUES[0]) # default value
entry_0 = OptionMenu(topFrame, leagues, *LEAGUES, command=get_league)

theLabel.config(font=("Ariel", 24))
theLabel.grid(row=0, columnspan=3, padx=10, pady=10)

button_1.grid(row=1, columnspan=3, padx=10, pady=10)

label_0.config(font=("Ariel", 10))
label_0.grid(row=2, padx=10, pady=10)

entry_0.grid(row=2, column=1, padx=10, pady=10)

label_1 = Label(topFrame, text='Your favourite team?')
label_1.config(font=("Ariel", 10))
label_1.grid(row=3, padx=10, pady=10)

teams = StringVar(topFrame)
teams.set('Select')
entry_1 = OptionMenu(topFrame, teams, *['Select'])
entry_1.grid(row=3, column=1, padx=10, pady=10)

matches = Label(bottomFrame, text="")
matches.config(font=("Ariel", 10))
matches.grid(row=0, columnspan=3, padx=10, pady=10)

root.mainloop()
