<template>
  <div class="kb-page">
    <div class="kb-header">
      <div>
        <h2>知识库管理</h2>
        <p class="sub">上传 / 编辑 / 删除知识库文档，修改后即时生效（重新向量化）</p>
      </div>
      <el-button @click="$router.push('/')">← 返回对话</el-button>
    </div>

    <div class="kb-body">
      <!-- 上传区 -->
      <el-card shadow="never" class="upload-card">
        <template #header>上传文档</template>
        <div class="upload-row">
          <el-upload
            :show-file-list="false"
            :before-upload="handleUpload"
            accept=".md,.txt,.pdf"
          >
            <el-button type="primary" :loading="uploading">
              {{ uploading ? '上传解析中…' : '选择文件上传' }}
            </el-button>
          </el-upload>
          <el-select v-model="uploadCategory" style="width: 160px" placeholder="文档分类">
            <el-option label="技术栈" value="技术栈" />
            <el-option label="学习路线" value="学习路线" />
          </el-select>
          <el-text size="small" type="info">支持 .md / .txt / .pdf，上传后自动分块向量化</el-text>
        </div>
      </el-card>

      <!-- 文档列表 -->
      <el-card shadow="never">
        <template #header>
          文档列表（{{ total }} 篇 · 数据存于 ChromaDB 向量库）
        </template>
        <el-table :data="documents" v-loading="loading" stripe>
          <el-table-column prop="title" label="文档标题" min-width="200" show-overflow-tooltip />
          <el-table-column prop="category" label="分类" width="110">
            <template #default="{ row }">
              <el-tag :type="row.category === '学习路线' ? 'success' : 'primary'" size="small">
                {{ row.category }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="chunk_count" label="向量块数" width="100" align="center" />
          <el-table-column prop="updated_at" label="更新时间" width="170">
            <template #default="{ row }">{{ formatTime(row.updated_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
              <el-popconfirm
                title="删除后知识库将无法检索到此文档，确认删除？"
                confirm-button-text="删除"
                cancel-button-text="取消"
                @confirm="handleDelete(row)"
              >
                <template #reference>
                  <el-button link type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 编辑弹窗 -->
    <el-dialog
      v-model="editVisible"
      title="编辑文档（保存后重新向量化）"
      width="720px"
      :close-on-click-modal="false"
    >
      <el-form :model="editForm" label-position="top">
        <el-form-item label="标题">
          <el-input v-model="editForm.title" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="editForm.category" style="width: 200px">
            <el-option label="技术栈" value="技术栈" />
            <el-option label="学习路线" value="学习路线" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容（Markdown）">
          <el-input
            v-model="editForm.content"
            type="textarea"
            :rows="16"
            placeholder="请输入文档内容，支持 Markdown 格式"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存并重新向量化</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  deleteDocument,
  getDocumentContent,
  getDocuments,
  updateDocument,
  uploadDocument,
} from '../api'

const documents = ref([])
const loading = ref(false)
const uploading = ref(false)
const uploadCategory = ref('技术栈')

const editVisible = ref(false)
const saving = ref(false)
const editForm = reactive({ id: null, title: '', category: '技术栈', content: '' })

const total = ref(0)

onMounted(loadDocuments)

async function loadDocuments() {
  loading.value = true
  try {
    documents.value = await getDocuments()
    total.value = documents.value.length
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}

function formatTime(iso) {
  if (!iso) return '-'
  return iso.replace('T', ' ').slice(0, 19)
}

async function handleUpload(file) {
  uploading.value = true
  try {
    const res = await uploadDocument(file, uploadCategory.value)
    ElMessage.success(`「${res.title}」上传成功，共 ${res.chunk_count} 个向量块`)
    await loadDocuments()
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    uploading.value = false
  }
  return false // 阻止 el-upload 默认上传行为
}

async function openEdit(row) {
  try {
    const data = await getDocumentContent(row.id)
    editForm.id = data.id
    editForm.title = data.title
    editForm.category = data.category
    editForm.content = data.content
    editVisible.value = true
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleSave() {
  if (!editForm.title.trim() || !editForm.content.trim()) {
    ElMessage.warning('标题和内容不能为空')
    return
  }
  saving.value = true
  try {
    await updateDocument(editForm.id, {
      title: editForm.title,
      category: editForm.category,
      content: editForm.content,
    })
    ElMessage.success('更新成功，已重新向量化')
    editVisible.value = false
    await loadDocuments()
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    saving.value = false
  }
}

async function handleDelete(row) {
  try {
    await deleteDocument(row.id)
    ElMessage.success('删除成功')
    await loadDocuments()
  } catch (e) {
    ElMessage.error(e.message)
  }
}
</script>

<style scoped>
.kb-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 28px 40px;
}
.kb-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}
.kb-header h2 {
  margin: 0 0 4px;
  color: #1d3a5f;
}
.sub {
  margin: 0;
  font-size: 13px;
  color: #909399;
}
.kb-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 1100px;
}
.upload-row {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}
</style>
