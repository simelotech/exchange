from flask_script import Manager
from flask_script.commands import Server, Shell, ShowUrls, Clean

from exchange_app import app

manager = Manager(app)
manager.add_command("shell", Shell())
manager.add_command("runserver", Server(use_reloader=True))
manager.add_command("show_urls", ShowUrls())
manager.add_command("clean", Clean())


if __name__ == "__main__":
    manager.run()
