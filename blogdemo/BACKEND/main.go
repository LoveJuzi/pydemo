package main

import (
	"blog/models"
	"blog/routes"
)

func main() {
	models.ConnectDatabase()
	r := routes.SetupRouter()
	r.Run()
}

// package main
//
// import (
// 	"net/http"
//
// 	"github.com/gin-gonic/gin"
// )
//
// func main() {
// 	// 实例
// 	r := gin.Default()
// 	// 路由
// 	// 路由方法有 GET, POST, PUT, PATCH, DELETE 和 OPTIONS
// 	r.GET("/", func(c *gin.Context) {
// 		c.String(200, "Hello, Geektutu")
// 	})
// 	// 动态路由
// 	r.GET("/user/:name", func(c *gin.Context) {
// 		name := c.Param("name")
// 		c.String(http.StatusOK, "Hello %s", name)
// 	})
// 	// 获取Query参数
// 	r.GET("/users", func(c *gin.Context) {
// 		name := c.Query("name")                   // 获取 name 参数
// 		role := c.DefaultQuery("role", "teacher") // 设置默认参数
// 		c.String(http.StatusOK, "%s is a %s", name, role)
// 	})
// 	// 获取POST参数
// 	r.POST("/form", func(c *gin.Context) {
// 		username := c.PostForm("username")
// 		password := c.DefaultPostForm("password", "0000")
//
// 		c.JSON(http.StatusOK, gin.H{
// 			"username": username,
// 			"password": password,
// 		})
// 	})
// 	// Map参数
// 	r.POST("/post", func(c *gin.Context) {
// 		ids := c.QueryMap("ids")
// 		names := c.PostFormMap("names")
//
// 		c.JSON(http.StatusOK, gin.H{
// 			"ids":   ids,
// 			"names": names,
// 		})
// 	})
// 	// 重定向
// 	r.GET("/redirect", func(c *gin.Context) {
// 		// c.Redirect(http.StatusMovedPermanently, "/index")
// 		c.Redirect(http.StatusMovedPermanently, "/")
// 	})
// 	r.GET("/gohome", func(c *gin.Context) {
// 		c.Request.URL.Path = "/"
// 		r.HandleContext(c)
// 	})
// 	// 启动服务
// 	r.Run() // listen and serve on 0.0.0.0:8080
// }
