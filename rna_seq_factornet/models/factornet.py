import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path

class ExpressionFactorNet:
    """Minimal dense regressor for expression data with a clean API."""

    def __init__(self, input_dim: int, dense_units: int = 64,
                 learning_rate: float = 1e-3, dropout_rate: float | None = 0.2, **_):
        inputs = keras.Input(shape=(input_dim,), name="expr")
        x = layers.Dense(dense_units, activation="relu")(inputs)
        if dropout_rate and dropout_rate > 0:
            x = layers.Dropout(dropout_rate)(x)
        outputs = layers.Dense(1, activation="linear")(x)
        self.model = keras.Model(inputs, outputs, name="ExpressionFactorNet")
        self.model.compile(optimizer=keras.optimizers.Adam(learning_rate), loss="mse")

    # ---- training/inference ----
    def fit(self, X, y, epochs=5, batch_size=32, verbose=0, validation_data=None):
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y, dtype=np.float32).reshape(-1, 1)
        return self.model.fit(X, y, epochs=epochs, batch_size=batch_size,
                              verbose=verbose, validation_data=validation_data)

    def predict(self, X):
        X = np.asarray(X, dtype=np.float32)
        return self.model.predict(X, verbose=0).reshape(-1)

    # ---- gradients for interpretation ----
    def compute_gradients(self, X):
        X = np.asarray(X, dtype=np.float32)
        Xtf = tf.convert_to_tensor(X)
        with tf.GradientTape() as tape:
            tape.watch(Xtf)
            y = self.model(Xtf, training=False)   # (batch, 1)
        grads = tape.gradient(y, Xtf)             # same shape as X
        return grads.numpy()

    # ---- save/load ----
    def save_model(self, path: str):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(path.as_posix(), include_optimizer=True, save_format="keras")

    def load_model(self, path: str):
        self.model = keras.models.load_model(path)
