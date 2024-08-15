from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
        return "första sidan heroku test jao"

if __name__ == '__main__':
    app.run()

