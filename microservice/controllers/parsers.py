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
    get.add_argument(
        'sheettype',
        type=str,
        location=['args', 'headers'],
        required=False,
        default='',
    )


class InoutParser:
    get = reqparse.RequestParser()
    get.add_argument(
        'page',
        type=int,
        location=['args', 'headers'],
        required=False,
        default=1,
    )

    get.add_argument(
        'brhno',
        type=str,
        location=['args', 'headers'],
        required=False,
        default=''
    )

    get.add_argument(
        'sheettype',
        type=str,
        location=['args', 'headers'],
        required=False,
        default='',
    )


class StockParser:
    get = reqparse.RequestParser()
    get.add_argument(
        'page',
        type=int,
        location=['args', 'headers'],
        required=False,
        default=1,
    )
    get.add_argument(
        'itemsubno',
        type=str,
        location=['args', 'headers'],
        required=False,
        default=''
    )


class UserParser:
    post = reqparse.RequestParser()
    post.add_argument(
        'userno',
        type=str,
        location=['form'],
        required=True,
        help="userno is required"
    )
    post.add_argument(
        'password',
        type=str,
        location=['form'],
        required=True,
        help="password is required"
    )
