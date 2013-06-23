package main

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
