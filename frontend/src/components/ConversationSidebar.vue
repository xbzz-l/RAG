<template>
  <div class="sidebar">
    <div class="sidebar-top">
      <div class="logo">
        <span class="logo-icon">IT</span>
        <span class="logo-text">技术栈知识库</span>
      </div>
      <el-button type="primary" size="large" class="new-btn" @click="$emit('new')">
        ＋ 新建对话
      </el-button>
      <!-- 知识库管理入口：仅管理员可见（普通用户界面上不存在该模块） -->
      <el-button
        v-if="authStore.isAdmin"
        class="kb-btn"
        size="large"
        @click="$router.push('/admin/kb')"
      >
        知识库管理
      </el-button>
    </div>

    <div class="conv-list">
      <div
        v-for="c in conversations"
        :key="c.id"
        class="conv-item"
        :class="{ active: c.id === currentConvId }"
        @click="$emit('select', c.id)"
      >
        <span class="conv-title">{{ c.title }}</span>
        <el-popconfirm
          title="删除该会话及其消息？"
          confirm-button-text="删除"
          cancel-button-text="取消"
          width="180"
          @confirm="$emit('remove', c.id)"
        >
          <template #reference>
            <span class="conv-del" @click.stop>×</span>
          </template>
        </el-popconfirm>
      </div>
      <el-empty v-if="!conversations.length" description="暂无对话" :image-size="60" />
    </div>

    <div class="sidebar-bottom">
      <div class="user-info">
        <span class="user-name">{{ authStore.username }}</span>
        <el-tag v-if="authStore.isAdmin" size="small" type="warning" effect="plain">管理员</el-tag>
      </div>
      <el-button text type="danger" size="small" @click="logout">退出登录</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

defineProps({
  conversations: { type: Array, default: () => [] },
  currentConvId: { type: Number, default: null },
})
defineEmits(['new', 'select', 'remove'])

const router = useRouter()
const authStore = useAuthStore()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100%;
  background: #1d3a5f;
  display: flex;
  flex-direction: column;
}
.sidebar-top {
  padding: 18px 14px 10px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}
.logo-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3fa7c8, #7fd1e8);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.logo-text {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}
.new-btn {
  width: 100%;
}
.kb-btn {
  width: 100%;
  margin: 8px 0 0 0;
  background: rgba(255, 255, 255, 0.12);
  border-color: transparent;
  color: #ffd666;
}
.kb-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffd666;
}
.conv-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px 10px;
}
.conv-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: 8px;
  color: #d3dce6;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s;
}
.conv-item:hover {
  background: rgba(255, 255, 255, 0.08);
}
.conv-item.active {
  background: rgba(63, 167, 200, 0.35);
  color: #fff;
}
.conv-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding-right: 6px;
}
.conv-del {
  color: #8aa0b8;
  font-size: 16px;
  line-height: 1;
  padding: 2px 4px;
  border-radius: 4px;
  visibility: hidden;
}
.conv-item:hover .conv-del {
  visibility: visible;
}
.conv-del:hover {
  color: #f56c6c;
}
.sidebar-bottom {
  padding: 12px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.user-name {
  color: #fff;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
