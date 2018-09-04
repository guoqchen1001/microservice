from flask_script import Manager, Server
from microservice import create_app
from microservice.models import db, Order, OrderDetail, OrderBr, Supply


env = "microservice.config.{}Config".format("Dev")

app = create_app(env)
manager = Manager(app)
manager.add_command("server", Server)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db, Order=Order, OrderDetail=OrderDetail, OrderBr=OrderBr, Supply=Supply)

if __name__ == "__main__":
    manager.run()

