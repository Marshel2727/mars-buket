from flask import jsonify

def success_response(data=None, message='Success', status_code=200):
    response = {
        'status': 'success',
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message='Error', status_code=400, data=None):
    response = {
        'status': 'error',
        'message': message,
        'data': data
    }
    return jsonify(response), status_code