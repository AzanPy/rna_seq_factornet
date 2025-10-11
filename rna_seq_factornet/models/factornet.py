# rna_seq_factornet/models/factornet.py
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class ExpressionFactorNet:
    """Minimal dense regressor for expression data.

    Expected input: X shape (n_samples, n_features)
    Provides: fit(X, y), predict(X), compute_gradients(X)
    """
    def __init__(self, input_dim: int, conv_filters=32, lstm_units=32,
                 dense_units=64, learning_rate=1e-3):
        inputs = keras.Input(shape=(input_dim,), name="expr")
        x = layers.Dense(dense_units, activation="relu")(inputs)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(1, activation="linear")(x)
        self.model = keras.Model(inputs, outputs, name="ExpressionFactorNet")
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate),
            loss="mse"
        )

    def fit(self, X, y, epochs=5, batch_size=32, verbose=0, validation_data=None):
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y, dtype=np.float32).reshape(-1, 1)
        return self.model.fit(
            X, y, epochs=epochs, batch_size=batch_size,
            verbose=verbose, validation_data=validation_data
        )

    def predict(self, X):
        X = np.asarray(X, dtype=np.float32)
        return self.model.predict(X, verbose=0).reshape(-1)

    def compute_gradients(self, X):
        """Gradient of model output w.r.t. inputs (per-sample)."""
        X = np.asarray(X, dtype=np.float32)
        Xtf = tf.convert_to_tensor(X)
        with tf.GradientTape() as tape:
            tape.watch(Xtf)
            y = self.model(Xtf, training=False)   # (batch, 1)
        grads = tape.gradient(y, Xtf)              # same shape as Xtf
        return grads.numpy()
