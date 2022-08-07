# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import reqparse, Resource
from utils.rank import Rank


get_parser = reqparse.RequestParser()
get_parser.add_argument(
    "mc_max",
    dest="mc_max",
    type=int,
    default=None,
    location="args",
    required=False,
    help="max market capital",
)
get_parser.add_argument(
    "mc_min",
    dest="mc_min",
    type=int,
    default=None,
    location="args",
    required=False,
    help="min market capital",
)
get_parser.add_argument(
    "limit",
    dest="limit",
    type=int,
    location="args",
    default=20,
    help="item limit count",
)


class Stock(Resource):
    def __init__(self, **kwargs):
        self.dao = kwargs["dao"]

    def get(self, market, year):
        args = get_parser.parse_args()
        print(args)
        res_list = self.dao.get_stock_list(
            market, mc_min=args.mc_min, mc_max=args.mc_max
        )
        res_data = self._rank_process(res_list, year)
        return jsonify({"data": res_data[: args.limit]})

    def _rank_process(self, res_list, year):
        rank_list = []
        for item in res_list:
            try:
                for k, v in item["fr"].items():
                    if str(year) in k:
                        selected = v
                        break
                else:
                    # if year not in fr. except item
                    continue
            except KeyError:
                # if fr is not exists. except item
                continue

            rank_list.append(
                {
                    "code": item["code"],
                    "name": item["name"],
                    "market_cap": item["market_cap"],
                    "pbr": selected["pbr"],
                    "per": selected["per"],
                    "roa": selected["roa"],
                    "roe": selected["roe"],
                    "fr": item["fr"],
                }
            )

        rank = Rank()
        rank.add_rank_column("roa", rank.DESC)
        rank.add_rank_column("per", rank.ASC)
        res_data = rank.get_rank(rank_list)
        return res_data
