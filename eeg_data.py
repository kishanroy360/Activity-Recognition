# -*- coding: utf-8 -*-
"""EEG_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10_qTH6wTIhxP_mAthfiAYEQqVrx76v1_
"""

!pip install -U -q kaggle
!mkdir -p ~/.kaggle



!cp kaggle.json ~/.kaggle/

!kaggle datasets list

!pip install -U -q PyDrive
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# 1. Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# choose a local (colab) directory to store the data.
local_download_path = os.path.expanduser('~/data')
try:
    os.makedirs(local_download_path)
except: pass

# 2. Auto-iterate using the query syntax
#    https://developers.google.com/drive/v2/web/search-parameters
file_list = drive.ListFile(
    {'q': "'1ecaoabJhaaIFFHSqdge93vZ78_Jn6U1D' in parents"}).GetList()

for f in file_list:
  # 3. Create & download by id.
    print('title: %s, id: %s' % (f['title'], f['id']))
    fname = os.path.join(local_download_path, f['title'])
    print('downloading to {}'.format(fname))
    f_ = drive.CreateFile({'id': f['id']})
    f_.GetContentFile(fname)


with open(fname, 'r') as f:
    print(f.read())

! ls ~/data
! pip install sklearn

import json
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv("~/data/eeg-data.csv")
# convert to arrays from strings
df['eeg_power'] = df.eeg_power.map(json.loads)
df

print(df.columns.values)
df = df.drop('Unnamed: 0', 1)
df = df.drop('indra_time', 1)
df = df.drop('browser_latency', 1)
df = df.drop('reading_time', 1)
df = df.drop('attention_esense', 1)
df = df.drop('meditation_esense', 1)
df = df.drop('raw_values', 1)
df = df.drop('signal_quality', 1)
df = df.drop('createdAt', 1)
df = df.drop('updatedAt', 1)
len(df.label.unique())

len(df.label.unique())

# separate eeg power to multiple columns
to_series = pd.Series(df['eeg_power']) # df to series
eeg_features=pd.DataFrame(to_series.tolist()) #series to list and then back to df
df = pd.concat([df,eeg_features], axis=1) # concatenate the create columns

df

# just look at first subject
df=df.loc[df['id'] == 1]

df = df.drop('eeg_power', 1) # drop comma separated cell
df = df.drop('id', 1) # drop comma separated cell
df

# prepare for training
label=df.pop("label") # pop off labels to new group
print(df.shape)
print(df.head())
# convert to np array. df has our featuers
df=df.values

# convert labels to onehots 
train_labels = pd.get_dummies(label)
# make np array
train_labels = train_labels.values
print(train_labels.shape)
len(train_labels[678])

## Here we start our code for the third experiment

## random imports
import pandas as pd 
import json
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import random

# a function to drop unwanted columns
def prepare_individual_data(df,individual):
	# drop unused features. just leave eeg_power and the label
    df = df.drop('Unnamed: 0', 1)
	# df = df.drop('id', 1)
    df = df.drop('indra_time', 1)
    df = df.drop('browser_latency', 1)
    df = df.drop('reading_time', 1)
    df = df.drop('attention_esense', 1)
    df = df.drop('meditation_esense', 1)
    df = df.drop('raw_values', 1)
    df = df.drop('signal_quality', 1)
    df = df.drop('createdAt', 1)
    df = df.drop('updatedAt', 1)
	# separate eeg power to multiple columns
    to_series = pd.Series(df['eeg_power']) # df to series
    eeg_features=pd.DataFrame(to_series.tolist()) #series to list and then back to df
    df = pd.concat([df,eeg_features], axis=1) # concatenate the create columns
	# df = pd.concat([df,eeg_features], axis=1, join='outer') # concatenate the create columns
	# just look at first subject
    df=df.loc[df['id'] == individual]
    df = df.drop('eeg_power', 1) # drop comma separated cell
	# df = df.drop('id', 1) # drop comma separated cell
    return df

df = pd.read_csv("~/data/eeg-data.csv")
relax = df[df.label == 'relax']
# df['label'] = df["label"].astype('category')
df['label'].value_counts()
df['eeg_power'] = df.eeg_power.map(json.loads)

individual_data=prepare_individual_data(df,1)

# this function cleans up individual data

def clean_labels(dd):
	# clean labels
	dd.loc[dd.label == 'math1', 'label'] = "math"
	dd.loc[dd.label == 'math2', 'label'] = "math"
	dd.loc[dd.label == 'math3', 'label'] = "math"
	dd.loc[dd.label == 'math4', 'label'] = "math"
	dd.loc[dd.label == 'math5', 'label'] = "math"
	dd.loc[dd.label == 'math6', 'label'] = "math"
	dd.loc[dd.label == 'math7', 'label'] = "math"
	dd.loc[dd.label == 'math8', 'label'] = "math"
	dd.loc[dd.label == 'math9', 'label'] = "math"
	dd.loc[dd.label == 'math10', 'label'] = "math"
	dd.loc[dd.label == 'math11', 'label'] = "math"
	dd.loc[dd.label == 'math12', 'label'] = "math"
	dd.loc[dd.label == 'colorRound1-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound1-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound2-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound3-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound4-6', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-1', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-2', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-3', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-4', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-5', 'label'] = "colors"
	dd.loc[dd.label == 'colorRound5-6', 'label'] = "colors"
	dd.loc[dd.label == 'readyRound1', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound2', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound3', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound4', 'label'] = "ready"
	dd.loc[dd.label == 'readyRound5', 'label'] = "ready"
	dd.loc[dd.label == 'blink1', 'label'] = "blink"
	dd.loc[dd.label == 'blink2', 'label'] = "blink"
	dd.loc[dd.label == 'blink3', 'label'] = "blink"
	dd.loc[dd.label == 'blink4', 'label'] = "blink"
	dd.loc[dd.label == 'blink5', 'label'] = "blink"
	dd.loc[dd.label == 'thinkOfItemsInstruction-ver1', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction2', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction1', 'label'] = "instruction"
	dd.loc[dd.label == 'colorInstruction2', 'label'] = "instruction"
	dd.loc[dd.label == 'musicInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'videoInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'mathInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'relaxInstruction', 'label'] = "instruction"
	dd.loc[dd.label == 'blinkInstruction', 'label'] = "instruction"
	return dd

cleaned_individual_data = clean_labels(individual_data)

cleaned_individual_data.head()

# this function drops unwanted labels from the data
def drop_useless_labels(df):
	# drop unlabeled and everyone paired and others. leave only relax and math. 
	df = df[df.label != 'unlabeled']
	df = df[df.label != 'everyone paired']
	df = df[df.label != 'instruction']
	df = df[df.label != 'blink']
	df = df[df.label != 'ready']
	df = df[df.label != 'colors']
	df = df[df.label != 'thinkOfItems-ver1']
	df = df[df.label != 'music']
	df = df[df.label != 'video-ver1']
	return df

final_individual_full_data= drop_useless_labels(cleaned_individual_data)

print(final_individual_full_data['label'].value_counts())

print(final_individual_full_data.head())

## Adding random gaussian noise to the data so that it can learn better representations. It is a form of regularization technique.
## this also increases the number of instances in the training set and hence gives us more examples with similar underlying 
## structure but different noise

for i in range(9):
	copy = final_individual_full_data
	copy[0]=copy[0]+random.gauss(1,.1) # add noice to mean freq var
	final_individual_full_data=final_individual_full_data.append(copy,ignore_index=True) # make voice df 2x as big
	print("shape of df after {0}th intertion of this loop is {1}".format(i,final_individual_full_data.shape))

## Preparing the data for training and testing
def get_traintest_data(individualdata):
	label=individualdata.pop("label") # pop off labels to new group
	train_labels = pd.get_dummies(label)
	train_labels = train_labels.values
	df=individualdata.values
	x_train,x_test,y_train,y_test = train_test_split(df,train_labels,test_size=0.2)
	#so now we have predictors and y values, separated into test and train
	x_train,x_test,y_train,y_test = np.array(x_train,dtype='float32'), np.array(x_test,dtype='float32'),np.array(y_train,dtype='float32'),np.array(y_test,dtype='float32')
	return x_train, x_test, y_train, y_test

x_train, x_test, y_train, y_test = get_traintest_data(final_individual_full_data)

## This function gives us a mini batch of 100 examples 
def get_mini_batch(x,y):
	rows=np.random.choice(x.shape[0], 100)
	return x[rows], y[rows]

def trainNN(x_train, y_train,x_test,y_test,number_trials):
    # there are 8 features
    # place holder for inputs. feed in later
    x = tf.placeholder(tf.float32, [None, x_train.shape[1]])
    # # # take 20 features  to 10 nodes in hidden layer
    w1 = tf.Variable(tf.random_normal([x_train.shape[1], 1000],stddev=.5,name='w1'))
    # # # add biases for each node
    b1 = tf.Variable(tf.zeros([1000]))
    # # calculate activations 
    hidden_output = tf.nn.softmax(tf.matmul(x, w1) + b1)
    w2 = tf.Variable(tf.random_normal([1000, y_train.shape[1]],stddev=.5,name='w2'))
    b2 = tf.Variable(tf.zeros([y_train.shape[1]]))
    # # placeholder for correct values 
    y_ = tf.placeholder("float", [None,y_train.shape[1]])
    # # #implement model. these are predicted ys
    y = tf.nn.softmax(tf.matmul(hidden_output, w2) + b2)
    # loss and optimization 
    loss = tf.reduce_mean(tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits = y, labels = y_, name='xentropy')))
    opt = tf.train.AdamOptimizer(learning_rate=.0005)
    train_step = opt.minimize(loss, var_list=[w1,b1,w2,b2])
    # start session
    sess = tf.Session()
    # init all vars
    init = tf.initialize_all_variables()
    sess.run(init)
    ntrials = number_trials
    iters = []
    loss_dict = []
    for i in range(ntrials):
        # get mini batch
        a,b=get_mini_batch(x_train,y_train)
        # run train step, feeding arrays of 100 rows each time
        _, cost =sess.run([train_step,loss], feed_dict={x: a, y_: b})
        if i%500 ==0:
            iters.append(i)
            loss_dict.append(cost)
            print("epoch is {0} and cost is {1}".format(i,cost)) 
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    acc_val = sess.run(accuracy, feed_dict={x: x_test, y_: y_test})
    print("test accuracy is {}".format(acc_val))
    ans = sess.run(y, feed_dict={x: x_test})
    print(y_test[0:3])
    print("Correct prediction\n",ans[0:3])
    return iters,loss_dict,acc_val

import matplotlib.pyplot as plt
# %matplotlib inline
iters, loss_dict, _ = trainNN(x_train,y_train,x_test,y_test,10000)

plt.figure(figsize=(20,10))
plt.plot(iters,loss_dict,label = "neural net")
plt.xlabel("Iterations")
plt.ylabel("Cross entropy loss")
plt.legend()
plt.show()



plt.figure(figsize=(20,10))
acc_list = []
for i in range(1,15):
    print('Training begins for {} individual'.format(i))
    df = pd.read_csv("~/data/eeg-data.csv")
    relax = df[df.label == 'relax']
    # df['label'] = df["label"].astype('category')
    df['label'].value_counts()
    df['eeg_power'] = df.eeg_power.map(json.loads)
    individual_data=prepare_individual_data(df,i)
    cleaned_individual_data = clean_labels(individual_data)
    final_individual_full_data= drop_useless_labels(cleaned_individual_data)
    for j in range(9):
	    copy = final_individual_full_data
	    copy[0]=copy[0]+random.gauss(1,.1) # add noice to mean freq var
	    final_individual_full_data=final_individual_full_data.append(copy,ignore_index=True) # make voice df 2x as big
	    print("shape of df after {0}th intertion of this loop is {1}".format(j,final_individual_full_data.shape))
    x_train, x_test, y_train, y_test = get_traintest_data(final_individual_full_data)
    iters, loss_dict, acc_val = trainNN(x_train,y_train,x_test,y_test,6000)
    print("The accuracy fot {} individual is: {}".format(i,acc_val))
    acc_list.append(acc_val)
    plt.plot(iters,loss_dict,label = str(i))
    
plt.legend()
plt.xlabel("Iterations")
plt.ylabel("Cross entropy loss")
plt.show()

plt.figure(figsize=(20,10))
plt.bar(list(range(1,15)),acc_list,color = 'orange')
plt.xlabel("Individual")
plt.ylabel("Accuracy")
plt.show()

for i in range(1,15):
    print('Accuracy of {} individual: {}'.format(i,acc_list[i-1]))

import numpy as np
print('Average accuracy for individuals is {}'.format(np.mean(acc_list)))

