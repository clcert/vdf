# VDF
On this repository I will explore proposals and implementations of Verifiable Delay Functions. 

A VDF takes time `T` in being evaluated, even with multiprocesing. The result is efficiently verifiable (poly *log `T`*). Is composed by 3 main algorithms.

- __Setup (λ,T) → pp__: Given a security parameter *λ* and difficulty time *T*, establish the public parameters to the correct functionality of VDF.

- __Eval (pp,x) → (y,π)__: Given an input *x* and the public parameters, makes a procesing that takes time *T*, producing an output *y* and a proof *π*, which one allows to verify the result quickly.

- __Verify (pp,x,y,π) → {Yes, No}__: Has the job of verify efficiently the result, returning *Yes* if *y* is the result of passing *x* as input to prove, with the same public parameters. Otherwise returns *No*.

Read wiki for more information
