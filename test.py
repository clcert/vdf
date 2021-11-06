from chiavdf import (
    create_discriminant,
    prove,
    verify_wesolowski,
)
from time import perf_counter
from secrets import token_bytes

discriminant_challenge = token_bytes(10)
discriminant_size = 512
form_size = 100
initial_el = b"\x08" + (b"\x00" * 99)
iters = 1000000

def test_prove_and_verify(
    discriminant_size, 
    discriminant_challenge,
    form_size,
    initial_el,
    iterations,
):
    
    discriminant = create_discriminant(discriminant_challenge, discriminant_size)
    
    t1 = perf_counter()
    result = prove(discriminant_challenge, initial_el, discriminant_size, iterations)
    t2 = perf_counter()

    print(f"Prove Time: {(t2 - t1)}")

    result_y = result[:form_size]
    proof = result[form_size : 2 * form_size]

    t3 = perf_counter()
    is_valid = verify_wesolowski(
        str(discriminant),
        initial_el,
        result_y,
        proof,
        iterations,
    )
    t4 = perf_counter()
    print(f"Verify Time: {(t4-t3)}")
    assert is_valid


test_prove_and_verify(
    discriminant_size, 
    discriminant_challenge, 
    form_size, 
    initial_el, 
    iterations
)