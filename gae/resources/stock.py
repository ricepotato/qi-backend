# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource


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
            market, mc_min=args.mc_min, mc_max=args.mc_max, limit=args.limit
        )
        return jsonify({"data": res_list})
