# VDF
On this repository I will explore proposals and implementations of Verifiable Delay Functions. 

A VDF takes time `T` in being evaluated, even with multiprocesing. The result is efficiently verifiable (poly *log `T`*). Is composed by 3 main algorithms.

- __Setup (λ,T) → pp__: Given a security parameter *λ* and difficulty time *T*, establish the public parameters to the correct functionality of VDF.

- __Eval (pp,x) → (y,π)__: Given an input *x* and the public parameters, makes a procesing that takes time *T*, producing an output *y* and a proof *π*, which one allows to verify the result quickly.

- __Verify (pp,x,y,π) → {Yes, No}__: Has the job of verify efficiently the result, returning *Yes* if *y* is the result of passing *x* as input to prove, with the same public parameters. Otherwise returns *No*.

## Chia VDF
Based on Wesoloski's proposal, has the following main algorithms:

- **Create Discriminant** (`create_discriminant`): This functions receives two inputs, a *challenge* and the *size* of discriminant to be created. After some computation, returns a valid __negative__ discriminant.
    - But, what does this function exactly? Internally it calls another function named `HashPrime`, which one receives the *challenge* as a *seed*, *size* as a *length*, and also another parameter more named *bitmask*, which is always the vector `{0,1,2, length-1}`. 
    - `HashPrime` generates a random psuedoprime using the hash and check method:
        - Randomly chooses x with bit-length *length*, then applies a mask
        - `(for b in *bitmask*) { x |= (1 << b) }`
        - Then return x if it is a psuedoprime, otherwise repeat.
    - Note that `HashPrime` returns a positive number, so it is mutiplied by *-1*.

- **Prove** (`prove`):

