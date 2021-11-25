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

func main() {
	d := createDiscriminant(1024)
	fmt.Println(d)
	// Produces RuntimeError: Deserializing compressed form failed
	// Error in Python prove function
	y, proof := prove(20, 1000000, 1024)
	fmt.Println(y, " ", proof)
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
	var d discrResponse
	err = decoder.Decode(&d)

	if err != nil {
		panic(err)
	}

	return d.Discriminant
}

func prove(x, T, discriminantSize int) (int, int) {

	postBody, _ := json.Marshal(map[string]string{
		"input":             strconv.Itoa(x),
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

	y, _ := strconv.Atoi(s.Y)
	p, _ := strconv.Atoi(s.Proof)

	return y, p
}
