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
	UserId   int // The user
	FriendId int // Their friend
	Rank     int // The friend rank
}

type Links struct {
	Links []Link
}

type Response struct {
	Links []Link `json:"links"`
	Users []User `json:"users"`
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

func getUserById(id int) (*User, error) {
	var u User
	db := getConnection()
	err := db.QueryRow("SELECT * FROM users WHERE id = $1", id).Scan(&u.Id, &u.Name, &u.Score)
	if err != nil {
		return &User{}, err
	} else {
		return &u, nil
	}
}

func getFriendsById(id int) (Friends, error) {
	var friends Friends
	db := getConnection()
	rows, err := db.Query("SELECT friend, index, \"user\" FROM friends WHERE \"user\" = $1", id)
	checkError(err)
	for rows.Next() {
		var f Friend
		err = rows.Scan(&f.UserId, &f.Index, &f.FriendId)
		if err != nil {
			return Friends{}, err
		}
		friends.Friends = append(friends.Friends, f)
	}
	return friends, nil
}

type UserNotFoundError struct {
	Message string
}
