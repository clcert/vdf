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

# For det_size = 1024, form_size must be 100
# Specified on implementation of ChiaVDF
FORM_SIZE = 100

def get_serialized_input(x_hex: str) -> bytes:
    x_int = int(x_hex, 16)
    # The first \x08 is a standard for binary quadratic forms
    x = b"\x08" + x_int.to_bytes(FORM_SIZE - 1, 'big')
    return x


@app.route('/eval', methods=['POST'])
@cross_origin()
def eval():
    
    try:
        x    = get_serialized_input(request.json['input'])
        T    = int(request.json['iterations'])
        ds   = int(request.json['discriminant_size'])
        seed = bytes.fromhex(request.json['seed'])

        result  = prove(seed, x, ds, T)
        y       = result[:FORM_SIZE].hex()
        proof   = result[FORM_SIZE : 2 * FORM_SIZE].hex()

        return {'output': y, 'proof': proof}

    except Exception as error:
        print(format_exc())
        return {'Error': str(error)}


@app.route('/verify', methods=['POST'])
@cross_origin()
def verify():
    try:
        ds   = int(request.json['discriminant_size'])
        T    = int(request.json['iterations'])
        x    = get_serialized_input(request.json['input'])
        y    = bytes.fromhex(request.json['output'])
        pi   = bytes.fromhex(request.json['proof'])
        seed = bytes.fromhex(request.json['seed'])

        d = create_discriminant(seed, ds)

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