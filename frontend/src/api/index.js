import axios from 'axios'

/** axios 实例：自动携带 token，统一错误处理 */
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',
  timeout: 60000,
})

api.interceptors.request.use((config) => {
  const auth = JSON.parse(localStorage.getItem('auth') || '{}')
  if (auth.token) config.headers.Authorization = `Bearer ${auth.token}`
  return config
})

api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    // 登录失效统一跳回登录页
    if (err.response?.status === 401) {
      localStorage.removeItem('auth')
      if (window.location.pathname !== '/login') window.location.href = '/login'
    }
    const msg = err.response?.data?.detail || err.message || '请求失败'
    return Promise.reject(new Error(msg))
  },
)

// ---------- 认证 ----------
export const register = (username, password) => api.post('/api/auth/register', { username, password })
export const login = (username, password) => api.post('/api/auth/login', { username, password })

// ---------- 会话 ----------
export const getConversations = () => api.get('/api/conversations')
export const getMessages = (id) => api.get(`/api/conversations/${id}/messages`)
export const deleteConversation = (id) => api.delete(`/api/conversations/${id}`)

// ---------- 流式对话（SSE，用原生 fetch 读取流；支持 AbortSignal 停止生成） ----------
export function streamChat({ conversation_id, message, onToken, onDone, onError, signal }) {
  const auth = JSON.parse(localStorage.getItem('auth') || '{}')
  return fetch(`${api.defaults.baseURL}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${auth.token}`,
    },
    body: JSON.stringify({ conversation_id, message }),
    signal,
  })
    .then(async (res) => {
      if (!res.ok) {
        let detail = '对话失败'
        try {
          const data = await res.json()
          detail = data.detail || detail
        } catch { /* 忽略解析错误 */ }
        throw new Error(detail)
      }
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      for (;;) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop()
        for (const part of parts) {
          const line = part.trim()
          if (!line.startsWith('data:')) continue
          try {
            const event = JSON.parse(line.slice(5).trim())
            if (event.type === 'token') onToken?.(event.content)
            // 来源随 done 事件在回答结束后统一下发
            else if (event.type === 'done') onDone?.(event.conversation_id, event.sources || [])
          } catch { /* 跳过无法解析的事件 */ }
        }
      }
    })
    .catch((e) => {
      // 用户主动停止不算错误，不弹错误提示
      if (e.name !== 'AbortError') onError?.(e)
      throw e
    })
}

// ---------- 知识库管理（仅管理员） ----------
export const uploadDocument = (file, category) => {
  const form = new FormData()
  form.append('file', file)
  form.append('category', category)
  return api.post('/api/kb/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
}
export const getDocuments = () => api.get('/api/kb/documents')
export const getDocumentContent = (id) => api.get(`/api/kb/documents/${id}/content`)
export const updateDocument = (id, data) => api.put(`/api/kb/documents/${id}`, data)
export const deleteDocument = (id) => api.delete(`/api/kb/documents/${id}`)
