from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    print(request.json)

#run the app
if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")