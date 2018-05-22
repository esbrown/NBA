import csv

class NBA():

    def __init__(self, filename):
        self.data = self.cleanData(filename)

    #baseline returns a simple plus-minus based on the average of the individual
    #plus/minus ratings for each player per game.
    # def baseline(self):
    #     avgPlusMinus = 0.0
    #     for player in self.data:
    #         avgPlusMinus += self.data[player]
    #     avgPlusMinus /= len(self.data)
    #     return avgPlusMinus

    def cleanData(self, filename):
        players = {}
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            print next(readCSV) #skip column headers
            for row in readCSV:
                name = row[0]
                stats = [float(num) for num in row[1:]]
                print stats
                if stats[0] >= -1: #have played at least ? games
                    players[name] = stats
        return players

def main():
    nba = NBA('normalized_abbrev_data.csv')
    print nba.data
    # print 'baseline plusMinus:', nba.baseline()

if __name__ == "__main__":
    main()
