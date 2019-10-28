from datamodel import *
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
import sys
import json
from random import randrange




datafile = sys.argv[1]
weigthsfile = None
if(len(sys.argv)>2): weigthsfile = sys.argv[2]
f = open(datafile,'r')
data = json.load(f)

Tx = data['config']['Tx']
Ty = data['config']['Ty']
human_vocab = data['human']
machine_vocab = data['machine']
inv_machine = {int(v):k for k,v in machine_vocab.items()}
inv_human = {int(v):k for k,v in human_vocab.items()}

X = []
for i in range(20):
    X.append(data['data'][randrange(0,1000)][0])

Xints,Xoh = encode_strings(X,Tx,human_vocab)

s0 = np.zeros((20,64))
c0 = np.zeros((20,64))

model = load_model('datareadmodel.h5')
#model.load_weights('model.h5')


Yoh = model.predict([Xoh,s0,c0])
Yoh = np.array(Yoh)
print(Yoh.shape)