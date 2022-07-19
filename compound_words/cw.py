import argparse
from collections import defaultdict
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

    def __init__(self, src_file):
        _df = pd.read_csv(src_file)
        
        self._first_dict = defaultdict(set)
        self._last_dict = defaultdict(set)

        for _first, _last in _df[["c1", "c2"]].values:
            self._first_dict[_first].add(_last)
            self._last_dict[_last].add(_first)

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


if __name__ == "__main__":
    args_ = _get_args()
    cw = CompoundWordDB(args_.src_file)
    import pdb; pdb.set_trace()
    pass
