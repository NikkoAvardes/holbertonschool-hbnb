#!/bin/bash

# --- Configuration ---
# Убедитесь, что эти пути правильные для вашего проекта
BACKEND_DIR="/Users/nicolaicarabet/Documents/Holberton/Python/holbertonschool-hbnb/part3/hbnb"
FRONTEND_DIR="/Users/nicolaicarabet/Documents/Holberton/Python/holbertonschool-hbnb/part4/base_files"
FRONTEND_PORT=8000
FLASK_PORT=5000

# Helper Function: Check and Kill Port
# Проверяет, занят ли порт, и принудительно завершает процесс.
check_and_kill_port() {
    local PORT=$1
    echo "Checking port $PORT for conflicting processes..."
    
    # Находим PID процесса, который слушает данный порт
    PID=$(sudo lsof -t -i :"$PORT" 2>/dev/null)
    
    if [ ! -z "$PID" ]; then
        echo "Port $PORT is currently in use by PID(s): $PID. Attempting to kill..."
        # Принудительно завершаем процесс
        sudo kill -9 "$PID"
        
        if [ $? -eq 0 ]; then
            echo "Successfully terminated process(es) on port $PORT."
        else
            echo "WARNING: Could not terminate process(es) on port $PORT."
        fi
    else
        echo "Port $PORT is free."
    fi
}

# --- Function to kill background processes on script exit (CRITICAL) ---
# Гарантирует, что процессы, запущенные этим скриптом, будут остановлены при нажатии Ctrl+C.
cleanup() {
    echo -e "\n\nStopping HBNB services..."
    # Проверяем и останавливаем Flask
    if [ ! -z "$FLASK_PID" ]; then
        kill "$FLASK_PID" 2>/dev/null
        echo "Backend (Flask PID $FLASK_PID) stopped."
    fi
    # Проверяем и останавливаем Frontend
    if [ ! -z "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID" 2>/dev/null
        echo "Frontend Server (PID $FRONTEND_PID) stopped."
    fi
    exit 0
}

# Перехватываем сигналы прерывания (Ctrl+C)
trap cleanup INT TERM

# --- 0. Pre-launch Cleanup: Clearing Ports ---
echo "--- 0. Pre-launch Cleanup: Clearing Ports ---"
check_and_kill_port "$FLASK_PORT"
check_and_kill_port "$FRONTEND_PORT"
sleep 1 # Даем системе секунду

# --- 1. Start Flask Backend API ---
echo -e "\n--- 1. Starting Flask Backend API ---"
echo "Directory: $BACKEND_DIR"

if [ -d "$BACKEND_DIR" ]; then
    (
        cd "$BACKEND_DIR" || exit 1
        
        # Активация виртуального окружения
        source venv/bin/activate
        
        # Установка переменных окружения Flask
        export FLASK_APP=run.py
        export HBNB_ENV=dev 

        # Запуск Flask в фоне
        flask run --port "$FLASK_PORT" --host 0.0.0.0 > flask_server.log 2>&1 &
        FLASK_PID=$!
        echo "Flask server started (PID: $FLASK_PID) on port $FLASK_PORT. Check flask_server.log for details."
    )
else
    echo "ERROR: Backend directory '$BACKEND_DIR' not found."
    exit 1
fi

# Ждем запуска Flask
sleep 2

# --- 2. Start Python Static Frontend Server ---
echo -e "\n--- 2. Starting Frontend Static Server ---"
echo "Directory: $FRONTEND_DIR"

if [ -d "$FRONTEND_DIR" ]; then
    (
        cd "$FRONTEND_DIR" || exit 1
        
        # Запуск простого HTTP-сервера Python в фоне
        python3 -m http.server "$FRONTEND_PORT" &
        FRONTEND_PID=$!
        echo "Frontend server started (PID: $FRONTEND_PID) on port $FRONTEND_PORT."
    )
else
    echo "ERROR: Frontend directory '$FRONTEND_DIR' not found. Terminating Flask."
    kill "$FLASK_PID" 2>/dev/null
    exit 1
fi

# --- 3. Final Instructions ---
echo -e "\n-----------------------------------------------------"
echo "HBNB Servers are running concurrently."
echo "Backend API (Flask): http://127.0.0.1:$FLASK_PORT/api/v1/"
echo "Frontend App:        http://127.0.0.1:$FRONTEND_PORT/index.html"
echo "-----------------------------------------------------"
echo "Press Ctrl+C to stop both servers."

# Ждем остановки скрипта пользователем (Ctrl+C)
wait