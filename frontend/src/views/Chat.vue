<template>
  <div class="chat-layout">
    <ConversationSidebar
      :conversations="conversations"
      :current-conv-id="currentConvId"
      @new="newConversation"
      @select="selectConversation"
      @remove="removeConversation"
    />

    <div class="chat-main">
      <!-- 会话标题栏 -->
      <div class="chat-header">
        <span class="chat-title">{{ currentTitle }}</span>
        <el-tag v-if="authStore.isAdmin" size="small" type="warning" effect="plain">管理员</el-tag>
      </div>

      <!-- 消息区 -->
      <div ref="messagesRef" class="chat-messages">
        <MessageItem v-for="(m, i) in messages" :key="i" :message="m" :streaming="streaming" />
        <!-- 欢迎引导 -->
        <div v-if="!messages.length" class="welcome">
          <h2>👋 你好，我是 IT技术栈知识库助手</h2>
          <p>我可以解答技术栈问题，也可以为你规划学习路线，全是干货。</p>
          <div class="examples">
            <div v-for="q in examples" :key="q" class="example-chip" @click="askExample(q)">
              {{ q }}
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="chat-input">
        <el-input
          v-model="input"
          type="textarea"
          :rows="3"
          resize="none"
          placeholder="输入你的问题，如：什么是Vue？ / 如何学习前端？"
          @keydown.enter.exact.prevent="send"
        />
        <div class="input-actions">
          <el-text size="small" type="info">Enter 发送 · 基于知识库检索回答</el-text>
          <div class="actions-right">
            <el-button v-if="streaming" type="danger" plain @click="stop">■ 停止生成</el-button>
            <el-button type="primary" :loading="streaming" @click="send">发 送</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import ConversationSidebar from '../components/ConversationSidebar.vue'
import MessageItem from '../components/MessageItem.vue'
import { deleteConversation, getConversations, getMessages, streamChat } from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const conversations = ref([])
const currentConvId = ref(null)
const messages = ref([])
const input = ref('')
const streaming = ref(false)
const messagesRef = ref()

const examples = ['什么是Vue？', '如何学习前端？', 'MySQL和Redis有什么区别？', 'Docker是干什么的？']

const currentTitle = computed(
  () => conversations.value.find((c) => c.id === currentConvId.value)?.title || '新对话',
)

onMounted(() => {
  authStore.restore()
  loadConversations()
})

async function loadConversations() {
  try {
    conversations.value = await getConversations()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

function newConversation() {
  currentConvId.value = null
  messages.value = []
  input.value = ''
}

async function selectConversation(id) {
  if (streaming.value) {
    ElMessage.warning('回答生成中，请稍候')
    return
  }
  currentConvId.value = id
  try {
    messages.value = await getMessages(id)
    scrollToBottom()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function removeConversation(id) {
  try {
    await deleteConversation(id)
    conversations.value = conversations.value.filter((c) => c.id !== id)
    if (currentConvId.value === id) newConversation()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

function scrollToBottom(force = false) {
  nextTick(() => {
    const el = messagesRef.value
    if (!el) return
    // 用户正在往上翻看时（离底部超过120px）不强制滚动，避免界面对抗
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 120
    if (force || nearBottom) el.scrollTop = el.scrollHeight
  })
}

function askExample(q) {
  input.value = q
  send()
}

const abortController = ref(null)

async function send() {
  const text = input.value.trim()
  if (!text || streaming.value) return
  input.value = ''

  // 用户消息上屏
  messages.value.push({ role: 'user', content: text })
  // 占位的 AI 回答（流式填充）；必须用 reactive，否则追加 token 不触发视图更新
  const assistantMsg = reactive({ role: 'assistant', content: '', sources: [] })
  messages.value.push(assistantMsg)
  streaming.value = true
  scrollToBottom(true)

  const controller = new AbortController()
  abortController.value = controller
  try {
    await streamChat({
      conversation_id: currentConvId.value,
      message: text,
      signal: controller.signal,
      onToken: (token) => {
        assistantMsg.content += token
        scrollToBottom()
      },
      onDone: (convId, sources) => {
        // 回答结束后统一展示来源
        assistantMsg.sources = sources
        // 首问时后端新建会话，返回会话ID
        if (!currentConvId.value) currentConvId.value = convId
        loadConversations()
      },
    })
  } catch (e) {
    if (e.name === 'AbortError') {
      // 用户主动停止：部分内容已生成，补停止标记
      if (assistantMsg.content) assistantMsg.content += '\n\n_（已停止生成）_'
    } else {
      if (!assistantMsg.content) assistantMsg.content = `请求失败：${e.message}`
      ElMessage.error(e.message)
    }
  } finally {
    abortController.value = null
    streaming.value = false
    scrollToBottom()
  }
}

/** 停止当前生成（中断 SSE 连接） */
function stop() {
  abortController.value?.abort()
}
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #f5f7fa;
}
.chat-header {
  height: 56px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 22px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
}
.chat-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 8px 22px;
}
.welcome {
  margin-top: 12vh;
  text-align: center;
  color: #606266;
}
.welcome h2 {
  font-size: 22px;
  color: #1d3a5f;
  margin-bottom: 10px;
}
.welcome p {
  font-size: 14px;
  margin-bottom: 20px;
}
.examples {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}
.example-chip {
  padding: 8px 16px;
  background: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 20px;
  font-size: 13px;
  color: #409eff;
  cursor: pointer;
  transition: all 0.15s;
}
.example-chip:hover {
  border-color: #409eff;
  background: #ecf5ff;
}
.chat-input {
  flex-shrink: 0;
  padding: 12px 22px 16px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
}
.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}
.actions-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
