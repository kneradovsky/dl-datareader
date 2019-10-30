import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras import backend as K
import numpy as np


def softmax(x, axis=1):
    """Softmax activation function.
    # Arguments
        x : Tensor.
        axis: Integer, axis along which the softmax normalization is applied.
    # Returns
        Tensor, output of softmax transformation.
    # Raises
        ValueError: In case `dim(x) == 1`.
    """
    ndim = K.ndim(x)
    if ndim == 2:
        return K.softmax(x)
    elif ndim > 2:
        e = K.exp(x - K.max(x, axis=axis, keepdims=True))
        s = K.sum(e, axis=axis, keepdims=True)
        return e / s
    else:
        raise ValueError('Cannot apply softmax to a tensor that is 1D')




def string2int(s, length,vocab):
    s = s.lower()
    s=s.replace(',','')
    if len(s)>length:
        s=s[:length]
    
    rep = list(map(lambda x: vocab.get(x, vocab.get('<unk>')), s))

    if len(s)<length:
        rep += [vocab['<pad>']] * (length - len(s))
    return rep

def int2string(data,inv_vocab):
    s = [inv_vocab[i] for i in data if inv_vocab[i]!='<pad>']
    return "".join(s)

def preprocess_data(X,Y,human_vocab,machine_vocab,Tx,Ty):
    X = np.array([string2int(x,Tx,human_vocab) for x in X])
    Y = np.array([string2int(y,Ty,machine_vocab) for y in Y])
    Xoh = np.array(list(map(lambda x: tf.keras.utils.to_categorical(x,num_classes=len(human_vocab)),X)))
    Yoh = np.array(list(map(lambda y: tf.keras.utils.to_categorical(y,num_classes=len(machine_vocab)),Y)))
    return X,Y,Xoh,Yoh

def encode_strings(Ss,length,vocab):
    Ints = np.array([string2int(string,length,vocab) for string in Ss])
    OneHot = np.array(list(map(lambda x: tf.keras.utils.to_categorical(x,num_classes=len(vocab)),Ints)))
    return Ints,OneHot

def decode_onehots(OneHots):
    result = np.argmax(OneHots,axis=2)
    return result

def decode_strings(one_hots,inv_vocab):
    ints = decode_onehots(one_hots)
    result=[]
    for encoded in ints:
        result.append(int2string(encoded,inv_vocab))
    return result


class ModelWrapper: 

    repeator = None
    activator = layers.Activation(softmax,name='attention_weights')
    concatenator = layers.Concatenate(axis=-1)
    densor1 = layers.Dense(10,activation='tanh')
    densor2 = layers.Dense(1,activation='relu')
    dotor = layers.Dot(axes=1)
    post_activation_LSTM = None
    output_layer = None

    def one_step_attention(self,a,s_prev):
        s_prev = self.repeator(s_prev)
        concat = self.concatenator([a,s_prev])
        e = self.densor1(concat)
        energies = self.densor2(e)
        alphas = self.activator(energies)
        context = self.dotor([alphas,a])
        return context

    def create_model(self,Tx,Ty,n_a,n_s,human_vocab_size,machine_vocab_size):
        #create repeator layer
        self.repeator = layers.RepeatVector(Tx)
        self.post_activation_LSTM=layers.LSTM(n_s,return_state=True)
        self.output_layer = layers.Dense(machine_vocab_size,activation=softmax)

        X = layers.Input(shape=(Tx,human_vocab_size))
        s0 = layers.Input(shape=(n_s,),name='s0')
        c0 = layers.Input(shape=(n_s,),name='c0')
        s = s0
        c = c0

        outputs=[]

        a = layers.Bidirectional(layers.LSTM(n_a,return_sequences=True))(X)

        for i in range(Ty):
            context = self.one_step_attention(a,s)
            s, ss, c = self.post_activation_LSTM(context,initial_state=[s,c])
            output = self.output_layer(s)
            outputs.append(output)
        model = tf.keras.Model(inputs=[X,s0,c0],outputs=outputs)
        return model


