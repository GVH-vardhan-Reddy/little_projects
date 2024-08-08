#imports
import tensorflow as tf
import numpy as np
from tensorflow import keras
#Define and compile the neural network
#in this case only one neuron
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
'''you need two things for an optimizer and an loss'''
#loss:how badly it went
#optimizer:how to correct it
model.compile(optimizer='sgd', loss='mean_squared_error')
#this is the data provided
xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)
#epoch is a cycle of rejection and correction for machine learning model
#greater epochs greater learning
#the below command is used to train the model
model.fit(xs, ys, epochs=10)
#predict the outcome
print(model.predict(np.array([10.0])))
