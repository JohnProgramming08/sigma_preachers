from project import create_app
from project.services import SignupService

if __name__ == "__main__":
    config = create_app()
    socket_io = config[0]
    app = config[1]
    with app.app_context():
        try:
            service = SignupService("MASTER", "MASTER")
            service.signup_user()
        except:
            pass
    socket_io.run(app, debug=True)
