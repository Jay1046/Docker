from tensorflow.keras.layers import Dense
import tensorflow as tf

class Softmax(tf.keras.Model):
    def __init__(self):
        super(Softmax, self).__init__()
        self.dense = Dense(3, input_dim=4, activation='softmax')
    
        
    def call(self, x):
        out = self.dense(x)
        return out
    
    
 