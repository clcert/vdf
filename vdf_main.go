package main

import (
	"fmt"
	"math/big"

	"github.com/clcert/vdf/govdf"
)

func main() {
	x := big.NewInt(50)
	seed := govdf.GetRandomSeed()
	govdf.SetServer("http://127.0.0.1:5000/")

	lbda := 1024
	T := 1000000

	y, proof := govdf.Eval(*x, T, lbda, seed)
	isV := govdf.Verify(*x, y, proof, T, lbda, seed)

	fmt.Println("Pass:", isV)
}
