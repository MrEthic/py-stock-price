from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import tensorflow.keras as keras


class BasePredictor:

    def __init__(
            self,
            data: pd.DataFrame,
            n_look_back: int,
            predict_n_last: int
    ):
        if not {'date', 'open', 'close', 'high', 'close', 'volume'}.issubset(set(data.columns)):
            raise ValueError(f'Incorrect DataFrame structure\n{data.columns}')

        if data['date'].dtype != np.datetime64:
            try:
                data["date"] = pd.to_datetime(data["date"], unit='ms')
            except Exception as e:
                raise ValueError("date columns can't by parsed as datetime")

        data.set_index('date')

        self._data = self._extract_features(data)
        self._n_look_back = n_look_back
        self._predict_n_last = predict_n_last

        self._training_set, self._test_set = self._split_sets()
        self._x_train, self._y_train = self._get_training()
        self._x_test, self._y_test = self._get_test()

        self._model: keras.Model = self._model()

    def __repr__(self):
        return f"n_look_back={self._n_look_back}, predict_last={self._predict_n_last}"

    @staticmethod
    def _standard_frac_scaler(df: pd.DataFrame) -> pd.DataFrame:
        df['frac_change'] = (df['close'] - df['open']) / df['open']
        df['frac_high'] = (df['high'] - df['open']) / df['open']
        df['frac_low'] = (df['low'] - df['open']) / df['open']
        return df

    def _split_sets(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split dataset in training and testing set

        :return: training and testing set
        """
        training_set = self._data[:-self._predict_n_last]
        test_set = self._data[-self._predict_n_last:]
        return training_set, test_set

    @abstractmethod
    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from a DataFrame

        :param df: DataFrame to extract features from
        :return: DataFrame with extracted features
        """
        pass

    @abstractmethod
    def _get_training(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Build the training set

        :return: a tuple as train_X, train_Y
        """
        pass

    @abstractmethod
    def _get_test(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Build the test set

        :return: a tuple as test_X, test_Y
        """
        pass

    @abstractmethod
    def _model(self, *args, **kwargs) -> keras.Model:
        """Build the model"""
        pass

    @property
    def model(self) -> pd.DataFrame:
        """
        Return model description

        :return: layer list
        """
        layers_info = []

        for layer in self._model.layers:
            layers_info.append(
                {
                    "Layer": f"{layer.name} ({layer.__class__.__name__})",
                    "Shape": f"{layer.output_shape}",
                    "# Params": layer.count_params()
                }
            )

        layers = pd.DataFrame(layers_info)
        layers.set_index('Layer', inplace=True)
        return layers

    @abstractmethod
    def fit(self, callbacks, *args, **kwargs) -> None:
        """Fit model"""
        pass

    @abstractmethod
    def predict(self) -> np.ndarray:
        """
        Predict model output on test set

        :return: predictions
        """
        pass

    @abstractmethod
    def evaluate(self) -> float:
        """
        Evaluate model performance

        :return: metric
        """

    @property
    @abstractmethod
    def predictions(self) -> pd.DataFrame:
        """
        Model predictions

        :return: Model predictions
        """
