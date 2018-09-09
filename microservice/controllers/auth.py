from flask_restful import abort,current_app,Resource
from .parsers import UserParser
from ..models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class AuthApi(Resource):
    """用户认证"""
    def post(self):
        args = UserParser.post.parse_args()
        user = User.query.get(args['userno'])
        if not user:
            abort(401, message="用户不存在或者密码错误")
        if not user.check_password(args["password"]):
            abort(401, message="用户名不存在或密码错误")

        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=600
        )

        return {'token': s.dumps({"userno": user.userno})}

