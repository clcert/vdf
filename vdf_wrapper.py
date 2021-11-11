from chiavdf import (
    create_discriminant,
    prove,
    verify_wesolowski,
)
from time import perf_counter, sleep
from secrets import token_bytes

CHALLENGE = token_bytes(10)
FORM_SIZE = 100

class PublicParameters:
 
    def __init__(self, it, size, discr):
        self.iterations = it
        self.discriminant_size = size
        self.discriminant = discr


# Setup (λ,T) → pp
def setup(lbda, T) -> PublicParameters:

    discriminant_size = lbda
    iterations = T

    discriminant = create_discriminant(
        CHALLENGE,
        discriminant_size
    )

    return PublicParameters(iterations, discriminant_size, discriminant)

# Eval (pp,x) → (y,π)
def eval(pp: PublicParameters, x) -> (int, int):

    result = prove(
        CHALLENGE,
        x,
        pp.discriminant_size, 
        pp.iterations
    )

    y = result[:FORM_SIZE]
    proof = result[FORM_SIZE : 2 * FORM_SIZE]

    return (y, proof)

# Verify (pp,x,y,π) → {True, False}:
def verify(pp, x, y, proof) -> bool:

    return verify_wesolowski(
        str(pp.discriminant),
        x,
        y,
        proof,
        pp.iterations,
    )


if __name__ == "__main__":
    pp = setup(1024, 10000000)
    x = b"\x08" + (b"\x00" * 99)
    y, proof = eval(pp, x)
    assert verify(pp, x, y, proof)
