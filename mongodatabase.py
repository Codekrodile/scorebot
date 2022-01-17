import pymongo

class Database:
    def __init__(self, link="mongodb://localhost:27017/", db_name=''):
        '''initialise database'''
        # print("connecting to:", link)
        self.client = pymongo.MongoClient(link)
        self.db = self.client[db_name]

    def reset_scoreboard(self):
        '''reset scoreboard'''
        # scoreboard = [
        #     {"Team":"A", "BBall":0, "Soccer":0, "Carrom":0, "Dart":0, "Foosball":0, "Total":0}, 
        #     {"Team":"B", "BBall":0, "Soccer":0, "Carrom":0, "Dart":0, "Foosball":0, "Total":0}, 
        #     {"Team":"C", "BBall":0, "Soccer":0, "Carrom":0, "Dart":0, "Foosball":0, "Total":0}, 
        #     {"Team":"CSS", "BBall":0, "Soccer":0, "Carrom":0, "Dart":0, "Foosball":0, "Total":0}, 
        #     {"Team":"SHQ", "BBall":0, "Soccer":0, "Carrom":0, "Dart":0, "Foosball":0, "Total":0}
        # ]

        sport = [
            {"team":"A", "bball":0, "soccer":0, "total":0}, 
            {"team":"B", "bball":0, "soccer":0, "total":0}, 
            {"team":"C", "bball":0, "soccer":0, "total":0}, 
            {"team":"CSS", "bball":0, "soccer":0, "total":0}, 
            {"team":"SHQ", "bball":0, "soccer":0, "total":0}
        ]

        mess = [
            {"team":"A", "carrom":0, "dart":0, "foosball":0, "total":0}, 
            {"team":"B", "carrom":0, "dart":0, "foosball":0, "total":0}, 
            {"team":"C", "carrom":0, "dart":0, "foosball":0, "total":0}, 
            {"team":"CSS", "carrom":0, "dart":0, "foosball":0, "total":0}, 
            {"team":"SHQ", "carrom":0, "dart":0, "foosball":0, "total":0}
        ]

        # event = [] #tbc
        
        coll = self.db["SPORT"]
        coll.delete_many({})
        coll.insert_many(sport)

        coll = self.db["MESS"]
        coll.delete_many({})
        coll.insert_many(mess)
        return

    def update_scoreboard(self, game, team, point):
        '''update scoreboard'''
        if game == "bball" or game == "soccer":
            coll = self.db["SPORT"]
        else: #game is either carrom, dart or foosball
            coll = self.db["MESS"]

        search = {"team":team}
        
        #get current point and add new points
        for document in coll.find(search).limit(1):
            update1 = {"$set":{game:document[game] + point}}
            update2 = {"$set":{"total":document["total"] + point}}

        coll.update_one(search, update1)
        coll.update_one(search, update2)
        return
    
    def get_total_scoreboard(self):
        '''get overall scoreboard'''
        coll1 = self.db["SPORT"]
        coll2 = self.db["MESS"]
        scoreboard = []

        for document in coll1.find({}, {"team":1, "total":1}):
            scoreboard.append([document["team"], document["total"]])

        n = 0
        for document in coll2.find({}, {"team":1, "total":1}):
            scoreboard[n].extend([document["total"], document["total"] + scoreboard[n][1]])
            n += 1

        scoreboard.sort(key= lambda x: x[3], reverse= True) #sort scoreboard in order of total score

        return scoreboard

    def get_sport_scoreboard(self):
        '''get sport scoreboard'''
        coll = self.db["SPORT"]
        scoreboard = []

        for document in coll.find({}, {"team":1, "bball":1, "soccer":1, "total":1}).sort("total", -1):
            scoreboard.append([document["team"], document["bball"], document["soccer"], document["total"]])

        return scoreboard

    def get_mess_scoreboard(self):
        '''get MESS scoreboard'''
        coll = self.db["MESS"]
        scoreboard = []

        for document in coll.find({}, {"team":1, "carrom":1, "dart":1, "foosball":1, "total":1}).sort("total", -1):
            scoreboard.append([document["team"], document["carrom"], document["dart"], document["foosball"], document["total"]])

        return scoreboard

    def get_all_teams(self):
        '''get names of teams'''
        coll = self.db["SPORT"]
        teams = []

        for document in coll.find({}, {"team":1}):
            teams.append(document.get("team"))
        
        return teams
