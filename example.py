from network.dense import Dense
from network.nn import NeuralNetwork
import numpy as np
import timeit
from copy import deepcopy

if __name__ == '__main__':
    # 2 input units
    # 5 hidden units
    # 1 output unit
    model = NeuralNetwork([
        Dense(size=(2, 5), activation='relu', init_method='He'),
        Dense((5, 1), activation='sigmoid', init_method='He')
    ])

    start = timeit.timeit()
    model2 = deepcopy(model)
    end = timeit.timeit()

    print(f"deep copy time:{end - start}")
    print(f"model 1 weights before:\n{model.layers[0].W}")
    print()

    model2.mutate(amount=0.5)
    
    print(f"model 1 weights after:\n{model.layers[0].W}")
    print()
    print(f"model 2 weights after:\n{model2.layers[0].W}")
    