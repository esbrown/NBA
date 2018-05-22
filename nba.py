import csv
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns;

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
                stats = [float(num) if num != "NA" else 0 for num in row[1:] ]
                # if stats[0] >= -1: #have played at least ? games
                players[name] = stats
        return players

    def kmeans(self):
        NUM_CLUSTERS = 5
        stats = np.array(self.data.values())
        names = self.data.keys()
        print names

        kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=0).fit(stats)
        y_kmeans = kmeans.predict(stats)
        print kmeans
        print kmeans.cluster_centers_
        print kmeans.labels_
        clusters = [[] for i in range(NUM_CLUSTERS)]
        for i, cluster in enumerate(kmeans.labels_):
            clusters[cluster].append(names[i])
        for cluster in clusters:
            print cluster, len(cluster)

        # plt.scatter(stats[:, 0], stats[:, 1], c=y_kmeans, s=50, cmap='viridis')
        #
        # centers = kmeans.cluster_centers_
        # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);
        # plt.show(block=True)



def main():
    nba = NBA('combined_nba_player_data.csv')
    nba.kmeans()
    # print 'baseline plusMinus:', nba.baseline()

if __name__ == "__main__":
    main()
