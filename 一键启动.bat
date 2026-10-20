@echo off
title IT技术栈知识库 - 智能一键启动
cd /d "%~dp0"

echo ==============================================
echo    IT技术栈知识库 智能一键启动
echo    首次运行会自动安装全部依赖，请耐心等待
echo ==============================================
echo.

echo [检查] 基础环境（Python / Node.js）...
where python >nul 2>&1 || (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+：https://www.python.org/downloads/
    pause
    exit /b 1
)
where node >nul 2>&1 || (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+：https://nodejs.org/
    pause
    exit /b 1
)

echo [检查] Ollama 服务...
curl -s --max-time 2 http://127.0.0.1:11434/api/tags >nul 2>&1 || (
    echo [错误] Ollama 未运行：请先安装并打开 Ollama 桌面应用 https://ollama.com/
    pause
    exit /b 1
)

echo [检查] 大模型 qwen2.5:3b...
ollama list 2>nul | findstr /C:"qwen2.5:3b" >nul 2>&1 || (
    echo 模型未安装，开始拉取 qwen2.5:3b（约2GB，仅首次需要）...
    ollama pull qwen2.5:3b
)

echo [检查] 后端 Python 依赖...
if not exist "backend\.venv\Scripts\python.exe" (
    echo 首次运行：创建虚拟环境并安装依赖（torch 约2GB，耗时较长）...
    python -m venv "backend\.venv"
    "backend\.venv\Scripts\python" -m pip install -r "backend\requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo [检查] 后端配置文件 .env...
if not exist "backend\.env" copy "backend\.env.example" "backend\.env" >nul

echo [检查] 前端依赖 node_modules...
if not exist "frontend\node_modules" (
    echo 首次运行：安装前端依赖...
    pushd "frontend"
    call npm install --no-fund --no-audit
    popd
)

echo [检查] 知识库向量数据...
if not exist "backend\data\chroma\chroma.sqlite3" (
    echo 首次运行：导入种子知识库（自动下载向量模型，约几分钟）...
    pushd "backend"
    ".venv\Scripts\python" -m app.seed_kb
    popd
)

echo.
echo [启动] 后端服务（FastAPI，端口 8000）...
start "IT知识库-后端" /D "%~dp0backend" cmd /k ".venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 1>%~dp0backend\start_backend.log 2>&1"

echo [启动] 前端服务（Vite，端口 5199）...
start "IT知识库-前端" /D "%~dp0frontend" cmd /k "npm run dev 1>%~dp0frontend\start_frontend.log 2>&1"

echo.
echo 正在等待服务启动（约10秒）...
timeout /t 10 /nobreak >nul

echo 正在打开浏览器...
start "" http://localhost:5199

echo.
echo 启动完成！两个服务窗口请勿关闭，停止服务直接关闭对应窗口。
echo.
pause
