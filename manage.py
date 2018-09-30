import os

activate_this = os.getenv("WSGI_ALT_VIRTUALENV_ACTIVATE_THIS")
if activate_this:
    exec(open(activate_this, encoding='utf-8').read(), dict(__file__=activate_this))

from flask_script import Manager, Server
from flask_apidoc.commands import GenerateApiDoc
from microservice import create_app
from microservice.models import (
    db,
    Supply,
    Branch,
    OrderMaster,
    OrderDetail,
    OrderBr,
    BrDynamic,
    DynamicStock,
    DynamicInoutMaster,
    DynamicInoutDetail,
    User,
    BranchWareHouse
)

env = "microservice.config.{}Config".format("Dev")
app = create_app(env)


manager = Manager(app)
manager.add_command("server", Server)
manager.add_command("apidoc", GenerateApiDoc())


@manager.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                OrderMaster=OrderMaster,
                OrderDetail=OrderDetail,
                OrderBr=OrderBr,
                Supply=Supply,
                BrDynamic=BrDynamic,
                DynamicStock=DynamicStock,
                DynamicInoutMaster=DynamicInoutMaster,
                DynamicInoutDetail=DynamicInoutDetail,
                Branch=Branch,
                User=User,
                BranchWareHouse=BranchWareHouse
                )


if __name__ == "__main__":
    app = manager.app
    manager.run()

