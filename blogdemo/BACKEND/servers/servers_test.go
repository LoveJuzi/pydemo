package servers_test

import (
	"blog/models"
	"blog/servers"
	"fmt"
	"log"
	"os"
	"testing"

	"github.com/go-playground/assert/v2"
	"gorm.io/gorm"
)

func DropAllTables(db *gorm.DB) {
	// 获取数据库中的所有表名
	var tables []string
	rows, err := db.Raw("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'").Rows()
	if err != nil {
		log.Fatalf("could not get table names: %v", err)
	}
	defer rows.Close()

	// 收集所有表名
	for rows.Next() {
		var table string
		if err := rows.Scan(&table); err != nil {
			log.Fatalf("could not scan row: %v", err)
		}
		tables = append(tables, table)
	}

	// 删除每个表
	for _, table := range tables {
		// 使用 DROP TABLE 删除表
		if err := db.Exec(fmt.Sprintf("DROP TABLE IF EXISTS %s CASCADE", table)).Error; err != nil {
			log.Printf("could not drop table %s: %v", table, err)
		}
	}
}

func TestMain(m *testing.M) {
	models.ConnectDatabase("localhost", 5432, "postgres", "201381", "postgres_test", "disable")
	code := m.Run()
	DropAllTables(models.DB)
	os.Exit(code)
}

func TestCreateUser(t *testing.T) {
	testUser := &models.User{Name: "shengmh", Email: "123@123.com", Password: "123"}
	err := servers.CreateUser(testUser)
	assert.Equal(t, nil, err)
}

func TestGetUserId(t *testing.T) {
	if _, err := servers.GetUserId("123@123.com"); err != nil {
		assert.Equal(t, nil, err)
	}
	if _, err := servers.GetUserId("asdf"); err != nil {
		assert.Equal(t, nil, err)
	}
}

func TestCreatePost(t *testing.T) {
	uid, _ := servers.GetUserId("123@123.com")

	testPost := &models.Post{Title: "第一篇博客", Content: "ABCD", UserID: uid}
	if err := servers.CreatePost(testPost); err != nil {
		assert.Equal(t, nil, err)
	}
}

func TestGetPosts(t *testing.T) {
	var posts []models.Post
	if err := servers.GetPosts(&posts); err != nil {
		assert.Equal(t, nil, err)
	}
}
