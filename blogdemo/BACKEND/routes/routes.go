package routes

import (
	"blog/controllers"

	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	r := gin.Default()

	r.POST("/users", controllers.CreateUser)
	r.POST("/posts", controllers.CreatePost)
	r.GET("/posts", controllers.GetPosts)

	return r
}
