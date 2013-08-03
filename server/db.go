package main

import (
	"database/sql"
	"fmt"
	"github.com/bmizerany/pq"
	"github.com/kevinburke/go-toml"
)

func getConnection() *sql.DB {
	config, err := toml.LoadFile("config.toml")
	checkError(err)
	configTree := config.Get("postgres").(*toml.TomlTree)
	user := configTree.Get("user").(string)
	password := configTree.Get("password").(string)
	host := configTree.Get("host").(string)
	database := configTree.Get("database").(string)
	port := configTree.Get("port").(int64)

	rawUrl := fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s?sslmode=disable",
		user, password, host, port, database,
	)
	url, err := pq.ParseURL(rawUrl)
	checkError(err)
	db, err := sql.Open("postgres", url)
	checkError(err)
	return db
}
