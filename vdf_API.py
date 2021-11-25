from flask import Flask, request
from flask_cors import CORS, cross_origin
from traceback import format_exc
from secrets import token_bytes
from chiavdf import (
    create_discriminant,
    prove,
    verify_wesolowski,
)

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

CHALLENGE = token_bytes(10)
FORM_SIZE = 100 # Could be an input


@app.route('/create', methods=['POST','GET'])
@cross_origin()
def create():

    try:
        discriminant_size = int(request.json['discriminant_size'])
        discriminant = create_discriminant(
            CHALLENGE,
            discriminant_size
        )
        return {'Discriminant': discriminant}

    except Exception as error:
        return {'Error': str(error)}


@app.route('/eval', methods=['GET','POST'])
@cross_origin()
def eval():
    try:
        x = int(request.json['input']).to_bytes(FORM_SIZE, 'big')
        T = int(request.json['iterations'])
        discriminant_size = int(request.json['discriminant_size'])

        result  = prove(CHALLENGE, x, discriminant_size, T)
        y       = int.from_bytes(result[:FORM_SIZE], 'big')
        proof   = int.from_bytes(result[FORM_SIZE : 2 * FORM_SIZE], 'big')

        return {'output': y, 'proof': proof}

    except Exception as error:
        print(format_exc())
        return {'Error': str(error)}


@app.route('/verify', methods=['GET','POST'])
@cross_origin()
def verify():
    try:
        D   = str(request.json['discriminant'])
        x   = int(request.json['input']).to_bytes(FORM_SIZE, 'big')
        y   = int(request.json['output']).to_bytes(FORM_SIZE, 'big')
        pi  = int(request.json['proof']).to_bytes(FORM_SIZE, 'big')
        T   = int(request.json['iterations'])

        is_valid = verify_wesolowski(D, x, y, pi, T)

        return {'Valid': is_valid}

    except Exception as error:
        print(format_exc())
        return {'Error': str(error)}
    

if __name__ == '__main__':
    app.run()