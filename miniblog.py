#!/usr/bin/env python3

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    app.run(
        port=6070,
        debug=True
    )


