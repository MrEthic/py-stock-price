import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd

from .base import BasePredictor


class LSTMPredictor(BasePredictor):

    def __init__(self, data, n_look_back, predict_n_last: int):
        super().__init__(data, n_look_back, predict_n_last)

    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return super()._standard_frac_scaler(df)

    def _get_training(self) -> tuple[np.ndarray, np.ndarray]:
        x_train, y_train = [], []
        n = self._n_look_back
        training_set = self._training_set[['frac_change', 'frac_high', 'frac_low']].values
        for i in range(n, self._training_set.shape[0]):
            x_train.append(training_set[i - n:i])
            y_train.append(training_set[i, 0])

        x_train = np.array(x_train)
        y_train = np.array(y_train)

        return x_train, y_train

    def _get_test(self) -> tuple[np.ndarray, np.ndarray]:
        x_test, y_test = [], []
        n = self._n_look_back
        test_set = self._test_set[['frac_change', 'frac_high', 'frac_low']].values
        for i in range(n, self._test_set.shape[0]):
            x_test.append(test_set[i - n:i])
            y_test.append(test_set[i, 0])

        x_test = np.array(x_test)
        y_test = np.array(y_test)

        return x_test, y_test

    def _model(self, optimizer='adam', loss='mean_squared_error') -> keras.Model:
        model = keras.Sequential()
        model.add(
            layers.LSTM(
                100,
                return_sequences=False,
                input_shape=(self._x_train.shape[1], self._x_train.shape[2])
            )
        )
        # model.add(
        #     layers.LSTM(
        #         100,
        #         return_sequences=False
        #     )
        # )
        # model.add(layers.Dense(25))
        model.add(layers.Dense(1))

        model.compile(optimizer=optimizer, loss=loss)

        return model

    def fit(self, callbacks=None, batch_size=1, epochs=3) -> None:
        self._model.fit(self._x_train, self._y_train, batch_size=batch_size, epochs=epochs, callbacks=callbacks)

    def predict(self) -> np.ndarray:
        return self._model.predict(self._x_test)

    def predictions(self) -> pd.DataFrame:
        predictions = self._test_set.iloc[self._n_look_back:][['date', 'open', 'close', 'high', 'low', 'frac_change']]
        predictions['predicted_change'] = self.predict()
        predictions['predicted_close'] = (1 + predictions['predicted_change']) * predictions['open']
        return predictions

    def evaluate(self) -> float:
        return np.sqrt(np.mean(self.predictions['close'] - self.predictions['predicted_close']))


