# -*- coding: utf-8 -*-

import copy
import logging

log = logging.getLogger("qi.utils.rank")

DESC = 1
ASC = -1


def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""

    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


class Rank(object):
    def __init__(self):
        self.sort_columns = []
        self.DESC = 1
        self.ASC = -1

    def init(self):
        self.sort_columns = []

    def add_rank_column(self, name, order):
        if order == self.DESC or order == self.ASC:
            self.sort_columns.append({"name": name, "order": order})
        else:
            raise ValueError("invalid order value. set DESC(1) or ASC(0).")

    def _add_total_rank_prop(self, data):
        copied_data = copy.deepcopy(data)
        for item in copied_data:
            total = 0
            for column in self.sort_columns:
                total += item["{}_rank".format(column["name"])]

            item["total_rank"] = total
        return copied_data

    def _add_rank_prop(self, sorted_data, prep_name):
        rank = 1
        idx = 0
        copied_data = copy.deepcopy(sorted_data)
        try:
            while True:
                if (
                    idx > 0
                    and copied_data[idx - 1][prep_name] == copied_data[idx][prep_name]
                ):
                    copied_data[idx]["{}_rank".format(prep_name)] = copied_data[
                        idx - 1
                    ]["{}_rank".format(prep_name)]
                else:
                    copied_data[idx]["{}_rank".format(prep_name)] = rank
                idx += 1
                rank += 1
                if idx == len(copied_data):
                    break
        except (KeyError, IndexError) as e:
            log.warning("_add_rank_prop error. %s", e)
            return sorted_data
        return copied_data

    def get_rank(self, data):
        self.data = data
        for sort_item in self.sort_columns:
            order = sort_item["order"]

            def cmp_func(x, y):
                """ 정렬 비교 함수 
                항목 중 None 인 항목을 뒤로 보냄
                order 값이 DESC 인 경우
                None 인 항목은 값이 작은 것으로 간주
                order 값이 ASC 인 경우
                None 인 항목은 값이 큰 것으로 간주
                """
                if x is None and y is None:
                    return 0
                elif x is None:
                    if order == self.DESC:
                        return order
                    else:
                        return order * -1
                elif y is None:
                    if order == self.DESC:
                        return order * -1
                    else:
                        return order
                else:
                    if x > y:
                        return order * -1
                    elif x < y:
                        return order
                    else:
                        return 0

            def cmp(src, dest):
                return cmp_func(src[sort_item["name"]], dest[sort_item["name"]])

            sorted_data = sorted(self.data, key=cmp_to_key(cmp))
            self.data = self._add_rank_prop(sorted_data, sort_item["name"])

        res_data = self._add_total_rank_prop(self.data)
        self.data = sorted(res_data, key=lambda item: item["total_rank"])
        return self.data
