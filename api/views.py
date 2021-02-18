from api import app
from flask import request, jsonify
from api import services


@app.route('/')
def index():
    return "Welcome to Dost platform"


@app.route('/api/v1/weebhook', methods=['POST'])
def webhook():
    try:
        if (request.json['contact'] and request.json['contact']['flow_category']):
            contact = request.json['contact']
            flow_category = contact['flow_category']
            print("exists")
            services.handle_registration(request.json)

    except IndexError:
        print("Failed to update")
    return 'Success'
