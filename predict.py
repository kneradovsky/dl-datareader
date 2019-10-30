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

print(human_vocab)


X = []
for i in range(20):
    X.append(data['data'][randrange(0,1000)][0])

print(X)

Xints,Xoh = encode_strings(X,Tx,human_vocab)

s0 = np.zeros((20,64))
c0 = np.zeros((20,64))

n_a = 32
n_s = 64


mw = ModelWrapper()

#model = mw.create_model(Tx,Ty,n_a,n_s,len(human_vocab),len(machine_vocab))
#opt = tf.keras.optimizers.Adam(lr=0.005,beta_1=0.9,beta_2=0.999,decay=0.01)
#model.compile(opt,loss='categorical_crossentropy',metrics=['accuracy'])

model = load_model('datareadmodel.h5',custom_objects={'softmax':softmax})
model.summary()
#model.load_weights('model.h5')

Yoh = model.predict([Xoh,s0,c0])
Yoh = np.array(Yoh).swapaxes(0,1)
Ystrings = decode_strings(Yoh,inv_machine)

for i in range(len(X)):
    print("{}={}".format(X[i],Ystrings[i]))

#EXAMPLES = ['3 May 1979', '5 April 09', '21th of August 2016', 'Tue 10 Jul 2007', 'Saturday May 9 2018', 'March 3 2001', 'March 3rd 2001', '1 March 2001']
# for example in X:
    
#     source = string2int(example, Tx, human_vocab)
#     source = np.array(list(map(lambda x: to_categorical(x, num_classes=len(human_vocab)), source)))
#     sources=np.zeros((1,source.shape[0],source.shape[1]))
#     sources[0]=source
#     prediction = model.predict([sources, s0, c0])
#     prediction=np.array(prediction).swapaxes(1,0)
#     prediction = np.argmax(prediction, axis = 2)
   
#     output = [inv_machine[int(i)] for i in prediction[0]]
    
#     print("source:", example)
#     print("output:", ''.join(output))

