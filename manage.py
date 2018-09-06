from flask_script import Manager, Server
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
    DynamicInoutDetail
)


env = "microservice.config.{}Config".format("Dev")

app = create_app(env)
manager = Manager(app)
manager.add_command("server", Server)

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
                Branch=Branch


                )


if __name__ == "__main__":
    manager.run()

