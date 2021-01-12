# -*- coding: utf-8 -*-
"""
Расчет волатильности биржевых сделок с использованием многопоточности
"""
import os
import time

from multiprocessing import Process, Queue
from queue import Empty


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 6)
        print(f'Функция {func.__name__} работала {elapsed} секунд(ы)')
        return result

    return surrogate


class Volatility(Process):
    def __init__(self, file_name, volatility_share_list, zero_volatility_share_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.max_price = 0
        self.min_price = 0
        self.volatility = 0
        self.ticker_name = None
        self.zero_volatility_list = []
        self.total_volatility_dict = {}

        self.volatility_share_list = volatility_share_list
        self.zero_volatility_share_list = zero_volatility_share_list

    def pars_file(self):
        with open(self.file_name, 'r', encoding='UTF-8') as file_for_analyze:
            next(file_for_analyze)
            line = next(file_for_analyze)
            line = line.split(',')
            current_price = float(line[2])
            self.min_price = current_price
            self.max_price = current_price
            self.ticker_name = line[0]
            while True:
                line = next(file_for_analyze, None)
                if line is None:
                    break
                if len(line) == 0:
                    break
                line = line.split(',')
                current_price = float(line[2])
                if self.max_price <= current_price:
                    self.max_price = current_price
                if self.min_price >= current_price:
                    self.min_price = current_price

    def volatility_percent(self):
        half_sum = (self.max_price + self.min_price) / 2
        self.volatility = ((self.max_price - self.min_price) / half_sum) * 100

    def run(self):
        self.pars_file()
        self.volatility_percent()
        if self.volatility == 0.0:
            self.zero_volatility_list.append(self.ticker_name)
            self.zero_volatility_share_list.put(self.zero_volatility_list)
        else:
            self.total_volatility_dict[self.ticker_name] = self.volatility
            self.volatility_share_list.put(self.total_volatility_dict)


class DirectoryVolatilityInfo(Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zero_volatility = []
        self.total_volatility_dict = {}
        self.sort_volatility_dict = {}
        self.volatility_share_list = Queue()
        self.zero_volatility_share_list = Queue()
        self.volatility = 0
        self.ticker_name = ''
        self.data_volatility = {}

    def sorter_max(self):
        print('Максимальная волатильность: ')
        for i in dict(self.sort_volatility_dict[0:3]):
            print(i, '-', dict(self.sort_volatility_dict)[i], '%')

    def sorter_min(self):
        print('Минимальная волатильность:')
        for i in dict(self.sort_volatility_dict[-3:]):
            print(i, '-', dict(self.sort_volatility_dict)[i], '%')

    def sorter_zero_volatility(self):
        sort_zero_volatility = sorted(self.zero_volatility)
        print('Нулевая волатильность:', '\n', ', '.join(sort_zero_volatility))

    @time_track
    def run(self):
        for dir_path, dir_names, file_names in os.walk('trades'):
            volatility_share_list = Queue()
            zero_volatility_share_list = Queue()
            tickers = [Volatility(file_name=dir_path + '/' + ''.join(file_name),
                                  volatility_share_list=volatility_share_list,
                                  zero_volatility_share_list=zero_volatility_share_list) for file_name in file_names]
            for ticker in tickers:
                ticker.start()
            for ticker in tickers:
                ticker.join()
            while not volatility_share_list.empty():
                self.data_volatility.update(volatility_share_list.get())
            while not zero_volatility_share_list.empty():
                self.zero_volatility.extend(zero_volatility_share_list.get())
        self.sort_volatility_dict = sorted(self.data_volatility.items(), key=lambda x: x[1], reverse=True)
        self.sorter_max()
        self.sorter_min()
        self.sorter_zero_volatility()


if __name__ == '__main__':
    volatility_info = DirectoryVolatilityInfo()
    volatility_info.start()
    volatility_info.join()

