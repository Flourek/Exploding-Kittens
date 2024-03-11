from app import create_app, io

app = create_app()

io.run(app, host='0.0.0.0', port=12101)