import argparse
from collections import defaultdict
import random
from typing import List

import pandas as pd


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src_file",
        type=str,
        required=True,
        help="source csv e.g. https://era.library.ualberta.ca/items/dc3b9033-14d0-48d7-b6fa-6398a30e61e4 "
    )

    _args = parser.parse_args()
    return _args


# compoundword csv taken fro https://era.library.ualberta.ca/items/dc3b9033-14d0-48d7-b6fa-6398a30e61e4


class CompoundWordDB:

    def __init__(self, src_file: str, last_th: int=5, first_th=5):
        self._first_th = first_th
        self._last_th = last_th

        _df = pd.read_csv(src_file)
        
        self._first_dict = defaultdict(set)
        self._last_dict = defaultdict(set)

        for _first, _last in _df[["c1", "c2"]].values:
            self._first_dict[_first].add(_last)
            self._last_dict[_last].add(_first)

        # if number of prefix >= threshold, place in first_dict_th
        self._first_dict_th = dict()
        for prefix, suffix_list in self._first_dict.items():
            if len(suffix_list) >= first_th:
                self._first_dict_th.update({prefix: suffix_list})

        self._last_dict_th = dict()
        for suffix, prefix_list in self._last_dict.items():
            if len(prefix_list) >= last_th:
                self._last_dict_th.update({suffix: prefix_list})

    def common_start(self, word: str) -> List[str]:
        """
        Returns a list of compound words with the same first constituent as the word supplied
        """
        cs = self._first_dict.get(word, [])
        return [f"{word}{item}" for item in cs]

    def common_last(self, word: str) -> List[str]:
        """
        Returns a list of compound words with the same last constituent as the word supplied
        """
        cl = self._last_dict.get(word, [])
        return [f"{item}{word}" for item in cl]

    def common_last_quiz(self):
        """
        Returns a random word list, all can form respective compound words by
        having a common last word atached to them respectively
        """
        key = random.choice(list(self._last_dict_th.keys()))
        options = random.choices(list(self._last_dict_th[key]), k=self._last_th)
        return key, options

    def common_first_quiz(self):
        """
        Returns a random word list, all can form respective compound words by
        having a common first word attached to them respectively.
        """
        key = random.choice(list(self._first_dict_th.keys()))
        options = random.choices(list(self._first_dict_th[key]), k=self._first_th)
        return key, options


if __name__ == "__main__":
    args_ = _get_args()
    cw = CompoundWordDB(args_.src_file)
    import pdb; pdb.set_trace()
    pass
