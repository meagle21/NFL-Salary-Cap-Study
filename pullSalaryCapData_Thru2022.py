import requests
from bs4 import BeautifulSoup 
import pandas as pd

years = [2020, 2021, 2022] #years that we can parse salary data from
for year in years:
	print(f"Collecting data for the year: {year}...")
	teams = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 
			 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 
			 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 
			 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 
			 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 
			 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 
			 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Commanders'] #nfl team names in list
	playerInfoDict = {"team" : [], "name" : [], "position" : [], "signing_bonus" : [], "base_salary": [], "restruct_bonus" : [],
							  "roster_bonus" : [], "workout_bonus" : [], "incentive_bonus" : [], "cap_hit" : []
							  } #dictionary will store the player data we get
	for team in teams:
		teamHyphen = team.replace(" ", "-") #urls dont include spaces, replace with hyphens
		if(team == "Washington Commanders" and year <= 2021): #since prior to 2022 the washington commanders were named washington football team, change name
			teamHyphen = "washington-football-team"
			requestUrl = rf"https://www.spotrac.com/nfl/{teamHyphen}/cap/{year}" #create the request url
		requestUrl = rf"https://www.spotrac.com/nfl/{teamHyphen}/cap/{year}" #create the request url
		response = requests.get(requestUrl) #send get request to the website 
		soupWebsite = BeautifulSoup(response.text, "html.parser") #get beautiful soup
		playerSalaryDataTable = soupWebsite.find("div", {"class" : "teams"}) #parse for the table tag
		playerSalaryDataRows = playerSalaryDataTable.find_all("tr")[:-1] #get player salary data rows
		for row in playerSalaryDataRows:
			playerInfo = row.find_all("td") #find all "td" tags which are each of the columns associated with the rows
			if(len(playerInfo) != 0):
				nameSplit = playerInfo[0].text.split("\n") #clean the html data to get the name of the player
				sentValues = 0
				if(len(nameSplit) > 1):
					for column in playerInfo:
						spanTag = column.find("span")
						if(spanTag is not None):
							spanTitle = spanTag.get("title")
							spanClass = spanTag.get("class")
							if(spanTitle == "Cap Hit"):
								playerInfoDict["cap_hit"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
							elif(spanTitle == "Signing Bonus"):
								playerInfoDict["signing_bonus"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
							elif(spanTitle == "Restructure Bonus"):
								playerInfoDict["restruct_bonus"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
							elif(spanTitle == "Workout Bonus"):
								playerInfoDict["workout_bonus"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
							elif(spanTitle == "Incentive Bonus"):
								playerInfoDict["incentive_bonus"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
							elif(spanTitle == "Roster Bonus"):
								playerInfoDict["roster_bonus"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
							elif(spanTitle is None and spanClass == ["cap"]):
								playerInfoDict["base_salary"].append(spanTag.text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", ""))
								sentValues += 1
					playerInfoDict["team"].append(team)
					playerInfoDict["name"].append(nameSplit[1])
					playerInfoDict["position"].append(playerInfo[1].text.replace("-", "").replace("(", "").replace(")", "").replace("$", "").replace(",", "")) #clean up the data that has "-", "(", ")", or "$"
					sentValues += 3
					if(sentValues != 10):
						listOfListsToClear = ["team", "name", "position", "base_salary"] #there are four players in 2020 that have weird html strcture that causes them not to be added, just going to ignore for now
						for playerInfoDictList in listOfListsToClear:
							playerInfoDict[playerInfoDictList].pop(-1)
				else:
					pass
	print(f"Collected salary data for the year: {year}.")
	playerInfoDf = pd.DataFrame.from_dict(playerInfoDict) #turn the dictionary into a dataframe
	playerInfoDf.to_csv(rf"Data/playerSalaryData_{year}.csv", index = False) #export the dataframe to the csv