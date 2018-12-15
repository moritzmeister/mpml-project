import pandas as pd
import numpy as np

class DataUtil:
    def __init__(self, sc, inputPath='data/spam.data.txt', statsInputPath='data/mean_std.txt', standardize=True):
        self.inputPath = inputPath
        self.standardize = standardize
        self.mean_std = pd.read_csv(statsInputPath, delimiter=',', header=None)
        self.mean = sc.broadcast(self.mean_std.iloc[:,0].values.astype(float))
        self.std = sc.broadcast(self.mean_std.iloc[:,1].values.astype(float))
        
        
    def read(self, sc):
        if self.standardize:
            return sc.textFile(self.inputPath).map(lambda x: np.asarray(x.split(' ')).astype(float)) \
                    .map(lambda x: (x[:56], x[57])) \
                    .map(lambda x: ((x[0] - self.mean.value[:56])/self.std.value[:56], x[1]))
        else:
            return sc.textFile(self.inputPath).map(lambda x: np.asarray(x.split(' ')).astype(float)) \
                    .map(lambda x: (x[:56], x[57]))