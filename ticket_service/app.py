from flask import Flask
from ticket_service.service import ticket_service

def create_app():
    app = Flask(__name__)
    #app.config.from_pyfile(config_filename)

    app.register_blueprint(ticket_service, url_prefix='/api/tickets')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)