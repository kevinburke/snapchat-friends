package main

import (
	"encoding/json"
	"github.com/hoisie/web"
	"html/template"
	"log"
	"strconv"
)

func checkError(err error) {
	if err != nil {
		log.Fatalf(err.Error())
	}
}

func homepage(ctx *web.Context) {
	t := template.New("master")
	tpl, err := t.ParseFiles("templates/index.html")
	err = tpl.Execute(ctx, nil)
	checkError(err)
}

func api(ctx *web.Context, username string) string {
	user, err := getUser(username)
	ctx.SetHeader("Content-Type", "application/prs.kevinburke.snapchat-v1+json", true)
	if err != nil {
		checkError(err)
		ctx.NotFound("User not found")
		return ""
	}
	friends := getFriendsById(user.Id)
	for i := 0; i < len(friends.Friends); i++ {
		friend := friends.Friends[i]
		log.Print(strconv.Itoa(friend.UserId))
		log.Print(strconv.Itoa(friend.Index))
		log.Print(strconv.Itoa(friend.FriendId))
	}
	bytes, err := json.Marshal(user)
	checkError(err)
	return string(bytes)
}

func main() {
	log.Print("hello there")
	web.Get("/users/(.*)", api)
	web.Get("/", homepage)
	web.Run("0.0.0.0:9999")
}
