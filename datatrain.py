from datamodel import *
import sys
import json
import numpy as np
from tqdm import tqdm
import tensorflow as tf




datafile = sys.argv[1]
weigthsfile = None
if(len(sys.argv)>2): weigthsfile = sys.argv[2]
f = open(datafile,'r')
data = json.load(f)

Tx = data['config']['Tx']
Ty = data['config']['Ty']
human_vocab = data['human']
machine_vocab = data['machine']
inv_machine = data['inv_machine']

X=[]
Y=[]
for d in tqdm(data['data']):
    X.append(d[0])
    Y.append(d[3])

m_train = int(0.9*len(X))
m_test = len(X) - m_train
#extract test values
X_test = X[m_train:]
X = X[:m_train]
Y_test = Y[m_train:]
Y = Y[:m_train]
m=m_train

X,Y,Xoh,Yoh = preprocess_data(X,Y,human_vocab,machine_vocab,Tx,Ty)
n_a = 32
n_s = 64


mw = ModelWrapper()

model = mw.create_model(Tx,Ty,n_a,n_s,len(human_vocab),len(machine_vocab))

if weigthsfile != None :
    model.load_weights(weigthsfile)

opt = tf.keras.optimizers.Adam(lr=0.005,beta_1=0.9,beta_2=0.999,decay=0.01)
model.compile(opt,loss='categorical_crossentropy',metrics=['accuracy'])


#initialize parameters
s0 = np.zeros((m,n_s))
c0 = np.zeros((m,n_s))

outputs = list(Yoh.swapaxes(0,1))

model.fit([Xoh,s0,c0],outputs,epochs=1,batch_size=100)

if weigthsfile == None : weigthsfile="dataweights.h5"

model.save_weights(weigthsfile)

X_test,Y_test,Xoh_test,Yoh_test = preprocess_data(X_test,Y_test,human_vocab,machine_vocab,Tx,Ty)
Yoh_test = list(Yoh_test.swapaxes(0,1))

s0 = np.zeros((m_test,n_s))
c0 = np.zeros((m_test,n_s))

model.evaluate([Xoh_test,s0,c0],Yoh_test)


model.save('datareadmodel.h5')


