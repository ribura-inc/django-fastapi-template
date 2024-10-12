#!/bin/bash

# OpenAPI JSONを生成
docker compose exec -T backend python scripts/print_openapi.py  > /tmp/new_openapi.json # git配下に新しいファイルが作成されると、pre-commitが再度トリガーされてしまうため、一時的に/tmpに出力

# 生成されたJSONの内容が空でないか確認
if [ ! -s /tmp/new_openapi.json ]; then
    echo "OpenAPI specification is empty. Please check the code and try again." >&2
    rm /tmp/new_openapi.json
    exit 1
fi

# 生成されたJSONと既存のJSONを比較
if ! cmp -s /tmp/new_openapi.json docs/openapi.json; then
    echo "OpenAPI specification has changed. Please review the changes before committing." >&2
    mv /tmp/new_openapi.json docs/openapi.json
    exit 1
else
    echo "No changes in OpenAPI specification."
    rm /tmp/new_openapi.json
fi
