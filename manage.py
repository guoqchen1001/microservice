from flask_script import Manager, Server
from main import app, db, Order, OrderDetail

manager = Manager(app)
manager.add_command("server",Server)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,Order=Order, OrderDetail=OrderDetail)


if __name__ == "__main__":
    manager.run()

