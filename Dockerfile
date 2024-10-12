# ベースイメージの指定
FROM python:3.11.6

# Pythonがpycファイルを書き込まないように
ENV PYTHONDONTWRITEBYTECODE=1

# Pythonがstdoutとstderrをバッファリングしないように
# これにより、バッファリングによりログが発生せずにアプリケーションがクラッシュする状況を避けられる
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリの設定
WORKDIR /backend
ENV PYTHONPATH=/backend

RUN apt-get update && apt-get install -y \
    libopencv-dev cmake

# Ryeのセットアップ
ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

COPY ./.python-version ./pyproject.toml ./requirements* ./README.md ./

RUN curl -sSf https://rye.astral.sh/get | RYE_TOOLCHAIN_VERSION="$(cat .python-version)" RYE_NO_AUTO_INSTALL=1  RYE_INSTALL_OPTION="--yes" bash
RUN rye config --set-bool behavior.global-python=true && \
    rye config --set-bool behavior.use-uv=true

RUN rye pin "$(cat .python-version)" && \
    rye sync

# アプリケーションのソースコードをコピー
COPY . .

# アプリケーションの起動コマンド
CMD ["python", "-m", "uvicorn", "config.asgi:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]
