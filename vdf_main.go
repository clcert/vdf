package main

import (
	"encoding/hex"
	"fmt"

	"github.com/clcert/vdf/govdf"
)

func main() {
	s := "23"
	x, err := hex.DecodeString(s)
	if err != nil {
		panic(err)
	}

	seed := govdf.GetRandomSeed()
	govdf.SetServer("http://127.0.0.1:5000/")

	lbda := 1024
	T := 1000000

	y, proof := govdf.Eval(T, lbda, x, seed)
	isV := govdf.Verify(x, y, proof, seed, T, lbda)

	fmt.Println("Pass:", isV)
}
