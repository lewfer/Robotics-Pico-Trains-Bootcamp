
# Flask app to present a web service and UI for the trains bootcamp

from flask import Flask, render_template, redirect, make_response, url_for
from flask import request, session, jsonify
from random import randint
from threading import Lock

rootDir = ""                              # local

lock = Lock()

app = Flask(__name__,
            template_folder=rootDir+'templates/',
            static_folder=rootDir+'static/')
            
# Not thread-safe, but should be ok in single-threaded developer Flask
data = {}
data['trains'] = {}

# Set the secret key so session encryption works
app.secret_key = b'A]qr>n@2XB"{B;CN'

# -------------------------------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------------------------------
def resetEverything():
    """Reset all the data"""
    global data

    lock.acquire()
    data = {}
    data['trains'] = {}
    lock.release()

def addTrain(id, name):
    """Add a new train"""
    lock.acquire()

    # Add to station's total
    if not id in data["trains"]:
        data["trains"][id] = {'name':name}
        print("Train ", id, "added")
    lock.release()

def reportTrain(id, location):
    """Report a train location"""
    lock.acquire()

    # Add to station's total
    if not id in data["trains"]:
        print("Unknown train at location {location}")
        data["trains"][id] = {'name':'unknown', 'location':location}
        print("Train location updated")
    else:
        print("Train {id} at location {location}")
        data["trains"][id]['location'] = location

    lock.release()

def getNextTrains(location):
    """Get next trains at specified location"""
    lock.acquire()
    
    lock.release()
    return [{'destination':'Airport', 'time':'10 mins'}, {'destination':'Airport', 'time':'20 mins'}]

def getNextAction(id):
    """Get next action for train with given id"""
    lock.acquire()
    
    lock.release()
    return "move_forward" # move_backward, stop

# -------------------------------------------------------------------------------------------------
# Route handlers
# -------------------------------------------------------------------------------------------------

@app.route('/add')
def add():
    """Add a new train"""

    print("add")

    # Get request arguments
    id = request.args.get('id')
    name = request.args.get('name')

    # Add train
    addTrain(id, name)

    # Return data in response
    return jsonify(data)

@app.route('/report')
def report():
    """Report a train location """

    print("report")

    # Get request arguments
    id = request.args.get('id')
    location = request.args.get('location')

    # Report location
    reportTrain(id, location)

    # Return data in response
    return jsonify(data["trains"][id])

@app.route('/info')
def info():
    """Get next trains"""

    # Get request arguments
    location = request.args.get('location')

    return jsonify(getNextTrains(location))

@app.route('/action')
def action():
    """Get next action for a train"""

    # Get request arguments
    id = request.args.get('id')

    return jsonify(getNextAction(id))

@app.route('/getdata')
def getdata():
    """Return all data"""

    print("data")

    # Return data in response
    return jsonify(data)

@app.route('/reset')
def reset():
    """Reset everything"""

    resetEverything()
    return jsonify(data)


# -------------------------------------------------------------------------------------------------
# Dashboard

@app.route('/')
def dashboard():
    """Show the dashboard, with charts"""
    return render_template('./dashboard.html', appData=data)



if __name__ == '__main__':
   #app.run(threaded=False, host="0.0.0.0", port=8000)
   app.run(threaded=True, host="0.0.0.0", port=8000)