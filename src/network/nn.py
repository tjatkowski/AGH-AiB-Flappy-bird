import matplotlib.pyplot as plt
import numpy as np
from network.dense import Dense

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.lr = None
        self.lr_decay = None
        self.loss_fun = None
        self.history = {}
        
    def fit(self, X, y, validation=None, epochs=100, lr=0.001, lr_decay=0.):
        self.loss_fun = NeuralNetwork.mse
        self.lr = lr
        self.lr_decay = lr_decay
        self.history["loss"] = []
        self.history["val_loss"] = []     
        for i in range(epochs):
            pred = self.__feed_forward(X)
            self.__back_propagation(y)
            train_loss = self.__calc_loss(y)
            self.history["loss"].append(train_loss) 
            if validation:
                X_val, y_val = validation
                _, val_loss = self.evaluate(X_val, y_val)
                self.history["val_loss"].append(val_loss)
            self.lr -= self.lr_decay
            self.__update()
        return self.history
        
    def evaluate(self, X, y):
        pred = self.__feed_forward(X)
        loss = self.__calc_loss(y)
        return pred, loss
    
    def predict(self, X):
        return self.__feed_forward(X)
    
    def plot_loss(self):
        n = range(len(self.history["loss"]))
        plt.plot(n, self.history["loss"], 'r', label='training loss')
        plt.plot(n, self.history["val_loss"], 'b', label='validation loss')
        plt.xlabel("Iteration")
        plt.ylabel("loss")
        plt.title("Loss curves for training")
        plt.legend()
        plt.show()  
    
    def __calc_loss(self, y):
        y_pred = self.layers[-1].A
        return NeuralNetwork.mse(y_pred, y)
        
    def __feed_forward(self, X):
        A = X
        for layer in self.layers:
            A = layer.forward(A)
        return A
    
    def __back_propagation(self, y):
        y_pred = self.layers[-1].A
        n = y.shape[1]
        error = 2 * (y-y_pred) / n
        for layer in self.layers[::-1]:
            error = layer.backward(error)
    
    def __update(self):
        for layer in self.layers:
            layer.update(self.lr)

    def mutate(self,scale=0.01, amount=0.1):
        """
        Change random waights by a small amount
        params:
            scale: std of the weights deltas
            amount: percent of the weights that will be modified
        """
        for layer in self.layers:
            h, w = layer.W.shape
            to_mutate = np.random.rand(h+1,w) < amount
            change = np.random.normal(loc=0, scale=scale, size=(h+1, w)) * to_mutate
            layer.W += change[:-1, :]
            # layer.b += change[-1, :] / 100

    def crossover(self, network, network2 = None, method="random"):
        if method == "random":
            for i, layer in enumerate(self.layers):
                h, w = layer.W.shape
                foo = np.random.rand(h, w)
                mask1 = foo > 0.5
                mask2  = np.invert(mask1)
                if np.any((mask1 + mask2) != 1):
                    raise ValueError
                new_W = mask1*layer.W + mask2*network.layers[i].W
                layer.set_weights(new_W)
        elif method == "half":
            for i, layer in enumerate(self.layers):
                h, w = layer.W.shape
                new_W = layer.W.reshape(-1).copy()
                new_W[h*w // 2: ] = network.layers[i].W.reshape(-1)[h*w // 2: ] 
                layer.W = new_W.reshape(h, w)
        elif method == "mean":
            for i, layer in enumerate(self.layers):
                if network2 is None:
                    layer.W = 0.6*layer.W + 0.4*network.layers[i].W
                else:
                    layer.W = 0.3*layer.W + 0.35*network.layers[i].W + 0.35*network2.layers[i].W
        else:
            for i, layer in enumerate(self.layers):
                if i%2 == 1:
                    layer.set_weights(network.layers[i].W)
        return self
            
    @staticmethod
    def mse(X, Y):
        A = X.reshape(-1)
        B = Y.reshape(-1)
        return np.sum((A-B)**2) / A.shape[0]