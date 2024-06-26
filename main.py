from server import WebServer

app = WebServer("0.0.0.0", 9080)

@app.route('/hello')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/bye')
def hello_world():
    return "<p>Bye, World!</p>"

if __name__ == '__main__':
    app.serve()