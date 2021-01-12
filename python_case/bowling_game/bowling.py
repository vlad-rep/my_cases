"""
API для расчета готовой игры в боулинг (по простым правилам)
"""


class Bowling:
    def __init__(self, result):
        self.result = result
        self.total = 0
        self.analyzed_res = {}
        self.frames = 0

    def analyzing_result(self):
        self.result = self.result.upper()
        for _ in self.result:
            for i, k in enumerate(zip(self.result.replace('X', 'X-')[0::2],
                                      self.result.replace('X', 'X-')[1::2]), start=1):
                self.analyzed_res[i] = k
        for k, v in self.analyzed_res.items():
            self.frames += 1
            self.check_errors(v)
            self.result_count(v)
        if self.frames != 10:
            raise Exception('Не правильное количество фреймов!')
        return self.total

    def result_count(self, v):
        if 'X' in v:
            self.total += 20
        elif '/' in v:
            self.total += 15
        elif '-' in v:
            self.total += 0
        else:
            self.total += int(v[0]) + int(v[1])
        return v

    def check_errors(self, v):
        if '0' in v:
            raise ValueError('Введено неправильное значение')
        elif '/' in v[0]:
            raise ValueError('Spare на первом броске')
        elif 'X' in v[1]:
            raise ValueError('Strike на втором броске')
        elif self.total > 200:
            raise ValueError('Было превышено максимальное количесво очков')
        if v[0].isdigit() and v[1].isdigit() and int(v[0]) + int(v[1]) >= 10:
            raise ValueError('Введено неправильное значение, сумма одного фрейма больше 9 очков')
        if 'X' or '/' or '-' in v[0].isalpha() or v[1].isalpha():
            pass
        else:
            raise ValueError(
                'Введено неправильное значение, в результате присутсвуют символы, не являющиеся специальными(X, /, -)')
