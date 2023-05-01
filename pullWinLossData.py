import requests
import pandas as pd


years = [2020, 2021, 2022] #year list

teamListDict = {"year" :[], "name" : [], "win_rate" : []} #team list dictionary

for year in years:

	url = rf"https://nfl-team-stats.p.rapidapi.com/v1/nfl-stats/teams/win-stats/{year}" #create URL with the correct year
	headers = {
				"content-type" : "application/octet-stream",
				"X-RapidAPI-Key" : "0658ad2267msh9349255b16f8e22p1eddd8jsn5ffcd5635e05",
				"X-RapidAPI-Host" : "nfl-team-stats.p.rapidapi.com"
		      }	 #intitalize headers so we can make the requests with the correct creds
	response = requests.get(url, headers = headers).json() #get the json response 
	teamsList = response["_embedded"]["teamWinStatsList"] #get the list of teams 
	for i in range(len(teamsList)):
		team = teamsList[i] #index into the groups of 4 
		teamName, winPercentage = team["name"], team["winRatePercentage"]
		teamListDict["year"].append(year)
		teamListDict["win_rate"].append(winPercentage)
		teamListDict["name"].append(teamName.replace(" xy", "").replace(" xz*", "").replace(" xz", "").replace(" x", ""))
outputDataframe = pd.DataFrame.from_dict(teamListDict)
outputDataframe.to_csv(r"Data/winLossData.csv", index = False)
