package main

import (
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
	err = tpl.Execute(ctx)
}

func main() {
	web.Get("/", homepage)
	web.Run("0.0.0.0:9999")
}
