package main

import ()

type User struct {
	Name  string
	Id    int
	Score int
}

type Users struct {
	Users []User
}

type Link struct {
	Source int
	Target int
}

type Links struct {
	Links []Link
}

func getUser(username string) (*User, error) {
	var u User
	db := getConnection()
	err := db.QueryRow("SELECT * FROM users WHERE username = $1", username).Scan(&u.Id, &u.Name, &u.Score)
	if err != nil {
		return &User{}, err
	} else {
		return &u, nil
	}
}

type UserNotFoundError struct {
	Message string
}
