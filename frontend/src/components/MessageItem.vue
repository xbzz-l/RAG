<template>
  <!-- 用户消息：右侧气泡 -->
  <div v-if="message.role === 'user'" class="msg-user">
    <div class="bubble-user">{{ message.content }}</div>
  </div>

  <!-- AI回答：左侧，markdown 渲染 + 来源引用 -->
  <div v-else class="msg-assistant">
    <div class="avatar">AI</div>
    <div class="assistant-body">
      <div class="md-body" v-html="rendered" />
      <div v-if="message.sources && message.sources.length" class="sources">
        <span class="sources-label">知识来源：</span>
        <el-tag
          v-for="(s, i) in message.sources"
          :key="i"
          size="small"
          type="info"
          effect="plain"
          class="source-tag"
        >
          {{ s.title }}（{{ s.category }}）
        </el-tag>
      </div>
      <div v-if="streaming && !message.content" class="thinking">
        <span class="dots">
          <span class="dot" /><span class="dot" /><span class="dot" />
        </span>
        <span>正在检索知识库，本地模型生成中，请稍候…</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  message: { type: Object, required: true }, // { role, content, sources }
  streaming: { type: Boolean, default: false },
})

const md = new MarkdownIt({ html: false, breaks: true, linkify: true })

// 流式输出时每收到 token 重新渲染
const rendered = computed(() => md.render(props.message.content || ''))
</script>

<style scoped>
.msg-user {
  display: flex;
  justify-content: flex-end;
  margin: 14px 0;
}
.bubble-user {
  max-width: 70%;
  background: #409eff;
  color: #fff;
  padding: 10px 14px;
  border-radius: 10px 2px 10px 10px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
.msg-assistant {
  display: flex;
  gap: 10px;
  margin: 14px 0;
}
.avatar {
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: linear-gradient(135deg, #1d3a5f, #3fa7c8);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}
.assistant-body {
  max-width: calc(100% - 50px);
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 2px 10px 10px 10px;
  padding: 12px 16px;
}
.sources {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px dashed #e4e7ed;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}
.sources-label {
  font-size: 12px;
  color: #909399;
}
.source-tag {
  cursor: default;
}
.thinking {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #909399;
}
.dots {
  display: flex;
  gap: 4px;
}
.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #409eff;
  animation: bounce 1.2s infinite;
}
.dot:nth-child(2) {
  animation-delay: 0.2s;
}
.dot:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}
</style>
