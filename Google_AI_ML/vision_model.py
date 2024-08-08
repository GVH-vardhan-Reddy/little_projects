#importing stuff
import tensorflow as tf
print(tf.__version__)
mnist = tf.keras.datasets.fashion_mnist
(training_images, training_labels), (test_images, test_labels) = mnist.load_data()
'''Calling load_data on that object gives you two sets of two lists: training values and 
testing values, which represent graphics that show clothing items and their labels.'''
import matplotlib.pyplot as plt
#normalization
training_images  = training_images / 255.0
test_images = test_images / 255.0
model = tf.keras.models.Sequential([tf.keras.layers.Flatten(), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(10, activation=tf.nn.softmax)])
#Sequential defines a sequence of layers in the neural network.
#Flatten takes a square and turns it into a one-dimensional vector.
#Dense adds a layer of neurons.
#Activation functions tell each layer of neurons what to do. There are lots of options, but use these for now
#Relu effectively means that if X is greater than 0 return X, else return 0. It only passes values of 0 or greater to the next layer in the network.
'''Softmax takes a set of values, and effectively picks the biggest one. For example, 
if the output of the last layer looks like [0.1, 0.1, 0.05, 0.1, 9.5, 0.1, 0.05, 0.05, 0.05], 
then it saves you from having to sort for the largest value—it returns [0,0,0,0,1,0,0,0,0].
Back'''
#traning the model.
model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(training_images, training_labels, epochs=5)
model.evaluate(test_images, test_labels)

