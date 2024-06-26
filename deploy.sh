#!/bin/bash

echo "deleting old app"
sudo rm -rf /var/www/

echo "creating app folder"
sudo mkdir -p /var/www/sdu_dorm

echo "moving files to app folder"
sudo mv  * /var/www/sdu_dorm

# Navigate to the app directory
cd /var/www/sdu_dorm/
sudo mv env .env

sudo apt-get update
echo "installing python and pip"
sudo apt-get install -y python3 python3-pip

# Install application dependencies from requirements.txt
echo "Install application dependencies from requirements.txt"
sudo pip install -r requirements.txt

echo "Applying database migrations..."
sudo python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
sudo python3 manage.py collectstatic --noinput

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo rm -f /etc/nginx/sites-available/myapp

# Configure Nginx to act as a reverse proxy if not already configured
if [ ! -f /etc/nginx/sites-available/myapp ]; then
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo bash -c 'cat > /etc/nginx/sites-available/myapp <<EOF
server {
    listen 80;
    server_name _;
    client_max_body_size 50M;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sdu_dorm/myapp.sock;
    }
}
EOF'

    sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
    sudo systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
sudo pkill gunicorn
sudo rm -rf myapp.sock
sudo rm -f /var/www/sdu_dorm/myapp.sock

# # Start Gunicorn with the Django application
# # gunicorn --workers 3 --bind 0.0.0.0:8000 server:app &
echo "starting gunicorn"
sudo gunicorn --workers 3 --bind unix:/var/www/sdu_dorm/myapp.sock sdu_dorm.wsgi:application --daemon

echo "Deployment is completed 🚀"
