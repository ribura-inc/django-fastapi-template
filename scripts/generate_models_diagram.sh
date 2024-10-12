#!/bin/bash

# ModelsのPUMLを生成
docker-compose exec -T backend python manage.py generate_puml --add-help --add-choices --add-legend --file new_models_diagram.puml

# 生成されたPUMLの内容が空でないか確認
if [ ! -s new_models_diagram.puml ]; then
    echo "Models diagram is empty. Please check the code and try again." >&2
    rm new_models_diagram.puml
    exit 1
fi

# 生成されたPUMLと既存のPUMLを比較
if ! cmp -s new_models_diagram.puml docs/models_diagram.puml; then
    echo "Models diagram has changed. Please review the changes before committing." >&2
    mv new_models_diagram.puml docs/models_diagram.puml
    exit 1
else
    echo "No changes in models diagram."
    rm new_models_diagram.puml
fi
