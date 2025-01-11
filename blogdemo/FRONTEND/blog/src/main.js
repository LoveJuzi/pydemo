import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';

const app = createApp(App)

// 挂载插件或全局配置
app.use(router);
app.use(store);

// 挂载到dom
app.mount('#app')
