package main

import (
	"bufio"
	"fmt"
    "os"
)

func main() {
	// 创建一个读取器
	reader := bufio.NewReader(os.Stdin)

	// 打印提示信息
	fmt.Print("请输入您的名字: ")

	// 从用户输入读取名字
	name, _ := reader.ReadString('\n')

	// 输出问候语
	fmt.Printf("你好, %s欢迎使用 Go!\n", name)
}

