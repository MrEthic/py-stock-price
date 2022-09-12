import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import train_test_split
from tqdm import tqdm


class HMMPredictor(object):
    def __init__(self, data, end_train_index,
                 n_hidden_states=4, n_latency_days=10,
                 n_steps_frac_change=50, n_steps_frac_high=10,
                 n_steps_frac_low=10):

        self._data = data
        self._end_train_index = end_train_index
        self.n_latency_days = n_latency_days

        self.hmm = GaussianHMM(n_components=n_hidden_states)

        self._compute_all_possible_outcomes(
            n_steps_frac_change, n_steps_frac_high, n_steps_frac_low)

    @staticmethod
    def _extract_features(data):
        open_price = np.array(data['open'])
        close_price = np.array(data['close'])
        high_price = np.array(data['high'])
        low_price = np.array(data['low'])

        frac_change = (close_price - open_price) / open_price
        frac_high = (high_price - open_price) / open_price
        frac_low = (open_price - low_price) / open_price

        return np.column_stack((frac_change, frac_high, frac_low))

    def fit(self):
        l, _ = self._data.shape
        feature_vector = HMMPredictor._extract_features(self._data.iloc[:-self._end_train_index])
        print(f"training on {feature_vector.shape}")

        self.hmm.fit(feature_vector)

    def _compute_all_possible_outcomes(self, n_steps_frac_change,
                                       n_steps_frac_high, n_steps_frac_low):
        frac_change_range = np.linspace(-0.1, 0.1, n_steps_frac_change)
        frac_high_range = np.linspace(0, 0.1, n_steps_frac_high)
        frac_low_range = np.linspace(0, 0.1, n_steps_frac_low)

        self._possible_outcomes = np.array(list(itertools.product(
            frac_change_range, frac_high_range, frac_low_range)))

    def _get_most_probable_outcome(self, day_index):
        previous_data_start_index = max(0, day_index - self.n_latency_days)
        previous_data_end_index = max(0, day_index - 1)
        previous_data = self._data.iloc[previous_data_start_index:previous_data_end_index]
        previous_data_features = HMMPredictor._extract_features(
            previous_data)

        outcome_score = []
        for possible_outcome in self._possible_outcomes:
            total_data = np.row_stack(
                (previous_data_features, possible_outcome))
            outcome_score.append(self.hmm.score(total_data))
        most_probable_outcome = self._possible_outcomes[np.argmax(
            outcome_score)]

        return most_probable_outcome

    def predict_close_price(self, day_index):
        open_price = self._data.iloc[day_index]['open']
        predicted_frac_change, predicted_frac_high, predicted_frac_low = self._get_most_probable_outcome(
            day_index)
        return open_price * (1 + predicted_frac_change)

    def predict(self, bar, with_plot=False):
        predicted_close_prices = []
        l, _ = self._data.shape

        for i, day_index in enumerate(range(l - self._end_train_index, l)):
            bar.progress((i + 1)/self._end_train_index)
            predicted_close_prices.append(self.predict_close_price(day_index))

        if with_plot:
            test_data = self._data.iloc[self._end_train_index:]
            days = np.array(test_data['open_time'], dtype="datetime64[ms]")
            actual_close_prices = test_data['close']

            fig = plt.figure()

            axes = fig.add_subplot(111)
            axes.plot(days, actual_close_prices, 'bo-', label="actual")
            axes.plot(days, predicted_close_prices, 'r+-', label="predicted")
            axes.set_title("Prediction")

            fig.autofmt_xdate()

            plt.legend()
            plt.show()

        return predicted_close_prices


# %%

# d = pd.read_csv(r'D:\Programation\Python\py-stock-price\src\datasources\data\BTCBUSD-DAILY.csv')
# stock_predictor = StockPredictor(d, 50)
# stock_predictor.fit()
# pred = stock_predictor.predict(with_plot=False)
#
# # %%
#
# stock_predictor.fit()
#
# # %%
# data = d.copy()
# test_data = data.iloc[-50:]
# days = np.array(test_data['open_time'], dtype="datetime64[ms]")
# days_all = np.array(data['open_time'], dtype="datetime64[ms]")
# actual_close_prices = data['close']
#
# fig = plt.figure(figsize=(25,20))
#
# axes = fig.add_subplot(111)
# axes.plot(days_all, actual_close_prices, 'b+-', label="actual")
# axes.plot(days, pred, 'r+-', label="predicted")
# axes.set_title("Prediction")
#
# fig.autofmt_xdate()
#
# plt.legend()
# plt.show()
