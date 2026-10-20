<template>
  <div class="login-page">
    <div class="login-card">
      <div class="brand">
        <h1>IT技术栈知识库</h1>
        <p>技术栈解析 · 学习路线推荐 · RAG智能问答</p>
      </div>

      <el-tabs v-model="mode" stretch>
        <el-tab-pane label="登 录" name="login" />
        <el-tab-pane label="注 册" name="register" />
      </el-tabs>

      <el-form :model="form" :rules="rules" ref="formRef" label-position="top" @keyup.enter="submit">
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" placeholder="请输入账号" clearable />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item v-if="mode === 'register'" label="确认密码" prop="confirm">
          <el-input v-model="form.confirm" type="password" placeholder="请再次输入密码" show-password />
        </el-form-item>
        <el-button type="primary" size="large" class="submit-btn" :loading="loading" @click="submit">
          {{ mode === 'login' ? '登 录' : '注 册' }}
        </el-button>
      </el-form>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, register } from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const mode = ref('login')
const loading = ref(false)
const formRef = ref()
const form = reactive({ username: '', password: '', confirm: '' })

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 3, max: 50, message: '账号长度 3-50 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirm: [
    {
      validator: (_, value, cb) =>
        value === form.password ? cb() : cb(new Error('两次输入的密码不一致')),
      trigger: 'blur',
    },
  ],
}

async function submit() {
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  loading.value = true
  try {
    if (mode.value === 'login') {
      const data = await login(form.username, form.password)
      authStore.setAuth(data)
      ElMessage.success(`欢迎回来，${data.username}`)
    } else {
      await register(form.username, form.password)
      ElMessage.success('注册成功，请登录')
      mode.value = 'login'
      loading.value = false
      return
    }
    router.push('/')
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1d3a5f 0%, #2d6a9f 60%, #3fa7c8 100%);
}
.login-card {
  width: 420px;
  background: #fff;
  border-radius: 12px;
  padding: 36px 40px 24px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
}
.brand {
  text-align: center;
  margin-bottom: 20px;
}
.brand h1 {
  font-size: 24px;
  color: #1d3a5f;
  margin: 0 0 6px;
}
.brand p {
  font-size: 13px;
  color: #909399;
  margin: 0;
}
.submit-btn {
  width: 100%;
  margin-top: 4px;
}
</style>
