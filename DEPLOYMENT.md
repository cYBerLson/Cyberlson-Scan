# SecureCheck-NG Deployment Guide

This document provides comprehensive instructions for deploying the SecureCheck-NG application in various environments, from local development to production on a Ubuntu Virtual Private Server (VPS) and cloud platforms like Render or Railway.

## 1. Local Development

Setting up SecureCheck-NG for local development is straightforward and allows for easy testing and feature development.

### 1.1. Create Virtual Environment

It is highly recommended to use a Python virtual environment to manage project dependencies and avoid conflicts with system-wide packages.

```bash
# Navigate to the project root directory
cd /path/to/SecureCheck-NG

# Create a virtual environment named 'venv'
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 1.2. Install Dependencies

Once the virtual environment is active, install all required Python packages using `pip`.

```bash
# Ensure your virtual environment is active
pip install -r requirements.txt
```

### 1.3. Configure Environment Variables

SecureCheck-NG uses environment variables for sensitive configurations. Create a `.env` file based on the provided example.

```bash
# Copy the example environment file
cp .env.example .env
```

Edit the newly created `.env` file using a text editor (e.g., `nano .env`) and set the `SECRET_KEY` to a strong, random value. For local development, `FLASK_CONFIG` should be set to `development`.

```ini
# .env file content
SECRET_KEY='your_very_long_and_random_secret_key_for_development'
FLASK_CONFIG=development
# PORT=5000 # Uncomment and change if you need a different port
```

### 1.4. Run Securely (Local)

With dependencies installed and environment variables configured, you can run the Flask application locally.

```bash
# Ensure your virtual environment is active
# The 'flask run' command will automatically pick up the .env file
flask run

# Alternatively, you can run using the provided run.py script
# python run.py
```

The application will typically be accessible at `http://127.0.0.1:5000`.

## 2. Production Deployment (Ubuntu VPS)

Deploying SecureCheck-NG to a production Ubuntu VPS involves setting up a robust and secure environment using Gunicorn as a WSGI server and Nginx as a reverse proxy.

### 2.1. Server Preparation

Connect to your Ubuntu VPS via SSH.

```bash
ssh your_user@your_vps_ip
```

### 2.2. Install Python and Dependencies

Ensure Python 3.11+ and necessary development tools are installed.

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip build-essential nginx curl git -y
```

### 2.3. Clone Repository and Setup Virtual Environment

Clone your project repository and set up the virtual environment on the server.

```bash
# Navigate to a suitable directory, e.g., /var/www/
cd /var/www/
sudo git clone https://github.com/your-username/SecureCheck-NG.git
sudo chown -R your_user:your_user SecureCheck-NG # Change ownership to your user
cd SecureCheck-NG

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.4. Configure Environment Variables (Production)

Create a `.env` file in the project root (`/var/www/SecureCheck-NG/.env`) with production-ready values. **Crucially, generate a new, strong `SECRET_KEY` and set `FLASK_CONFIG` to `production`.**

```ini
# .env file content for production
SECRET_KEY='a_very_long_complex_and_unique_secret_key_for_production'
FLASK_CONFIG=production
PORT=5000 # Gunicorn will bind to this port
```

### 2.5. Install Gunicorn

Gunicorn will serve the Flask application.

```bash
# Ensure virtual environment is active
pip install gunicorn
```

### 2.6. Configure Gunicorn Systemd Service

Create a systemd service file to manage Gunicorn, ensuring it starts automatically and runs reliably.

```bash
sudo nano /etc/systemd/system/securecheck.service
```

Add the following content to `securecheck.service`:

```ini
[Unit]
Description=Gunicorn instance to serve SecureCheck-NG
After=network.target

[Service]
User=your_user # Replace with your actual username
Group=www-data
WorkingDirectory=/var/www/SecureCheck-NG
Environment="PATH=/var/www/SecureCheck-NG/venv/bin"
Environment="FLASK_CONFIG=production"
Environment="SECRET_KEY=a_very_long_complex_and_unique_secret_key_for_production" # Set your actual secret key here or load from .env
ExecStart=/var/www/SecureCheck-NG/venv/bin/gunicorn --workers 3 --bind unix:/var/www/SecureCheck-NG/securecheck.sock -m 007 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Note**: For `SECRET_KEY` in the systemd service, it's generally more secure to load it from a separate, restricted file or use a secrets management system. For simplicity in this guide, it's shown directly. In a real production environment, consider more robust secret management.

Reload systemd, start the service, and enable it to run on boot:

```bash
sudo systemctl daemon-reload
sudo systemctl start securecheck
sudo systemctl enable securecheck
```

Check the status:

```bash
sudo systemctl status securecheck
```

### 2.7. Configure Nginx Reverse Proxy

Nginx will act as a reverse proxy, handling incoming requests and forwarding them to Gunicorn.

```bash
sudo nano /etc/nginx/sites-available/securecheck
```

Add the following Nginx configuration:

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com; # Replace with your domain

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/SecureCheck-NG/securecheck.sock;
    }
}
```

Create a symbolic link to enable the site and test Nginx configuration:

```bash
sudo ln -s /etc/nginx/sites-available/securecheck /etc/nginx/sites-enabled
sudo nginx -t
```

If the test is successful, restart Nginx:

```bash
sudo systemctl restart nginx
```

### 2.8. Enable HTTPS (Let's Encrypt Example)

Secure your application with HTTPS using Certbot and Let's Encrypt.

```bash
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

Follow the prompts. Certbot will automatically configure Nginx for HTTPS.

### 2.9. Secure Firewall Setup (UFW)

Configure UFW (Uncomplicated Firewall) to allow only necessary traffic.

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw enable
```

## 3. Deployment to Render or Railway

Cloud platforms like Render and Railway offer simplified deployment for Flask applications. The general steps are similar, focusing on connecting your Git repository and configuring environment variables.

### 3.1. General Steps

1.  **Connect to Git Repository**: Link your GitHub/GitLab repository containing SecureCheck-NG to your Render/Railway account.
2.  **Build Command**: Specify the command to install dependencies. This usually involves activating a virtual environment and running `pip install -r requirements.txt`.
    *   Example (Render): `pip install -r requirements.txt`
3.  **Start Command**: Define how your application should be started. For Flask with Gunicorn, this would be:
    *   Example: `gunicorn --workers 3 --bind 0.0.0.0:$PORT run:app`
    *   Note: `$PORT` is usually provided by the platform.
4.  **Environment Variables**: Crucially, add your `SECRET_KEY` and set `FLASK_CONFIG=production` in the platform's environment variable settings. Each platform has a dedicated section for this.
5.  **Health Checks**: Configure health checks to ensure your application is running correctly.
6.  **Custom Domains & HTTPS**: Both platforms provide easy integration for custom domains and automatically handle HTTPS certificates.

### 3.2. Render Specifics

*   **Blueprint**: You can define a `render.yaml` blueprint for infrastructure as code.
*   **Disk**: If your application needed persistent storage, you would configure a disk.

### 3.3. Railway Specifics

*   **Service Type**: Choose 
a `Service` and select `Python` as the language.
*   **Build & Deploy**: Railway automatically detects `requirements.txt` and uses `pip install`.

Remember to always keep your `SECRET_KEY` secure and never commit it directly to your repository.
