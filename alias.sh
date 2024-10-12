#########################
#### alias settings  ####
#########################

# docker
alias build='docker compose build'
alias up='docker compose up'
alias stop='docker compose stop'
alias down='docker compose down'
alias upd='docker compose up -d' # up with detached mode(background)
alias restart='docker compose restart'

# fastapi container
alias backend_bash='docker compose exec backend bash'
alias makemigrations='docker compose exec backend python manage.py makemigrations'
alias migrate='docker compose exec backend python manage.py migrate'
alias showmigrations='docker compose exec backend python manage.py showmigrations'
alias createsuperuser='docker compose exec backend python manage.py createsuperuser'
alias collectstatic='docker compose exec backend python manage.py collectstatic --noinput'
alias dependencies='docker compose exec backend rye sync'
alias generate_puml='docker compose exec backend python manage.py generate_puml --add-help --add-choices --add-legend'
