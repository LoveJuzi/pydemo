package servers

import "blog/models"

func CreateUser(user *models.User) error {
	return models.DB.Create(user).Error
}

func CreatePost(post *models.Post) error {
	return models.DB.Create(post).Error
}

func GetUserId(email string) (uint, error) {
	var user models.User
	if err := models.DB.Select("id").Where("email = ?", email).First(&user).Error; err != nil {
		return 0, nil
	}
	return user.ID, nil
}

func GetPosts(posts *[]models.Post) error {
	return models.DB.Preload("User").Find(&posts).Error
}
