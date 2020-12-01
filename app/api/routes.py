from flask import Blueprint,request

api = Blueprint("api", __name__)


# JUST THE BEGINING
@api.route('/start', methods=['POST'])
def api_route():
    try:
        print(request.is_json)
        request_json = request.get_json()
        email = request_json.get('email')
        secret = request_json.get('secret')

        if email is None or secret is None:
            print('Something went wrong')
            return 'Wrong'
    except Exception as e:
        return f'{e}'
    return "Hello"
