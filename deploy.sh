#!/bin/bash

echo "deleting old app"
sudo rm -rf /var/www/sdu_dorm/

echo "creating app folder"
sudo mkdir -p /var/www/sdu_dorm

echo "moving files to app folder"
sudo cp -R * /var/www/sdu_dorm/ # Используем cp вместо mv, чтобы сохранить исходные файлы

# Navigate to the app directory
cd /var/www/sdu_dorm/

# Add Python 3.10 PPA
sudo apt-get update
sudo add-apt-repository ppa:deadsnakes/ppa -y # Добавлен -y для автоматического подтверждения
sudo apt-get update

echo "installing python 3.10.2 and pip"
sudo apt-get install -y python3.10 python3.10-venv # Установка пакета python3.10-venv для создания виртуального окружения

# Create a virtual environment
echo "Creating a virtual environment"
python3.10 -m venv venv
source venv/bin/activate

# Install application dependencies from requirements.txt
echo "Install application dependencies from requirements.txt"
pip install -r requirements.txt

# Apply migrations
echo "Applying database migrations"
python manage.py migrate

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Configure Nginx to act as a reverse proxy
if [ ! -f /etc/nginx/sites-available/sdu_dorm ]; then
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo bash -c 'cat > /etc/nginx/sites-available/sdu_dorm <<EOF
server {
    listen 80;
    server_name 13.49.18.134;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sdu_dorm/sdu_dorm.sock;
    }

    location /static/ {
        alias /var/www/sdu_dorm/static/;
    }
}
EOF'

    sudo ln -s /etc/nginx/sites-available/sdu_dorm /etc/nginx/sites-enabled
    sudo systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
sudo pkill gunicorn
sudo rm -rf sdu_dorm.sock

# Start Gunicorn with the Django application
echo "starting gunicorn"
gunicorn --workers 3 --bind unix:/var/www/sdu_dorm/sdu_dorm.sock sdu_dorm.wsgi:application --daemon

echo "Deployment is completed 🚀"
