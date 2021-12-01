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

FORM_SIZE = 100 # Could be an input


@app.route('/eval', methods=['GET','POST'])
@cross_origin()
def eval():
    
    try:
        # Apparently the first \x08 is necessary
        x = b"\x08" + int(request.json['input']).to_bytes(FORM_SIZE - 1, 'big')
        T = int(request.json['iterations'])
        ds = int(request.json['discriminant_size'])
        seed = bytes.fromhex(request.json['seed'])

        result  = prove(seed, x, ds, T)
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
        ds   = int(request.json['discriminant_size'])
        x   = b"\x08" + int(request.json['input']).to_bytes(FORM_SIZE-1, 'big')
        y   = int(request.json['output']).to_bytes(FORM_SIZE, 'big')
        pi  = int(request.json['proof']).to_bytes(FORM_SIZE, 'big')
        T   = int(request.json['iterations'])
        seed = bytes.fromhex(request.json['seed'])

        d = create_discriminant(
            seed, ds
        )

        is_valid = verify_wesolowski(str(d), x, y, pi, T)

        return {'valid': is_valid}

    except Exception as error:
        print(format_exc())
        return {'Error': str(error)}


# @app.route('/create', methods=['POST','GET'])
# @cross_origin()
def __create():

    try:
        discriminant_size = int(request.json['discriminant_size'])
        seed = bytearray.fromhex(request.json['seed'])
        discriminant = create_discriminant(
            seed,
            discriminant_size
        )
        return {'discriminant': discriminant}

    except Exception as error:
        return {'Error': str(error)}
    

if __name__ == '__main__':
    app.run()