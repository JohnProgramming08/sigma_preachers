from project import create_app

if __name__ == "__main__":
    config = create_app()
    socket_io = config[0]
    app = config[1]
    socket_io.run(app, debug=True)