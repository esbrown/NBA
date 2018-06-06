import csv
from sklearn.cluster import KMeans
import sklearn.utils.class_weight as class_weight
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns;
import pylab as pl

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.datasets.samples_generator import make_blobs
from pandas.tools.plotting import parallel_coordinates

from sklearn.metrics import silhouette_samples, silhouette_score

from sklearn.datasets import load_iris

class NBA():

    def __init__(self, filename, numClusters):
        self.NUM_CLUSTERS = numClusters
        self.classes = []
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
            self.classes = next(readCSV) #skip column headers
            for row in readCSV:
                name = row[0]
                stats = [float(num) if num != "NA" else 0 for num in row[1:] ]
                # if stats[0] >= -1: #have played at least ? games
                players[name] = stats
        return players


    def kmeans(self):
        stats = np.array(self.data.values())
        names = self.data.keys()
        kmeans = KMeans(n_clusters=self.NUM_CLUSTERS, random_state=0).fit(stats)
        y_kmeans = kmeans.predict(stats)
        centers = kmeans.cluster_centers_
        # print 'YKMEANS: ' + str(y_kmeans)
        # print 'KMEANS: ' + str(kmeans)
        # print 'CLUSTER CENTERS: ' + str(kmeans.cluster_centers_)
        # print 'LABELS: ' + str(kmeans.labels_)
        labeledPlayers = {}
        clusters = [[] for i in range(self.NUM_CLUSTERS)]
        for i, cluster in enumerate(kmeans.labels_):
            clusters[cluster].append(names[i])
            labeledPlayers[names[i]] = cluster
        #for cluster in clusters:
            #print cluster, len(cluster)
        #silhouette_avg = silhouette_score(stats, y_kmeans)
        print labeledPlayers
        #print 'num clusters: ' + str(self.NUM_CLUSTERS) + '  silhouette_score: ' + str(round(silhouette_avg, 4))
        #self.visualize(kmeans, stats)


    def visualize(self, kmeans, stats):
        pca = PCA(n_components=2).fit(stats)
        pca_2d = pca.transform(stats)
        clusters = kmeans.cluster_centers_
        clusters_2d = pca.transform(clusters)
        colors = ['r','b','y','g','c','m']
        pl.scatter(pca_2d[:, 0], pca_2d[:, 1], s=20, c=[colors[l_] for l_ in kmeans.labels_])
        plt.scatter(clusters_2d[:, 0], clusters_2d[:, 1], s=80, marker='x', c=[c for c in colors[:len(clusters_2d)]])
        pl.show()



def main():
    nba = NBA('combined_nba_player_data.csv', 5)
    nba.kmeans()
    #X, y = make_blobs(n_samples=200, centers=3, n_features=2, random_state=0)
    #plt.scatter(X[:,0], X[:,1], c=y)
    #plt.show()
    # print 'baseline plusMinus:', nba.baseline()

if __name__ == "__main__":
    main()
