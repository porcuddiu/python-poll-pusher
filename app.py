from flask import Flask, render_template, request, jsonify, make_response
from dbsetup import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# configure pusher object
pusher = Pusher(
app_id='914821',
key='d6b0d5a2684738ecb338',
secret='2eaa262266db12b0c02a',
cluster='eu',
ssl=True)

database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()

def main():
    global conn, c

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = simplejson.loads(request.data)
    update_item(c, [data['member']])
    output = select_all_items(c, [data['member']])
    pusher.trigger(u'poll', u'vote', output)
    return request.data

if __name__ == '__main__':
    main()
    app.run(debug=True)
