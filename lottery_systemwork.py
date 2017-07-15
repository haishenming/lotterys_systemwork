
from flask import Flask

from core.view import app



if __name__ == '__main__':

    app.config.from_object('config.setting')
    app.run(debug=True)
