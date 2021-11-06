# VDF
On this repository I will explore proposals and implementations of Verifiable Delay Functions

## Chia VDF
Based on Wesoloski's proposal, has the following main algorithms:

- **Create Discriminant** (`create_discriminant`): This functions receives two inputs, a *challenge* and the *size* of discriminant to be created. After some computation, returns a valid __negative__ discriminant.
    - But, what does this function exactly? Internally it calls another function named `HashPrime`, which one receives the *challenge* as a *seed*, *size* as a *length*, and also another parameter more named *bitmask*, which is always the vector `{0,1,2, length-1}`. 
    - `HashPrime` generates a random psuedoprime using the hash and check method:
        - Randomly chooses x with bit-length `length`, then applies a mask
        - (for b in *bitmask*) { x |= (1 << b) }.
        - Then return x if it is a psuedoprime, otherwise repeat.
    - Note that `HashPrime` returns a positive number, so it is mutiplied by *-1*.

- **Prove** (`prove`):

