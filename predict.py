from PIL import Image
import tensorflow as tf
import tflib
import tflib.ops
import tflib.network
from tqdm import tqdm
import numpy as np
import data_loaders
import time
import os

BATCH_SIZE      = 20
EMB_DIM         = 80
ENC_DIM         = 256
DEC_DIM         = ENC_DIM*2
NUM_FEATS_START = 64
D               = NUM_FEATS_START*8
V               = 502
H               = 20
W               = 50


X = tf.placeholder(shape=(None,None,None,None),dtype=tf.float32) # difine shape parameter
mask = tf.placeholder(shape=(None,None),dtype=tf.int32)
seqs = tf.placeholder(shape=(None,None),dtype=tf.int32)
learn_rate = tf.placeholder(tf.float32)
input_seqs = seqs[:,:-1]
target_seqs = seqs[:,1:]
emb_seqs = tflib.ops.Embedding('Embedding',V,EMB_DIM,input_seqs)

ctx = tflib.network.im2latex_cnn(X,NUM_FEATS_START,True)
out,state = tflib.ops.im2latexAttention('AttLSTM',emb_seqs,ctx,EMB_DIM,ENC_DIM,DEC_DIM,D,H,W)
logits = tflib.ops.Linear('MLP.1',out,DEC_DIM,V)
predictions = tf.argmax(tf.nn.softmax(logits[:,-1]),axis=1)


loss = tf.reshape(tf.nn.sparse_softmax_cross_entropy_with_logits(
    tf.reshape(logits,[-1,V]),
    tf.reshape(seqs[:,1:],[-1])
    ), [tf.shape(X)[0], -1])

mask_mult = tf.to_float(mask[:,1:])
loss = tf.reduce_sum(loss*mask_mult)/tf.reduce_sum(mask_mult)

#train_step = tf.train.AdamOptimizer(1e-2).minimize(loss)
optimizer = tf.train.GradientDescentOptimizer(learn_rate)
gvs = optimizer.compute_gradients(loss)
capped_gvs = [(tf.clip_by_norm(grad, 5.), var) for grad, var in gvs]
train_step = optimizer.apply_gradients(capped_gvs)

def predict(imgName):
    imgs = []

    imgs.append(np.asarray(Image.open(imgName).convert('YCbCr'))[:,:,0][:,:,None])
    imgs = np.asarray(imgs,dtype=np.float32).transpose(0,3,1,2)
    inp_seqs = np.zeros((1,160)).astype('int32')
    print imgs.shape
    inp_seqs[:,0] = np.load('properties.npy').tolist()['char_to_idx']['#START'] # load vocabulary dict

    properties = np.load('properties.npy').tolist()
    idx_to_chars = lambda Y: ' '.join(map(lambda x: properties['idx_to_char'][x],Y))
    
    # training loops
    for i in xrange(1,160):
        inp_seqs[:,i] = sess.run(predictions,feed_dict={X:imgs,input_seqs:inp_seqs[:,:i]})

    np.save('pred_imgs',imgs)
    np.save('pred_latex',inp_seqs)
    print "Saved npy files! Use Predict.ipynb to view results"
    return inp_seqs


sess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=8))
init = tf.global_variables_initializer()

sess.run(init)
saver = tf.train.Saver()
saver.restore(sess,'./weights_best.ckpt')
