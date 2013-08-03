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

type Friend struct {
	UserId   int
	Index    int
	FriendId int
}

type Friends struct {
	Friends []Friend
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

func getFriendsById(id int) Friends {
	var friends Friends
	db := getConnection()
	rows, err := db.Query("SELECT friend, index, \"user\" FROM friends WHERE \"user\" = $1", id)
	checkError(err)
	for rows.Next() {
		var f Friend
		err = rows.Scan(&f.UserId, &f.Index, &f.FriendId)
		checkError(err)
		friends.Friends = append(friends.Friends, f)
	}
	return friends
}

type UserNotFoundError struct {
	Message string
}
