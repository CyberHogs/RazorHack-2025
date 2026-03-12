package main

import (
	sqlite3 "github.com/mattn/go-sqlite3"

    "bufio"
	"database/sql"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	
)

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Print("Company Name: ")
	usr, err := reader.ReadString('\n')
    if err != nil { log.Fatal(err) }
    usr = strings.TrimSpace(usr)

    fmt.Print("License Key: ")
    key, err := reader.ReadString('\n')
    if err != nil { log.Fatal(err) }
    key = strings.TrimSpace(key)

	resp, err := http.Get("http://orlinab.pythonanywhere.com/db")
    if err != nil { log.Fatal(err) }
    defer resp.Body.Close()

	bytes, err := io.ReadAll(resp.Body)
    if err != nil { log.Fatal(err) }

	sqlite3conn := []*sqlite3.SQLiteConn{}
	sql.Register("hook", &sqlite3.SQLiteDriver {
		ConnectHook: func(conn *sqlite3.SQLiteConn) error {
			sqlite3conn = append(sqlite3conn, conn)
			conn.RegisterUpdateHook(func(op int, db string, table string, rowid int64) {
				log.Println("connected")
			})
			return nil
		},
	})

	db, err := sql.Open("hook", ":memory:")
	if err != nil { log.Fatal(err) }
	defer db.Close()
	db.Ping()

	err = sqlite3conn[0].Deserialize(bytes, "")
	if err != nil { log.Fatal(err) }

	rows, err := db.Query("select license_key from customer where company_name = ?", usr)
	if err != nil { log.Fatal(err) }
	defer rows.Close()

	if !rows.Next() {
		fmt.Printf("Company name '%s' not found.\n", usr)
		return;
	}
	
	var db_key string
	err = rows.Scan(&db_key)
	if err != nil { log.Fatal(err) }

	if key == db_key {
		fmt.Println("Yay! Did you know that the Spinosaurus are semiaquatic dinosaurs with tadpole-like tails?")
	} else {
		fmt.Println("Wrong License Key!")
	}
}
