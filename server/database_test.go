package main

import (
	"testing"
)

func TestGetUser(t *testing.T) {
	user, err := getUser("ekrubnivek")
	if err != nil {
		t.Error(err.Error())
	}
	if user.Score != 618 {
		t.Error("score ", user.Score, "does not match expected 618")
	}
}

//func TestDatabaseConnection(t *testing.T) {
//rows, err := db.Query("SELECT * FROM users WHERE username = 'ekrubnivek'")
//checkError(err)
//for rows.Next() {
//var id int
//var username string
//var score int
//err = rows.Scan(&id, &username, &score)
//checkError(err)
//fmt.Println(id)
//fmt.Println(score)
//}
//}
