package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
)

var server = "http://127.0.0.1:5000"

type discrResponse struct {
	Discriminant string `json:"discriminant"`
}

type proveResponse struct {
	Y     string `json:"output"`
	Proof string `json:"proof"`
}

type verifyResponse struct {
	IsValid bool `json:"valid"`
}

func main() {
	x := strconv.Itoa(50)
	lbda := 1024
	T := 1000000

	d := createDiscriminant(lbda)
	y, proof := prove(x, T, lbda)
	isV := verify(d, x, y, proof, T)

	fmt.Println("Pass:", isV)
}

// Creates a discriminant for binary quadratic forms
func createDiscriminant(discriminantSize int) string {

	postBody, _ := json.Marshal(map[string]string{
		"discriminant_size": strconv.Itoa(discriminantSize),
	})
	responseBody := bytes.NewBuffer(postBody)

	// Leverage Go's HTTP Post function to make request
	resp, err := http.Post(server+"/create", "application/json", responseBody)

	// Handle Error
	if err != nil {
		log.Fatalf("An Error Occured %v", err)
	}
	defer resp.Body.Close()

	// Read the response body
	decoder := json.NewDecoder(resp.Body)
	var s discrResponse
	err = decoder.Decode(&s)

	if err != nil {
		panic(err)
	}

	return s.Discriminant
}

func prove(x string, T, discriminantSize int) (string, string) {

	postBody, _ := json.Marshal(map[string]string{
		"input":             x,
		"iterations":        strconv.Itoa(T),
		"discriminant_size": strconv.Itoa(discriminantSize),
	})
	responseBody := bytes.NewBuffer(postBody)

	// Leverage Go's HTTP Post function to make request
	resp, err := http.Post(server+"/eval", "application/json", responseBody)

	// Handle Error
	if err != nil {
		log.Fatalf("An Error Occured %v", err)
	}
	defer resp.Body.Close()

	// Read the response body
	decoder := json.NewDecoder(resp.Body)
	var s proveResponse
	err = decoder.Decode(&s)

	if err != nil {
		panic(err)
	}

	// Should return two Integers
	return s.Y, s.Proof
}

// Y and Pi should be Integers
// but the numbers are too big.
func verify(d, x, y, pi string, T int) bool {

	postBody, _ := json.Marshal(map[string]string{
		"discriminant": d,
		"input":        x,
		"output":       y,
		"proof":        pi,
		"iterations":   strconv.Itoa(T),
	})
	responseBody := bytes.NewBuffer(postBody)

	// Leverage Go's HTTP Post function to make request
	resp, err := http.Post(server+"/verify", "application/json", responseBody)

	// Handle Error
	if err != nil {
		log.Fatalf("An Error Occured %v", err)
	}
	defer resp.Body.Close()

	// Read the response body
	decoder := json.NewDecoder(resp.Body)
	var s verifyResponse
	err = decoder.Decode(&s)

	if err != nil {
		panic(err)
	}

	return s.IsValid
}
