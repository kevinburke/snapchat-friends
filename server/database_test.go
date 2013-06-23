package main

import (
	"database/sql"
	"fmt"
	"github.com/bmizerany/pq"
	"github.com/kevinburke/go-toml"
	"testing"
)

func TestDatabaseConnection(t *testing.T) {
	config, err := toml.LoadFile("config.toml")
	checkError(err)
	configTree := config.Get("postgres").(*toml.TomlTree)
	user := configTree.Get("user").(string)
	password := configTree.Get("password").(string)
	host := configTree.Get("host").(string)
	port := configTree.Get("port").(int64)

	rawUrl := fmt.Sprintf(
		"postgres://%s:%s@%s:%d/snapchat",
		user, password, host, port,
	)
	url, err := pq.ParseURL(rawUrl)
	checkError(err)
	db, err := sql.Open("postgres", url)
	checkError(err)
	rows, err := db.Query("SELECT * FROM users WHERE username = 'ekrubnivek'")
	checkError(err)
	for rows.Next() {
		var id int
		var username string
		var score int
		err = rows.Scan(&id, &username, &score)
		checkError(err)
		fmt.Println(id)
		fmt.Println(score)
	}
}
