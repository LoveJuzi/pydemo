package models

import (
	"fmt"
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

type User struct {
	ID       uint   `gorm:"primaryKey"`
	Name     string `gorm:"not null"`
	Email    string `gorm:"unique;not null"`
	Password string `gorm:"not null"`
}

type Post struct {
	ID      uint   `gorm:"primaryKey"`
	Title   string `gorm:"not null"`
	Content string `gorm:"type:text;not null"`
	UserID  uint   `gorm:"not null"`
	User    User   `gorm:"foreignKey:UserID"`
}

func ConnectDatabase(host string, port int, user string, password string, dbname string, sslmode string) {
	// "host=localhost port=5432 user=postgres password=201381 dbname=postgres sslmode=disable"
	dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		host, port, user, password, dbname, sslmode)
	database, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	database.AutoMigrate(&User{}, &Post{})

	DB = database
}
