package main

import (
        "fmt"
        "log"
        "net/http"
)

func helloWorldHandler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "Hello, World!")
}

func main() {
        http.HandleFunc("/", helloWorldHandler)

        fmt.Println("Server listening on port 8080...")
        log.Fatal(http.ListenAndServe(":8081", nil))
}

