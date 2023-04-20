from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def start_app():
    app.run(debug=True)


if __name__ == '__main__':

    # Start the Flask app after preprocessing is done
    start_app()
