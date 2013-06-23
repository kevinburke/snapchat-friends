package main

import (
	"encoding/json"
	"fmt"
	"github.com/hoisie/web"
	"html/template"
	"os"
)

func checkError(err error) {
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
		return
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
		ctx.NotFound("User not found")
		return ""
	}
	bytes, err := json.Marshal(user)
	checkError(err)
	return string(bytes)
}

func main() {
	web.Get("/users/(.*)", api)
	web.Get("/", homepage)
	web.Run("0.0.0.0:9999")
}
