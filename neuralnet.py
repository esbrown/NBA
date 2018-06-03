import csv
import numpy as np
from keras.utils import to_categorical
from keras import models
from keras import layers
from keras import regularizers

class neuralnet():
    def __init__(self):
        self.playerData = self.createDict('normalized_neural_data.csv')
        self.playerData2017 = self.createDict('normalized_neural_data_2017.csv')
        self.playerData2016 = self.createDict('normalized_neural_data_2016.csv')
        self.playerData2015 = self.createDict('normalized_neural_data_2015.csv')
        self.playerData2014 = self.createDict('normalized_neural_data_2014.csv')
        self.playerData2013 = self.createDict('normalized_neural_data_2013.csv')
        self.playerData2012 = self.createDict('normalized_neural_data_2012.csv')
        self.playerData2011 = self.createDict('normalized_neural_data_2011.csv')

    def createDict(self, filename):
        playerData = {}
        with open(filename, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name = row[0].lower().split()
                if name == []: ### weird error
                    continue
                name[0] = name[0][0] + '.'
                name = ''.join(name)
                name = name.replace("*", "")
                if name not in playerData and name != 't.':
                    playerData[name] = [float(item) if item != '' else 0 for item in row[1:]]
        return playerData

    def appendData(self, fileName, dictName, x, y):
        with open(fileName, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # print row
                names = row[0]
                names = names.lower().split(', ')
                lineupStatistics = np.zeros(130) #stack 5 player stats
                for i, name in enumerate(names):
                    if name not in dictName: ###takes care of suffix issue
                        name = name.split()[0]
                    lineupStatistics[i*26:(i+1)*26] = dictName[name]
                x.append(lineupStatistics)
                y.append(1 if float(row[1]) > 0 else 0)
        return x,y

    def prepareData(self):
        x = []
        y = []
        x,y = self.appendData('lineup_data.csv', self.playerData, x, y)
        x,y = self.appendData('lineup_data_2016-17.csv', self.playerData2017, x, y)
        x,y = self.appendData('lineup_data_2015-16.csv', self.playerData2016, x, y)
        x,y = self.appendData('lineup_data_2014-15.csv', self.playerData2015, x, y)
        x,y = self.appendData('lineup_data_2013-14.csv', self.playerData2014, x, y)
        x,y = self.appendData('lineup_data_2012-13.csv', self.playerData2013, x, y)
        x,y = self.appendData('lineup_data_2011-12.csv', self.playerData2012, x, y)
        x,y = self.appendData('lineup_data_2010-11.csv', self.playerData2011, x, y)

        x = np.array(x)
        y = np.array(y)

        permutation = np.random.permutation(len(x))
        x = x[permutation]
        y = y[permutation]

        trainX, devX, testX = np.split(x, [1800, 1900], axis = 0)
        trainY, devY, testY = np.split(y, [1800, 1900], axis = 0)

        return trainX, trainY, devX, devY, testX, testY

    def trainModel(self, X, Y, devX, devY):
        model = models.Sequential()
        model.add(layers.Dense(4, activation = 'relu', input_shape=(130,)))
        model.add(layers.Dropout(0.6, noise_shape = None, seed = None))
        # model.add(layers.Dense(5, activation = 'relu'))
        # model.add(layers.Dropout(0.6, noise_shape = None, seed = None))
        model.add(layers.Dense(1, activation = 'sigmoid'))
        model.summary()
        model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
        results = model.fit(X,Y, epochs = 150, batch_size = 50, validation_data = (devX, devY))
        print ("Test-Accuracy: ", np.mean(results.history['val_acc']))
        return model

def main():
    net = neuralnet()
    trainX, trainY, devX, devY, testX, testY = net.prepareData()
    model = net.trainModel(trainX, trainY, devX, devY)
    predictions = model.predict(testX)
    # predictions = (predictions - np.mean(predictions))/np.std(predictions)
    # predictions = (predictions + np.mean(testY))*np.std(testY)
    count = 0
    for i in range(len(predictions)):
        print(predictions[i], testY[i])
    predictions = predictions > 0.5
    count = 0
    for i in range(len(predictions)):
        if predictions[i] == testY[i]:
            count += 1
    print(float(count)/len(predictions))




if __name__ == "__main__":
    main()
