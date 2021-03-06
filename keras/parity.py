	
# Importing libraries
import numpy as np
import sys
import time
from random import randint
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.utils.vis_utils import plot_model

# ----- Script parameters ----- #
RESULT_SIZE = 8;						# Number of values showed
TRAINING_EPOCHS = 10;				# Number of epochs to train
BATCH_SIZE = 10;							# Number of training examples (Samples per training)
NUM_SAMPLES = 10000;				# Number of samples in arrays
EVALUATION_SAMPLES = 10000;	# Number of samples to evaluate

# ----- Functions ----- #
def show_values(num):
	sys.stdout.write("\n--------------------------------------------------------------------------------\n")
	sys.stdout.write("---------------------------------- Results -------------------------------------")
	sys.stdout.write("---------------------------------- Is Par? -------------------------------------")
	sys.stdout.write("\n--------------------------------------------------------------------------------\n")
	print("\tTraining values (A):")
	for i in range (num):
		sys.stdout.write("	%d" %a_array[i])
	sys.stdout.write("\n	-------------------------------------------------------\n")
	print("\tTraining solutions (C):")	
	for i in range(num):
		sys.stdout.write("	%d" %c_array[i])
	sys.stdout.write("\n	-------------------------------------------------------\n")
	print("\tPrediction values (X):")
	for i in range(num):
		sys.stdout.write("	%d" %x_array[i])
	sys.stdout.write("\n	-------------------------------------------------------\n")
	print("\tPrediction solutions:")
	for i in range(num):
		sys.stdout.write("	%d" %rounded_predictions[i])
	sys.stdout.write("\n")
	for i in range(num):
		sys.stdout.write("	%.2f" %predictions[i])
	sys.stdout.write("\n	-------------------------------------------------------\n")
	print("\tStatistics (error):")
	# Calcule error
	error = 0
	average_error = 0
	average_accuracy = 0
	for i in range (NUM_SAMPLES):
		if x_list[i]>=25:
			error = 1.00-predictions[i]
		else:
			error = predictions[i]
		average_error = average_error + error;
		if i < RESULT_SIZE:
			sys.stdout.write("	%.2f" %error)
	# Calcule and show averages
	average_error = (average_error/NUM_SAMPLES)
	average_accuracy = 1.00 - average_error
	sys.stdout.write("\n	Average error: %.2f" %average_error)
	sys.stdout.write("	Average accuracy: %.2f" %average_accuracy)
	sys.stdout.write("\n--------------------------------------------------------------------------------\n")
	sys.stdout.write("--------------------------------------------------------------------------------")
	sys.stdout.write("\n--------------------------------------------------------------------------------\n")


# ----- Main ----- #
# Preprocessing Data
a_list = []		# Input list A
b_list = []		# Input list B
c_list = []		# Knowledged output to train
x_list = []		# Input list X to predict

for i in range (NUM_SAMPLES):
	a_value = randint(0, 50)
	x_value = randint(0, 50)

	#if a_value<25:
	if a_value%2 == 1:
		c_value = 0	# Is impar
	else:
		c_value = 1	# Is par

	a_list.append(a_value)
	c_list.append(c_value)
	x_list.append(x_value)

a_array = np.array(a_list)
b_array = np.array(b_list)
c_array = np.array(c_list)
x_array = np.array(x_list)
		
scaler = MinMaxScaler(feature_range=(0,1))
scaled_a_samples = scaler.fit_transform((a_array).reshape(-1,1))
scaled_c_samples = scaler.fit_transform((c_array).reshape(-1,1))
scaled_x_samples = scaler.fit_transform((x_array).reshape(-1,1))

# Creating neural network
model = Sequential([
    Dense(12, input_shape=(1,), activation = 'relu'),		# input_shape=(1,) <=> input_dim=1
    Dense(8, activation = 'relu'),
		Dense(1, activation = 'sigmoid'),
])

model.summary()

# Plot neural network
#plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

# Training neural network
print("Training...")
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Batch size is the number of samples that will be propagated through the network every epoch.
model.fit(scaled_a_samples, scaled_c_samples, epochs=TRAINING_EPOCHS, batch_size=BATCH_SIZE, verbose=1)

# Predicting
print("Predicting...") # Probability
predictions = model.predict(scaled_x_samples, batch_size=BATCH_SIZE, verbose=0)

print("Rounded predictions...") # Binary result
rounded_predictions = model.predict_classes(scaled_x_samples, batch_size=BATCH_SIZE, verbose=0)

# Show results
show_values(RESULT_SIZE)

########## Evaluate trained model and show score
print("Evaluation: ")
score = model.evaluate(scaled_a_samples[:EVALUATION_SAMPLES], scaled_c_samples[:EVALUATION_SAMPLES], verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


