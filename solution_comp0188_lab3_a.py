# -*- coding: utf-8 -*-
"""Solution_Comp0188_Lab3_A.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BhRQDv5bRrmQhRHohvUmmohrDTTRodNj

In this lab we will use Baseline Recurrent Neural Network (RNN) model for mnist dataset with plotting functionality for the model and retrain the model with learning rate scheduler which is a component of parameterized learning.

Four components of parameterized learning.

1. Data (Xi and yi): Raw pixlel intensities / extracted features + class labels y=(k=0,1,2 ...9). Each data is D-dimensional. (N=60000 total images, Each image is 28x28 single channel image forming 784 vectors). 

2. Scoring function: output_class_labels = F(Input_images)  

3. Loss function: Measures agreement between predicted class labels and ground-truth class labels.

4. Weights and biases - It will be updated during training process.

# Data

For example, consider
a dataset of 100 images from the MNIST dataset, each image sized 28 × 28 pixels. Using this notation, X1 is the first image, X2 the second image, and so on.

We also define a vector y in supervised learning where yi provides the class label for the i-th example in the dataset.

#Scoring Function                                                       

The scoring function accepts our data as an input and maps the data to class labels. For instance,
given our set of input images, the scoring function takes these data points, applies some function
f (our scoring function), and then returns the predicted class labels, similar to the pseudocode
below: output_class_labels = F(Input_images).

#Loss Function:                                                     
A loss function quantifies how well our predicted class labels agree with our ground-truth labels.
The higher level of agreement between these two sets of labels, the lower our loss (and higher our
classification accuracy, at least on the training set)

#Weights and biases:             
Depending on your model type (MLP, CNN, RNN) there may exist many parameters, but at the most basic level, these are the four building blocks of parameterized learning that you’ll commonly encounter.
Once we’ve defined these four key components, we can then apply optimization methods that allow
us to find a set of parameters W and b that minimize our loss function with respect to our scoring
function (while increasing classification accuracy on our data).
"""

#!pip install tensorflow
#!pip install scikit_learn

"""A computational graph is a way to formalize the structure of a set of computations, such as those involved in mapping inputs and parameters to outputs and loss."""

#!pip install pydot

from google.colab import drive
drive.mount('/content/gdrive', force_remount=False)

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, SimpleRNN
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.datasets import mnist

# load mnist dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# compute the number of labels
num_labels = len(np.unique(y_train))

# convert to one-hot vector
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# resize and normalize
image_size = x_train.shape[1]
x_train = np.reshape(x_train,[-1, image_size, image_size])
x_test = np.reshape(x_test,[-1, image_size, image_size])
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# network parameters
input_shape = (image_size, image_size)
batch_size = 128
units = 256
dropout = 0.2

# model is RNN with 256 units, input is 28-dim vector 28 timesteps
model = Sequential()
model.add(SimpleRNN(units=units,
                    dropout=dropout,
                    input_shape=input_shape))
model.add(Dense(num_labels))
model.add(Activation('softmax'))
model.summary()
# enable this if pydot can be installed
# pip install pydot
# We can also create a plot of the model for reference and save on the google drive for future reference.

#This requires that pydot and pygraphviz are installed in the local computer. 
#If this is a problem, you can comment out this line and the import statement for the plot_model() function

plot_model(model, to_file='/content/gdrive/MyDrive/Colab Notebooks/rnn-mnist.png', show_shapes=True)

# loss function for one-hot vector
# use of sgd optimizer
# accuracy is good metric for classification tasks

# For classification problem, we use categorical_crossentropy(multi class) / binary_crossentropy (two class)
model.compile(loss='categorical_crossentropy',
              optimizer='RMSprop',
              metrics=['accuracy'])
# train the network
model.fit(x_train, y_train, epochs=20, batch_size=batch_size)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)

print("\nTest accuracy: %.1f%%" % (100.0 * acc))

### RMSProp test acc is 97.4 ###

"""Learning Rate Schedulers

The concept of learning rate schedules, sometimes called learning
rate annealing or adaptive learning rates. By adjusting our learning rate on an epoch-to-epoch basis,
we can reduce loss, increase accuracy, and even in certain situations reduce the total amount of time
it takes to train a network.

Learning rates were kept constant in few previous experiments covered in the lab – we typically
set alpha = {0.1, 0.01, 0.001} and then train the network for a fixed number of epochs without changing
the learning rate. This method may work well in some situations, but it’s often beneficial to
decrease our learning rate over time and perform abalation experiments for your inference.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, SimpleRNN
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.datasets import mnist


# network parameters
input_shape = (image_size, image_size)
batch_size = 128
units = 256
dropout = 0.2

# model is RNN with 256 units, input is 28-dim vector 28 timesteps
model = Sequential()
model.add(SimpleRNN(units=units,
                    dropout=dropout,
                    input_shape=input_shape))
model.add(Dense(num_labels))
model.add(Activation('softmax'))
model.summary()

opt = RMSprop(learning_rate=0.1)
# For classification problem, we use categorical_crossentropy(multi class) / binary_crossentropy (two class)
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
# train the network
H = model.fit(x_train, y_train, validation_split=0.2, epochs=20, batch_size=batch_size)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)

print("\n Validation accuracy: %.1f" %(100.0 * np.mean(H.history["val_accuracy"])))
print("\nTest accuracy: %.1f%%" % (100.0 * acc))

#
# Validation accuracy: 9.9

# Test accuracy: 10.3%

opt = RMSprop(learning_rate=0.01)
# For classification problem, we use categorical_crossentropy(multi class) / binary_crossentropy (two class)
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
# train the network
H = model.fit(x_train, y_train, validation_split=0.2, epochs=20, batch_size=batch_size)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)

print("\n Validation accuracy: %.1f" %(100.0 * np.mean(H.history["val_accuracy"])))
print("\nTest accuracy: %.1f%%" % (100.0 * acc))

opt = RMSprop(learning_rate=0.001)
# For classification problem, we use categorical_crossentropy(multi class) / binary_crossentropy (two class)
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
# train the network
H = model.fit(x_train, y_train, validation_split=0.2, epochs=20, batch_size=batch_size)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)

print("\n Validation accuracy: %.1f" %(100.0 * np.mean(H.history["val_accuracy"])))
print("\nTest accuracy: %.1f%%" % (100.0 * acc))

from tensorflow.keras.optimizers import Adam

# model is RNN with 256 units, input is 28-dim vector 28 timesteps
model = Sequential()
model.add(SimpleRNN(units=units,
                    dropout=dropout,
                    input_shape=input_shape))
model.add(Dense(num_labels))
model.add(Activation('softmax'))
model.summary()

opt = Adam(learning_rate=0.001)
# For classification problem, we use categorical_crossentropy(multi class) / binary_crossentropy (two class)
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
# train the network
H = model.fit(x_train, y_train, validation_split=0.2, epochs=20, batch_size=batch_size)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)

print("\n Validation accuracy: %.1f" %(100.0 * np.mean(H.history["val_accuracy"])))
print("\nTest accuracy: %.1f%%" % (100.0 * acc))

"""# Task 1:

Perform validation split from the training data = 0.8 and validation data = 0.2 and then train the model with Adam optimizer with constant learning rates where lr=0.0001 and 0.01 and infer the test accuracy, validation accuracy and report it.

# Task 2:

Perform the above experiment with RNN with constant learning rate of 0.1 and 0.01 with SGD optimizer and report the test accuracy

MNIST - Hand written digit dataset, a hello world to the strategic learning experiments.    
where (“NIST” stands for National Institute of Standards and Technology while the “M” stands for “modified” as the data has been preprocessed to reduce any burden on computer vision processing and focus solely on the task of digit recognition) dataset is one of the most well studied datasets in the computer vision and machine learning literature. The goal of this dataset is to correctly classify the handwritten digits 0 − 9. Digits images are preprocessed and saved as grayscale images of dimension 28x28 resulting in a feature vector dimensionality of 784. In many cases, this dataset is a benchmark, a standard to which machine learning algorithms are ranked.
"""

####### Add your scripts for the constant learning rate ###########

#Standard decay in keras package
#While using SGD optimizer the decay parameter is associated with the optimizers.

# Lr (learning rate) = 0.01
# Decay = lr/decay_E
import numpy as np
decay_E = 40
Decay = 0.01/40
print(Decay)
batch_size = 128
print(60000/128)

# a time-based learning rate scheduler – it is controlled via the decay
# parameter of the optimizer classes (such as SGD)

#Therefore, a total of 469 weight updates need to be applied before an epoch completes
init_lr = 0.01
E=np.arange(0,20)
print(E)
iterations = 469
LR = []
for epoch in E:
  lr = init_lr*(1.0/(1.0+Decay*epoch*iterations))
  LR.append(lr)
print(LR)

LR_H =[]
Decay = 0.1 / 40

for epoch in E:
  lr = init_lr*(1.0/(1.0+Decay*epoch*iterations))
  LR_H.append(lr)
print(LR_H)

import matplotlib.pyplot as plt

plt.style.use("seaborn-white")
plt.rcParams['figure.figsize'] = (10.0, 10.0) # set default size of plots
plt.subplot(2, 1, 1)
plt.plot(np.arange(0, 20), LR, label="LR_0.01")
plt.plot(np.arange(0, 20), LR_H, label="LR_0.1")
plt.title('Learning rate parameterization')
plt.xlabel('Epochs')
plt.ylabel('LR')
plt.legend()
plt.grid(True)
plt.show()



import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, SimpleRNN
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.datasets import mnist

def step_decay(epoch):
    initial_alpha = 0.2
    factor = 0.25
    decayE = 5

    #
    alpha = initial_alpha*(factor**np.ceil((1+epoch)/decayE))
    print(epoch, alpha)
    return np.float(alpha)

# load mnist dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# compute the number of labels
num_labels = len(np.unique(y_train))

# convert to one-hot vector
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# resize and normalize
image_size = x_train.shape[1]
x_train = np.reshape(x_train,[-1, image_size, image_size])
x_test = np.reshape(x_test,[-1, image_size, image_size])
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# network parameters
input_shape = (image_size, image_size)
batch_size = 128
units = 256
dropout = 0.2

# model is RNN with 256 units, input is 28-dim vector 28 timesteps
model = Sequential()
model.add(SimpleRNN(units=units,
                    dropout=dropout,
                    input_shape=input_shape))
model.add(Dense(num_labels))
model.add(Activation('softmax'))
model.summary()


# loss function for one-hot vector
# use of sgd optimizer with step decay with learning rate scheduler that calculates lr and decreases it for every 5 epochs
# accuracy is good metric for classification tasks

callbacks = [LearningRateScheduler(step_decay)]

model.compile(loss='categorical_crossentropy',
              optimizer='SGD',
              metrics=['accuracy'])
# train the network
H=model.fit(x_train, y_train, epochs=20, batch_size=batch_size, callbacks=callbacks)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)
print("\nTest accuracy: %.1f%%" % (100.0 * acc))

import matplotlib.pyplot as plt
# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 20), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, 20), H.history["accuracy"], label="train_acc")

plt.title("Training Loss and Accuracy on MNIST")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()

"""#Task 3:
Perform the Learning rate scheduler experiment with validation data split = 0.2 and report the test and validation data accuracy.
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, SimpleRNN
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.datasets import mnist

def step_decay(epoch):
    initial_alpha = 0.01
    factor = 0.25
    decayE = 5

    #
    alpha = initial_alpha*(factor**np.ceil((1+epoch)/decayE))
    print(epoch, alpha)
    return np.float(alpha)

# load mnist dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# compute the number of labels
num_labels = len(np.unique(y_train))

# convert to one-hot vector
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# resize and normalize
image_size = x_train.shape[1]
x_train = np.reshape(x_train,[-1, image_size, image_size])
x_test = np.reshape(x_test,[-1, image_size, image_size])
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# network parameters
input_shape = (image_size, image_size)
batch_size = 128
units = 256
dropout = 0.2

# model is RNN with 256 units, input is 28-dim vector 28 timesteps
model = Sequential()
model.add(SimpleRNN(units=units,
                    dropout=dropout,
                    input_shape=input_shape))
model.add(Dense(num_labels))
model.add(Activation('softmax'))
model.summary()


# loss function for one-hot vector
# use of sgd optimizer with step decay with learning rate scheduler that calculates lr and decreases it for every 5 epochs
# accuracy is good metric for classification tasks

callbacks = [LearningRateScheduler(step_decay)]

model.compile(loss='categorical_crossentropy',
              optimizer='SGD',
              metrics=['accuracy'])
# train the network
H=model.fit(x_train, y_train, validation_split=0.2, epochs=20, batch_size=batch_size, callbacks=callbacks)

_, acc = model.evaluate(x_test,
                        y_test,
                        batch_size=batch_size,
                        verbose=0)
print("\nTest accuracy: %.1f%%" % (100.0 * acc))