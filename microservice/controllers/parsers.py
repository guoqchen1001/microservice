from flask_restful import reqparse


class OrderParse:
    get = reqparse.RequestParser()
    get.add_argument(
        'page',
        type=int,
        location=['args', 'headers'],
        required=False,
        default=1,
    )
    put = reqparse.RequestParser()
    put.add_argument(
        'sheetnos',
        type=list,
        location=['form', 'json'],
        required=True
     )

