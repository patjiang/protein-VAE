#!/usr/bin/env python

import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
from models import build_vae

# load data
maps = pickle.load(open("../results/maps.pkl", "rb"))
maps = maps.reshape(maps.shape[0], -1)

# scale data
scaler = MinMaxScaler()
maps_scale = scaler.fit_transform(maps)

# use 1/4 for testing
x_test = maps_scale[3::4]

# use 3/4 for training
x_train = np.delete(maps_scale, list(range(3, maps_scale.shape[0], 4)), axis=0)

# delete maps to spare some space
del maps, maps_scale

# set params
original_dim = x_train.shape[1]
batch_size = 64
latent_dim = 2
num_hidden_layer = 4
epochs = 200

# build VAE models #
encoder, decoder, vae = build_vae(original_dim, latent_dim, num_hidden_layer)

# train VAE
vae.fit(x=x_train, y=x_train,
        shuffle=True,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_test, x_test))

encoded = encoder.predict(x_train, batch_size=batch_size)
pickle.dump(encoded, open("../results/encoded.pkl", "wb"))

# save models
encoder.save_weights("../results/models/vae_encoder.h5")
decoder.save_weights("../results/models/vae_decoder.h5")

# save scaler
pickle.dump(scaler, open("../results/scaler.pkl", "wb"))
