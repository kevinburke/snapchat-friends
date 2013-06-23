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

func getFriendsById(id int) Users {
	var users Users
	db := getConnection()
	rows, err := db.Query("SELECT * FROM friends WHERE username = $1", id)
}

type UserNotFoundError struct {
	Message string
}
