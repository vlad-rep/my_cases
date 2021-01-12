# -*- coding: utf-8 -*-
import argparse

from bowling import Bowling

"""

"""
def run():

    parser = argparse.ArgumentParser()

    parser.add_argument('result', type=str, help='Результат игры из 10 фреймов')
    args = parser.parse_args()
    game_score_result = Bowling(args.result)
    print(f'В результате счета игры: {args.result}, вы набрали {game_score_result.analyzing_result()} очков!')


if __name__ == "__main__":
    run()
