# 需求列表

## 主页

构成：
- 标题
- 导航栏
- 文章列表

- 查看所有博客文章
- 查看单篇文章
- 创建新文章
- 更新文章
- 删除文章


## 前端如何访问后端的数据？

## GORM

这个库非常好用，可以自动创建表

## 创建 User 表

```go
type User struct {
	ID       uint   `gorm:"primaryKey"`
	Name     string `gorm:"not null"`
	Email    string `gorm:"unique;not null"`
	Password string `gorm:"not null"`
}
```

## 创建 Post 表

```go
type Post struct {
	ID      uint   `gorm:"primaryKey"`
	Title   string `gorm:"not null"`
	Content string `gorm:"type:text;not null"`
	UserID  uint   `gorm:"not null"`
	User    User   `gorm:"foreignKey:UserID"`
}
```