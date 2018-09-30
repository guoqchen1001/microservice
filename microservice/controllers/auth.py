from flask_restful import abort,current_app,Resource
from functools import wraps
from .parsers import AuthParser
from ..models import User
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer
                          , BadSignature, SignatureExpired)
from .base import ErrorCode


class AuthApi(Resource):
    """用户认证"""
    def post(self):
        """
           @api {post}  /api/auth  获取令牌
           @apiVersion 1.0.0
           @apiName  auth
           @apiGroup 安全校验
           @apiParam {string}  user_no   （必须）  用户名
           @apiParam {string}  password  （必须）  密码

           @apiSuccess (回参) {string} Token 令牌
           @apiSuccessExample {json} Success-Response:
           {
               "Token": "1234567890"
           }
           @apiUse UserNotFoundError

        """
        args = AuthParser.post.parse_args()
        user = User.query.get(args['user_no'])
        if not user:
            abort(400, message="用户名不存在或者密码错误", code=ErrorCode.user_not_found.value)
        if not user.check_password(args["password"]):
            abort(400, message="用户名不存在或密码错误", code=ErrorCode.user_not_found.value)

        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=current_app.config['TOKEN_EXPIRES_IN'] or 600
        )

        return {'Token': s.dumps({"user_no": user.user_no})}

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def _warpper(*args, **kwargs):
            r_args = AuthParser.auth.parse_args()
            token = r_args['Token']
            
            if not token:
                abort(400, message="未检测到token", code=ErrorCode.signature_required.value)

            user_no = ""  # 用户编码

            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
                user_no = data['user_no']
            except SignatureExpired:
                abort(403, message="token已过期", code=ErrorCode.signature_expired.value)
            except BadSignature:
                abort(401, message="token不合法", code=ErrorCode.signature_required.value)

            user = User.query.get(user_no)

            if not user:
                abort(400, message="用户{}不存在".format(user_no), code=ErrorCode.user_not_found.value)
            if not user.isvalid():
                abort(400, message="用户{}无权限，请联系管理员开通".format(user_no), code=ErrorCode.permission_not_allowed.value)

            kwargs.update({'user': user})
            return func(*args, **kwargs)

        return _warpper




