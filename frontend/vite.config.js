import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5199, // 固定端口，供一键启动脚本自动打开浏览器
    strictPort: true,
  },
})
