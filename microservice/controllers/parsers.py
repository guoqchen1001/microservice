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
        'sheet_type',
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


class AuthParser:
    post = reqparse.RequestParser()
    post.add_argument(
        'user_no',
        type=str,
        location=['form'],
        required=True,
        help="未检测到参数：<user_no>"
    )
    post.add_argument(
        'password',
        type=str,
        location=['form'],
        required=True,
        help="未检测到参数：<password>"
    )

    auth = reqparse.RequestParser()
    auth.add_argument(
        "token",
        type=str,
        required=True,
        help="未检测到参数：<token>"
    )