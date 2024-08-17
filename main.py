
from flask import Flask
from website import create_app
from website import connect_to_db,get_connection

app = create_app()

def main():
    app.run(debug=True)

if __name__ == '__main__': 
    main()
