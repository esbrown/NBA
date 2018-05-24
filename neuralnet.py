import csv
import numpy as np
from keras.utils import to_categorical
from keras import models
from keras import layers

class neuralnet():
    def __init__(self, filename):
        self.playerData = self.createDict(filename)

    def createDict(self, filename):
    	playerData = {}
    	with open(filename, 'rU') as csvfile:
    		reader = csv.reader(csvfile)
    		for row in reader:
    			name = row[0].lower().split()
    			name[0] = name[0][0] + '.'
    			name = ''.join(name)
    			playerData[name] = [float(item) if item != '' else 0 for item in row[1:]]
    	return playerData

    def prepareData(self, data):
        x = []
        y = []
        with open(data, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # print row
                names = row[0]
                names = names.lower().split(', ')
                lineupStatistics = np.zeros(130) #stack 5 player stats
                for i, name in enumerate(names):
                    if name not in self.playerData: ###takes care of suffix issue
                        name = name.split()[0]
                    # print self.playerData[name]
                    lineupStatistics[i*26:(i+1)*26] = self.playerData[name]
                x.append(lineupStatistics)
                y.append(1 if float(row[1]) > 0 else 0)
        x = np.array(x)
        y = np.array(y)

        trainX, devX, testX = np.split(x, [150, 200], axis = 0)
        trainY, devY, testY = np.split(y, [150, 200], axis = 0)

        return trainX, trainY, devX, devY, testX, testY
        # print y
        # print x.shape, y.shape

    def trainModel(self, X, Y, devX, devY):
        model = models.Sequential()
        model.add(layers.Dense(50, activation = 'relu', input_shape=(130,)))
        model.add(layers.Dropout(0.3, noise_shape = None, seed = None))
        model.add(layers.Dense(50, activation = 'relu'))
        model.add(layers.Dropout(0.3, noise_shape = None, seed = None))
        model.add(layers.Dense(50, activation = 'relu'))
        model.add(layers.Dense(1, activation = 'sigmoid'))
        model.summary()
        model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
        results = model.fit(X,Y, epochs = 30, batch_size = 25, validation_data = (devX, devY))
        print ("Test-Accuracy: ", np.mean(results.history['val_acc']))

def main():
    net = neuralnet('nba_player_data.csv')
    trainX, trainY, devX, devY, testX, testY = net.prepareData('lineup_data.csv')
    model = net.trainModel(trainX, trainY, devX, devY)


    # print 'baseline plusMinus:', nba.baseline()

if __name__ == "__main__":
    main()
