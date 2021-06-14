import numpy as np

class Dense:
    def __init__(self, size, activation=None, init_method=None, W=None):
        """
        size: Tuple holding number of neurons in the input and the output
        activation: Activation function
            -'elu': Exponential Linear Unit  function
            -'relu': Rectified linear activation function
            -'none': linear activation
        init_method: method for initializing the weights
            -'He' initialization
            -'Xavier'(Glorot) initialization
        """
        self.size = size
        self.in_size = size[0]
        self.out_size = size[1]
        self.__init_weights(init_method, W)
        self.Z = None
        self.A = None
        if activation is None:
            self.nonlin = lambda x: x
            self.nonlin_deriv = lambda x: np.ones(x.shape)
        elif activation == 'elu':
            self.nonlin = Dense.elu
            self.nonlin_deriv = Dense.dElu
        elif activation == 'relu':
            self.nonlin = Dense.relu
            self.nonlin_deriv = Dense.dRelu
        elif activation == 'sigmoid':
            self.nonlin = Dense.sigmoid
            self.nonlin_deriv = Dense.dSigmoid
        
    def __init_weights(self, init_method, W):
        if init_method == 'He':
            self.W = np.random.randn(self.size[0], self.size[1]) * np.sqrt(1/self.size[0])
            self.b = np.zeros((1, self.out_size)) 
        elif init_method == 'Xavier':
            self.W = np.random.randn(self.size[0], self.size[1]) * np.sqrt(2/(self.size[0] + self.size[1]))
            self.b = np.zeros((1, self.out_size))   
        elif W is not None and type(W) == np.ndarray:
            if W.shape == self.size:
                self.W = W
                self.b = np.zeros((1, self.out_size))   
            else:
                raise ValueError
        else:
            self.W = np.random.normal(0.0, 0.4, size=self.size)
            # self.b = np.random.normal(0.0, 0.2, size=(1, self.out_size))
            self.b = np.zeros((1, self.out_size))  

    def set_weights(self, W, b=None):
        if b is None:
            self.b = np.zeros((1, self.out_size))   
        else:
            if type(b) != np.ndarray:
                print(type(b))
                raise TypeError("Given bias must be numpy array")
            self.b = b
        
        if type(W) != np.ndarray:
            print(type(W))
            raise TypeError("Weights must be numpy array")
        if W.shape != self.size:
            print(W.shape)
            raise TypeError("Wrong shape of weights")
        self.W = W
        
            
    def forward(self, X):
        self.X = X
        self.Z = self.X.dot(self.W) + self.b
        self.A = self.nonlin(self.Z)
        return self.A
        
    def backward(self, dA):
        m = self.X.shape[0]
        dZ = dA * self.nonlin_deriv(self.Z)
        dW = (1/m) * self.X.T.dot(dZ)
        db = (1/m) * np.sum(dZ, axis=0, keepdims=True)
        dX = dZ.dot(self.W.T)
        self.dZ = dZ
        self.dW = dW
        self.db = db
        return dX
    
    def update(self, lr):
        self.W += lr * self.dW
        self.b += lr * self.db

    @staticmethod
    def sigmoid(X):
        return 1/(1+np.exp(-X))

    @staticmethod
    def dSigmoid(Z):
        s = 1/(1+np.exp(-Z))
        dZ = s * (1-s)
        return dZ
            
    @staticmethod
    def relu(Z):
        return np.maximum(0,Z)

    @staticmethod
    def dRelu(x):
        x[x<=0] = 0
        x[x>0] = 1
        return x
    
    @staticmethod
    def elu(x, alpha = 0.01):
        return np.where(x>=0, x, alpha*np.exp(x)-1)
    
    @staticmethod
    def dElu(x, alpha = 0.01):
        return np.where(x>0, 1, alpha*np.exp(x))    