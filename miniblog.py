from app import create_app, db

app = create_app()


if __name__ == '__main__':
    app.run(
        port=5055,
        debug=True
    )


