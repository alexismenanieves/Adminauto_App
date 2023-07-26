from application import app

if __name__ == '__main__':
    app.run(debug=False)
else:
    gunicorn_app = app