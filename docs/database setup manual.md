# PostgreSQL Database Setup Manual for Django
## Nexus Vote Project

**Document Version:** 1.0  
**Last Updated:** August 13, 2025  
**Author:** MATRIX30  
**Project:** Nexus Vote - Decentralized Voting Platform

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [PostgreSQL Installation](#postgresql-installation)
4. [Database Configuration](#database-configuration)
5. [Django Configuration](#django-configuration)
6. [Environment Setup](#environment-setup)
7. [Database Migration](#database-migration)
8. [Testing the Connection](#testing-the-connection)
9. [Security Best Practices](#security-best-practices)
10. [Troubleshooting](#troubleshooting)
11. [Backup and Recovery](#backup-and-recovery)
12. [Performance Optimization](#performance-optimization)

---

## Overview

This manual provides step-by-step instructions for setting up PostgreSQL as the primary database for the Nexus Vote Django application. PostgreSQL is chosen for its robustness, scalability, and advanced features that support the secure voting platform requirements.

### Why PostgreSQL for Nexus Vote?

- **ACID Compliance**: Ensures data integrity for critical voting data
- **Advanced Security**: Row-level security and encryption capabilities
- **Scalability**: Handles concurrent voting sessions efficiently
- **JSON Support**: Native support for poll metadata and dynamic configurations
- **Full-text Search**: Enhanced search capabilities for polls and users

---

## Prerequisites

Before starting the database setup, ensure you have:

- Administrative access to your system
- Python 3.8+ installed
- Django 4.0+ installed
- Basic knowledge of command line operations
- Internet connection for downloading packages

---

## PostgreSQL Installation

### Linux (Ubuntu/Debian)

```bash
# Update package lists
sudo apt update

# Install PostgreSQL and additional tools
sudo apt install postgresql postgresql-contrib postgresql-client

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
sudo systemctl status postgresql
```

### Linux (CentOS/RHEL/Fedora)

```bash
# For CentOS/RHEL 8+
sudo dnf install postgresql postgresql-server postgresql-contrib

# For older versions
sudo yum install postgresql postgresql-server postgresql-contrib

# Initialize database
sudo postgresql-setup --initdb

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS

```bash
# Using Homebrew (recommended)
brew install postgresql
brew services start postgresql

# Alternative: Download from official website
# Visit: https://www.postgresql.org/download/macosx/
```

### Windows

1. Download PostgreSQL installer from [official website](https://www.postgresql.org/download/windows/)
2. Run the installer as administrator
3. Follow installation wizard:
   - Choose installation directory
   - Select all components
   - Set postgres user password
   - Set port (default: 5432)
   - Choose locale
4. Complete installation

---

## Database Configuration

### 1. Access PostgreSQL Command Line

```bash
# Switch to postgres user (Linux/macOS)
sudo -u postgres psql

# For Windows, use pgAdmin or Command Prompt
psql -U postgres
```

### 2. Create Database and User

```sql
-- Create database for Nexus Vote
CREATE DATABASE nexus_vote_db;

-- Create dedicated user
CREATE USER nexus_vote_user WITH PASSWORD 'SecurePassword123!';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nexus_vote_db TO nexus_vote_user;

-- Additional permissions for Django
ALTER USER nexus_vote_user CREATEDB;

-- Exit PostgreSQL
\q
```

### 3. Configure PostgreSQL Settings

Edit PostgreSQL configuration file:

```bash
# Find configuration file location
sudo -u postgres psql -c 'SHOW config_file;'

# Common locations:
# Linux: /etc/postgresql/14/main/postgresql.conf
# macOS: /usr/local/var/postgres/postgresql.conf
# Windows: C:\Program Files\PostgreSQL\14\data\postgresql.conf
```

Key settings to modify:

```ini
# postgresql.conf
listen_addresses = 'localhost'  # For development
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Enable logging for debugging
log_statement = 'all'
log_duration = on
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
```

### 4. Configure Client Authentication

Edit `pg_hba.conf`:

```bash
# Find pg_hba.conf location
sudo -u postgres psql -c 'SHOW hba_file;'
```

Add or modify these lines:

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   nexus_vote_db   nexus_vote_user                         md5
host    nexus_vote_db   nexus_vote_user 127.0.0.1/32           md5
host    nexus_vote_db   nexus_vote_user ::1/128                 md5
```

Restart PostgreSQL:

```bash
# Linux
sudo systemctl restart postgresql

# macOS
brew services restart postgresql

# Windows
net stop postgresql-x64-14
net start postgresql-x64-14
```

---

## Django Configuration

### 1. Install Required Packages

```bash
# Navigate to project directory
cd /path/to/nexus_vote

# Install psycopg2 (PostgreSQL adapter for Python)
pip install psycopg2-binary

# Or for production
pip install psycopg2

# Install additional packages
pip install python-decouple  # For environment variables
```

### 2. Update requirements.txt

```text
Django>=4.2.0
psycopg2-binary>=2.9.0
python-decouple>=3.8
python-dotenv>=1.0.0
```

### 3. Configure Django Settings

Edit `nexus_vote/settings.py`:

```python
import os
from decouple import config

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='nexus_vote_db'),
        'USER': config('DB_USER', default='nexus_vote_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 60,
            'options': '-c default_transaction_isolation=serializable'
        },
    }
}

# Database connection pooling (for production)
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# Time zone configuration
USE_TZ = True
TIME_ZONE = 'UTC'

# For better PostgreSQL performance
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

## Environment Setup

### 1. Create Environment File

Create `.env` file in project root:

```bash
# Database Configuration
DB_NAME=nexus_vote_db
DB_USER=nexus_vote_user
DB_PASSWORD=SecurePassword123!
DB_HOST=localhost
DB_PORT=5432

# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Security Settings
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
```

### 2. Load Environment Variables

In `settings.py`:

```python
from dotenv import load_dotenv
load_dotenv()

# Or using python-decouple (recommended)
from decouple import config, Csv

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

---

## Database Migration

### 1. Test Database Connection

```bash
# Test connection
python manage.py dbshell

# Should connect to PostgreSQL
# Exit with \q
```

### 2. Create and Apply Migrations

```bash
# Create initial migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Verify Tables Creation

```sql
-- Connect to database
psql -U nexus_vote_user -d nexus_vote_db

-- List all tables
\dt

-- Describe a table (example)
\d auth_user

-- Exit
\q
```

---

## Testing the Connection

### 1. Django Shell Test

```bash
python manage.py shell
```

```python
from django.db import connection
from django.test.utils import get_runner
from django.conf import settings

# Test database connection
cursor = connection.cursor()
cursor.execute("SELECT version();")
result = cursor.fetchone()
print(f"PostgreSQL Version: {result[0]}")

# Test model operations
from django.contrib.auth.models import User
user_count = User.objects.count()
print(f"User count: {user_count}")
```

### 2. Create Test Data

```python
# In Django shell
from django.contrib.auth.models import User

# Create test user
test_user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)
print(f"Created user: {test_user.username}")
```

---

## Security Best Practices

### 1. Database Security

```sql
-- Create read-only user for reporting
CREATE USER nexus_readonly WITH PASSWORD 'ReadOnlyPass123!';
GRANT CONNECT ON DATABASE nexus_vote_db TO nexus_readonly;
GRANT USAGE ON SCHEMA public TO nexus_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO nexus_readonly;

-- Revoke unnecessary permissions
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

### 2. Connection Security

```python
# In settings.py for production
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
    'connect_timeout': 60,
    'options': '-c default_transaction_isolation=serializable'
}
```

### 3. Environment Security

```bash
# Set proper file permissions
chmod 600 .env

# Add to .gitignore
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Connection Refused

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check listening ports
sudo netstat -tlnp | grep 5432

# Start PostgreSQL if not running
sudo systemctl start postgresql
```

#### 2. Authentication Failed

```sql
-- Reset user password
ALTER USER nexus_vote_user WITH PASSWORD 'NewPassword123!';

-- Check user permissions
\du nexus_vote_user
```

#### 3. Permission Denied

```sql
-- Grant database permissions
GRANT ALL PRIVILEGES ON DATABASE nexus_vote_db TO nexus_vote_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nexus_vote_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nexus_vote_user;
```

#### 4. Encoding Issues

```sql
-- Check database encoding
SELECT datname, datcollate, datctype FROM pg_database WHERE datname = 'nexus_vote_db';

-- Create database with specific encoding
CREATE DATABASE nexus_vote_db 
    WITH ENCODING = 'UTF8' 
    LC_COLLATE = 'en_US.UTF-8' 
    LC_CTYPE = 'en_US.UTF-8';
```

---

## Backup and Recovery

### 1. Create Database Backup

```bash
# Full database backup
pg_dump -U nexus_vote_user -h localhost nexus_vote_db > nexus_vote_backup.sql

# Compressed backup
pg_dump -U nexus_vote_user -h localhost -Fc nexus_vote_db > nexus_vote_backup.dump

# Backup with timestamp
pg_dump -U nexus_vote_user -h localhost nexus_vote_db > "nexus_vote_$(date +%Y%m%d_%H%M%S).sql"
```

### 2. Restore Database

```bash
# Restore from SQL file
psql -U nexus_vote_user -h localhost nexus_vote_db < nexus_vote_backup.sql

# Restore from dump file
pg_restore -U nexus_vote_user -h localhost -d nexus_vote_db nexus_vote_backup.dump
```

### 3. Automated Backup Script

Create `backup_script.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/nexus_vote_$TIMESTAMP.sql"

# Create backup
pg_dump -U nexus_vote_user -h localhost nexus_vote_db > "$BACKUP_FILE"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "nexus_vote_*.sql" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

---

## Performance Optimization

### 1. Database Configuration

```sql
-- Create indexes for better performance
CREATE INDEX idx_poll_created_at ON polls_poll(created_at);
CREATE INDEX idx_vote_poll_id ON votes_vote(poll_id);
CREATE INDEX idx_user_email ON auth_user(email);

-- Analyze tables for optimal query plans
ANALYZE;

-- Update table statistics
VACUUM ANALYZE;
```

### 2. Django Settings

```python
# In settings.py
DATABASES['default']['OPTIONS'] = {
    'MAX_CONNS': 20,
    'connect_timeout': 60,
    'options': '-c default_transaction_isolation=read_committed'
}

# Connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. Monitoring Queries

```python
# Add to settings.py for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
```

---

## Conclusion

Following this manual ensures a robust, secure, and optimized PostgreSQL setup for the Nexus Vote Django application. Regular maintenance, monitoring, and security updates are essential for production environments.

For additional support or questions, contact: matrixboy30@gmail.com

---

**Document End**
