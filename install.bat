@echo off
REM Windows 安装脚本

echo ==========================================
echo 安装项目依赖包
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo 检测到 Python:
python --version
echo.

REM 检查虚拟环境
if "%VIRTUAL_ENV%"=="" (
    echo 未检测到虚拟环境
    set /p create_venv="是否创建虚拟环境? (y/n): "
    if /i "%create_venv%"=="y" (
        echo 创建虚拟环境...
        python -m venv venv
        if errorlevel 1 (
            echo 警告: 虚拟环境创建失败
        ) else (
            echo 激活虚拟环境...
            call venv\Scripts\activate.bat
        )
    )
) else (
    echo 当前已在虚拟环境中: %VIRTUAL_ENV%
)

echo.
echo 升级 pip...
python -m pip install --upgrade pip --quiet

echo.
echo 安装依赖包...
echo 这可能需要几分钟时间...
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ==========================================
    echo 依赖包安装失败
    echo ==========================================
    echo.
    echo 可能的解决方案:
    echo 1. 使用管理员权限运行
    echo 2. 使用虚拟环境
    echo 3. 手动安装关键包
    pause
    exit /b 1
) else (
    echo.
    echo ==========================================
    echo 依赖包安装成功！
    echo ==========================================
    echo.
    echo 下一步:
    echo 1. 配置环境变量: 复制 env.example 为 .env
    echo 2. 编辑 .env 文件，填写你的 API 密钥
    echo 3. 启动服务: python main.py
    echo.
    pause
)
