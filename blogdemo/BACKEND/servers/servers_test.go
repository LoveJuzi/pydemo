package servers_test

import (
	"blog/models"
	"blog/servers"
	"os"
	"testing"

	"github.com/go-playground/assert/v2"
)

func TestMain(m *testing.M) {
	models.ConnectDatabase("localhost", 5432, "postgres", "201381", "postgres_test", "disable")
	code := m.Run()
	models.DropAllTables(models.DB)
	os.Exit(code)
}

func TestCreateUser(t *testing.T) {
	testUser := &models.User{Name: "shengmh", Email: "123@123.com", Password: "123"}
	err := servers.CreateUser(testUser)
	assert.Equal(t, nil, err)
}

func TestGetUserId(t *testing.T) {
	if _, err := servers.GetUserId("123@123.com"); err != nil {
		TestCreateUser(t)
		TestGetUserId(t)
		return
	}

	if _, err := servers.GetUserId("123@123.com"); err != nil {
		assert.Equal(t, nil, err)
	}
	if _, err := servers.GetUserId("asdf"); err != nil {
		assert.Equal(t, err, err)
	}
}

func TestCreatePost(t *testing.T) {
	var uid uint
	var err error
	if uid, err = servers.GetUserId("123@123.com"); err != nil {
		TestCreateUser(t)
		TestCreatePost(t)
		return
	}

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
