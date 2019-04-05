package main

import (
	"fmt"
	"gopkg.in/couchbase/gocb.v1"
)

type User struct {
	Id string `json:"uid"`
	Email string `json:"email"`
	Interests []string `json:"interests"`
}

func main() {
	cluster, _ := gocb.Connect("couchbase://localhost")
	cluster.Authenticate(gocb.PasswordAuthenticator{
	    Username: "USERNAME",
	    Password: "PASSWORD",
	})
	bucket, _ := cluster.OpenBucket("bucketname", "")

	bucket.Manager("", "").CreatePrimaryIndex("", true, false)

        bucket.Upsert("u:kingarthur",
                User{
                        Id: "kingarthur",
                        Email: "kingarthur@couchbase.com",
                        Interests: []string{"Holy Grail", "African Swallows"},
                }, 0)

        // Get the value back
        var inUser User
        bucket.Get("u:kingarthur", &inUser)
        fmt.Printf("User: %v\n", inUser)
}