# 仮想環境のディレクトリ名
VENV_DIR="myenv"

# 仮想環境が存在しない場合、作成する
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install -r requirements.txt
else
    source $VENV_DIR/bin/activate
fi

# Djangoプロジェクトを起動
python manage.py runserver

# 仮想環境を非アクティブにする
# deactivate