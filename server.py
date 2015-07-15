from flask import Flask, request, render_template, json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html',events={})

@app.route('/events')
def addEvents():
    events = request.args.get('events')
    return render_template('login.html', events = json.dumps(events))

def main():
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
