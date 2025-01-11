#!/bin/bash

#export GIN_MODE=release # 使用 gin 的 release 模式
#(go run main.go) &
#sleep 2

# echo "开始测试"

# echo "测试Map参数"
# curl -g "http://localhost:8080/post?ids[Jack]=001&ids[Tom]=002" -X POST -d 'names[a]=Sam&names[b]=David'
# echo

# echo "测试重定向"
# curl -i "http://localhost:8080/redirect"
# echo

# echo "测试重定向2"
# curl -i "http://localhost:8080/gohome"
# echo

curl -g "http://localhost:8080/posts"
