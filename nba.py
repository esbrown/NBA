class NBA():

    def __init__(self):
        self.data = {
            "Bradley Beal": 1.7,
            "John Wall": 1.5,
            "Otto Porter": 3.6,
            "Markieff Morris": -0.5,
            "Marcin Gortat": 0.3,
        }

    #baseline returns a simple plus-minus based on the average of the individual
    #plus/minus ratings for each player per game.
    def baseline(self):
        avgPlusMinus = 0.0
        for player in self.data:
            avgPlusMinus += self.data[player]
        avgPlusMinus /= len(self.data)
        return avgPlusMinus

def main():
    nba = NBA()
    print 'baseline plusMinus:', nba.baseline()

if __name__ == "__main__":
    main()
