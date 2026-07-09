from project import create_app
from project.services import PopulateService

if __name__ == "__main__":
    config = create_app()
    socket_io = config[0]
    app = config[1]
    with app.app_context():
        PopulateService.add_global_room()
        PopulateService.add_master()
        PopulateService.add_admin_message_types()
    socket_io.run(app, debug=True)
