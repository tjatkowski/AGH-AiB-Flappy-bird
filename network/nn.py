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
            
    @staticmethod
    def mse(X, Y):
        A = X.reshape(-1)
        B = Y.reshape(-1)
        return np.sum((A-B)**2) / A.shape[0]