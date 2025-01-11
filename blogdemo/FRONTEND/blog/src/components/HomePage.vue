<template>
    <div>
        <h1>世界和平的博客</h1>
        <p>我的名字叫盛明辉</p>
        <ul>
            <li><a href="https://vuejs.org">Core Docs</a></li>
            <li><a href="https://forum.vuejs.org">Forum</a></li>
            <li><a href="https://chat.vuejs.org">Community Chat</a></li>
            <li><a href="https://twitter.com/vuejs">Twitter</a></li>
            <li><a href="https://news.vuejs.org">News</a></li>
        </ul>
        <ol>
            <li v-for="site in sites" :key="site.id">
                {{ site.name }}
            </li>
        </ol>
        <ul>
            <li v-for="user in users" :key="user.id">{{ user.name }}</li>
        </ul>
    </div>
</template>

<script>
import axios from "axios"

export default {
    name: "HomePage",
    data() {
        return {
            msg: '欢迎来到菜鸟教程！',
            sites: [
                { id: 1, name: 'Runoob' },
                { id: 2, name: 'Google' },
                { id: 3, name: 'Taobo' }
            ],
            users: [], // 用于存储后端返回的数据
        }
    },
    mounted() {
        // 在组件挂载时发送请求
        axios
            .get("https://jsonplaceholder.typicode.com/users")
            .then((response) => {
                this.users = response.data
            })
            .catch((error) => {
                console.error("Eorr fetching data:", error)
            })
    }
}
</script>

<style></style>
