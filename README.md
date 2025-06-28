# GTN Engineering IT Helpdesk System

A comprehensive Flask-based IT helpdesk management system designed for professional IT support operations. Successfully migrated to Replit environment with enhanced security, PostgreSQL database integration, and improved ticket history tracking.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-v15+-blue.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-v5.3+-purple.svg)
![Replit](https://img.shields.io/badge/replit-compatible-orange.svg)

## Features

### 🎯 Core Functionality
- **Role-Based Access Control**: Three user levels (Super Admin, Admin, User)
- **Ticket Management**: Complete lifecycle from creation to resolution
- **Enhanced Ticket History**: New streamlined format showing Created By, Assigned By, Assigned To, and Status with colored badges
- **File Upload Support**: Secure attachment system supporting images, PDF, Word, and Excel files
- **Email Notifications**: SMTP integration for automatic ticket assignment notifications
- **System Detection**: Automatic IP address and system name capture
- **Real-time Updates**: Live ticket status tracking and notifications
- **Comment System**: Collaborative ticket discussion and updates

### 📊 Advanced Features
- **Visual Reports Dashboard**: Charts and analytics with Chart.js
- **Excel Export**: Comprehensive ticket data export functionality
- **User Management**: Complete user administration system
- **Assignment System**: Intelligent ticket routing based on categories
- **Search & Filtering**: Advanced ticket filtering and search capabilities

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **Professional Styling**: Modern CSS with custom properties
- **Intuitive Navigation**: Role-based menu system
- **Interactive Elements**: Hover effects and smooth transitions
- **Accessibility**: WCAG compliant design patterns

### 🔧 Technical Features
- **Multi-Database Support**: PostgreSQL (primary), SQL Server, MySQL
- **Security**: CSRF protection, secure password hashing
- **Performance**: Connection pooling and optimized queries
- **Scalability**: Gunicorn WSGI server for production deployment

## System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **Database**: PostgreSQL 15+ (recommended), SQL Server, or MySQL
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Storage**: 100MB for application, additional space for database
- **Network**: Port 5000 for development, 80/443 for production

### Supported Platforms
- **Development**: Windows, macOS, Linux
- **Production**: Linux (Ubuntu 20.04+, CentOS 8+), Windows Server
- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Quick Start (Replit Environment)

### 1. Replit Setup
The system is now optimized for Replit deployment with automatic setup:
- PostgreSQL database automatically provisioned
- Environment variables pre-configured
- Dependencies auto-installed via Replit's package system

### 2. Default Login Credentials
The system creates default accounts on first run:
- **Super Admin**: `super_admin` / `admin123`
- **Admin**: `admin_user` / `admin123`
- **Test User**: `test_user` / `user123`

### 3. Run Application
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

The application will be available at your Replit URL on port 5000

### 4. Local Development Setup (Alternative)
For local development outside Replit:
```bash
git clone <repository-url>
cd gtn-helpdesk-system
pip install -r requirements.txt
export DATABASE_URL="postgresql://username:password@localhost:5432/gtn_helpdesk"
export SESSION_SECRET="your-secret-key-here"
python main.py
```

## Installation Guide

### Development Setup

1. **Install Python 3.11+**
   ```bash
   python --version  # Verify installation
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-wtf flask-login
   pip install werkzeug email-validator openpyxl psycopg2-binary
   pip install gunicorn pymysql pyodbc
   ```

4. **Configure Database**
   - PostgreSQL: See [PostgreSQL Setup Guide](README_PostgreSQL_Setup.md)
   - SQL Server: Configure connection string with pyodbc
   - MySQL: Configure connection string with PyMySQL

### Production Deployment

1. **Configure Environment Variables**
   ```bash
   export DATABASE_URL="your-production-database-url"
   export SESSION_SECRET="secure-production-secret"
   export FLASK_ENV="production"
   ```

2. **Start with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   ```

3. **Setup Reverse Proxy** (Nginx recommended)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

## Configuration

### Database Configuration

The system supports multiple database backends with automatic detection:

```python
# Priority order: PostgreSQL > SQL Server > MySQL
DATABASE_URL = "postgresql://user:pass@host:port/db"  # Primary
SQL_SERVER_URL = "mssql+pyodbc://user:pass@host:port/db?driver=..."
MYSQL_URL = "mysql+pymysql://user:pass@host:port/db"
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Primary database connection | None | Yes |
| `SESSION_SECRET` | Flask session secret key | None | Yes |
| `SQL_SERVER_HOST` | SQL Server hostname | None | No |
| `SQL_SERVER_DATABASE` | SQL Server database name | gtn_helpdesk | No |
| `MYSQL_URL` | MySQL connection URL | None | No |

### Application Settings

```python
# In app.py - customize as needed
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    },
    'WTF_CSRF_ENABLED': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16MB max file upload
})
```

## User Guide

### Default Login Credentials

#### Super Administrator
- **Username**: `superadmin`
- **Password**: `super123`
- **Capabilities**: Full system access, user management, reports

#### Admin Users
- **Username**: `yuvaraj` | **Password**: `admin123`
- **Username**: `jayachandran` | **Password**: `admin123` 
- **Username**: `narainkarthik` | **Password**: `admin123`
- **Capabilities**: Ticket management, assignment, resolution

#### Test User
- **Username**: `testuser` | **Password**: `user123`
- **Capabilities**: Create tickets, view own tickets, add comments

**⚠️ Important**: Change all default passwords immediately after installation!

### User Roles & Permissions

| Feature | User | Admin | Super Admin |
|---------|------|-------|-------------|
| Create Tickets | ✅ | ✅ | ✅ |
| View Own Tickets | ✅ | ✅ | ✅ |
| View All Tickets | ❌ | ✅ | ✅ |
| Assign Tickets | ❌ | ✅ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |
| Reports Dashboard | ❌ | ❌ | ✅ |
| Excel Export | ❌ | ❌ | ✅ |
| System Settings | ❌ | ❌ | ✅ |

### Creating Your First Ticket

1. **Login** as a regular user
2. **Navigate** to "New Ticket" 
3. **Fill out the form**:
   - Title: Descriptive summary
   - Description: Detailed problem description
   - Category: Hardware/Software
   - Priority: Low/Medium/High/Critical
   - System Name: Auto-detected or manual entry
   - File Attachments: Upload images, PDF, Word documents, or Excel files
5. **Submit** - Ticket number will be generated automatically

### Admin Workflow

1. **Dashboard Overview**: View all tickets and statistics
2. **Ticket Assignment**: Assign tickets to appropriate admins
3. **Status Updates**: Update ticket status as work progresses
4. **Comment System**: Add internal notes and user communication
5. **Resolution**: Mark tickets as resolved with solution details

## API Documentation

### Database Models

#### User Model
```python
class User(db.Model):
    id = Integer (Primary Key)
    username = String(80) (Unique, NOT NULL)
    email = String(120) (Unique, NOT NULL)
    password_hash = String(256) (NOT NULL)
    first_name = String(50) (NOT NULL)
    last_name = String(50) (NOT NULL)
    department = String(100) (Optional)
    role = String(50) (NOT NULL, Default: 'User')  # user, admin, super_admin
    is_admin = Boolean (Default: False)
    ip_address = String(45) (Optional, IPv4/IPv6)
    system_name = String(100) (Optional)
    profile_image = String(200) (Optional)
    created_at = DateTime (Default: UTC now)
```

#### Ticket Model
```python
class Ticket(db.Model):
    id = Integer (Primary Key)
    title = String(200) (NOT NULL)
    description = Text (NOT NULL)
    category = String(50) (NOT NULL)  # Hardware, Software
    priority = String(20) (NOT NULL)  # Low, Medium, High, Critical
    status = String(20) (NOT NULL, Default: 'Open')  # Open, In Progress, Resolved, Closed
    user_name = String(100) (NOT NULL)  # Full name of ticket creator
    user_ip_address = String(45) (Optional)  # IP at creation
    user_system_name = String(100) (Optional)  # System name at creation
    image_filename = String(255) (Optional)  # Uploaded file
    user_id = Integer (Foreign Key, NOT NULL → users.id)
    assigned_to = Integer (Foreign Key, Optional → users.id)
    assigned_by = Integer (Foreign Key, Optional → users.id)
    created_at = DateTime (Default: UTC now)
    updated_at = DateTime (Auto-update on changes)
    resolved_at = DateTime (Optional, set when resolved)
```

#### Comment Model
```python
class TicketComment(db.Model):
    id = Integer (Primary Key)
    ticket_id = Integer (Foreign Key, NOT NULL → tickets.id)
    user_id = Integer (Foreign Key, NOT NULL → users.id)
    comment = Text (NOT NULL)
    created_at = DateTime (Default: UTC now)
```

#### Attachment Model
```python
class Attachment(db.Model):
    id = Integer (Primary Key)
    ticket_id = Integer (Foreign Key, NOT NULL → tickets.id)
    filename = String(255) (NOT NULL)
    uploaded_at = DateTime (Default: UTC now)
```

### Key Routes

| Route | Method | Description | Access Level |
|-------|--------|-------------|--------------|
| `/` | GET | Homepage | Public |
| `/user-login` | GET/POST | User authentication | Public |
| `/admin-login` | GET/POST | Admin authentication | Public |
| `/user-dashboard` | GET | User ticket overview | User+ |
| `/admin-dashboard` | GET | Admin ticket management | Admin+ |
| `/super-admin-dashboard` | GET | System overview | Super Admin |
| `/create-ticket` | GET/POST | New ticket creation | User+ |
| `/ticket/<id>` | GET | Ticket details | Owner/Admin+ |
| `/reports-dashboard` | GET | Analytics dashboard | Super Admin |
| `/download-excel-report` | GET | Excel export | Super Admin |

## Advanced Features

### System Information Capture

The application automatically captures:
- **IP Address**: Real client IP (handles proxy forwarding)
- **System Name**: Operating system and browser detection
- **User Agent**: Browser and device information
- **Session Data**: Login time and activity tracking

### Intelligent Assignment System

- **Category-Based**: Routes tickets to specialized teams
- **Workload Balancing**: Distributes tickets evenly among admins
- **Priority Handling**: Escalates critical issues automatically
- **Department Matching**: Assigns based on user department

### File Attachment System

- **Multiple File Types**: Support for images (JPG, PNG, GIF, BMP), PDF documents, Word files (.doc, .docx), and Excel spreadsheets (.xls, .xlsx)
- **Multiple Files**: Upload multiple attachments per ticket
- **Secure Storage**: Files stored with unique timestamps to prevent conflicts
- **Admin Access**: Only administrators can view and download attachments for security
- **File Validation**: Automatic file type validation and size limits

### Reporting & Analytics

- **Visual Charts**: Category, priority, and status breakdowns
- **Export Capabilities**: Excel files with complete ticket data
- **Performance Metrics**: Resolution times and response rates
- **Historical Data**: Trend analysis and reporting

### Security Features

- **Password Hashing**: Werkzeug secure password storage
- **CSRF Protection**: Form submission security
- **Session Management**: Secure user session handling
- **Input Validation**: WTForms data validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check database status
systemctl status postgresql  # Linux
net start postgresql-x64-16  # Windows

# Verify connection string
psql -U username -d database_name -h localhost
```

#### Application Won't Start
```bash
# Check Python version
python --version

# Verify dependencies
pip list | grep -E "(flask|sqlalchemy|wtf)"

# Check environment variables
echo $DATABASE_URL
echo $SESSION_SECRET
```

#### Permission Denied Errors
```bash
# Check file permissions
chmod 755 main.py
chmod 644 *.html *.css *.js

# Database permissions
GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk TO username;
```

### Performance Optimization

#### Database Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
```

#### Application Tuning
```python
# Configure connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'pool_recycle': 300,
    'pool_pre_ping': True,
    'max_overflow': 30
}
```

## Development

### Project Structure
```
gtn-helpdesk-system/
├── main.py                 # Application entry point
├── app.py                  # Flask app configuration
├── routes.py               # URL routing and views
├── models.py               # Database models
├── forms.py                # WTForms definitions
├── static/                 # CSS, JS, images
│   ├── style.css          # Custom styling
│   ├── script.js          # Client-side functionality
│   └── gtn_logo.jpg       # Company logo
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── user_dashboard.html # User interface
│   ├── admin_dashboard.html # Admin interface
│   └── ...
├── README.md              # This file
├── README_PostgreSQL_Setup.md # Database setup guide
└── requirements.txt       # Python dependencies
```

### Adding New Features

1. **Database Changes**: Update models.py and run migrations
2. **Forms**: Add new form classes in forms.py
3. **Routes**: Create new endpoints in routes.py
4. **Templates**: Design HTML interfaces in templates/
5. **Styling**: Update static/style.css for new components

### Code Style Guidelines

- **Python**: Follow PEP 8 standards
- **HTML**: Use semantic markup and proper indentation
- **CSS**: Use CSS custom properties and BEM methodology
- **JavaScript**: ES6+ features with proper error handling

## Deployment Options

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Systemd Service (Linux)
```ini
[Unit]
Description=GTN Helpdesk System
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/opt/gtn-helpdesk
Environment=DATABASE_URL=postgresql://...
Environment=SESSION_SECRET=...
ExecStart=/opt/gtn-helpdesk/venv/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Windows Service
Use NSSM (Non-Sucking Service Manager) or similar tools to run as Windows service.

## Support & Maintenance

### Backup Strategy
```bash
# Daily database backup
pg_dump -U username gtn_helpdesk > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/app
```

### Monitoring
- **Application Logs**: Check Flask application logs
- **Database Performance**: Monitor query execution times
- **System Resources**: CPU, memory, and disk usage
- **User Activity**: Login patterns and ticket creation rates

### Updates & Patches
1. **Test Environment**: Always test updates in staging
2. **Database Migration**: Use proper migration scripts
3. **Backup First**: Create full backup before updates
4. **Gradual Rollout**: Deploy to small user groups first

## Recent Updates & Changelog

### June 27, 2025 - v2.1.0 (Replit Migration & Enhanced Features)
- **Replit Integration**: Successfully migrated from Replit Agent to Replit environment
- **Automatic PostgreSQL**: Database provisioning and setup now fully automated
- **Enhanced Ticket History**: Redesigned ticket history sidebar with cleaner format:
  - Created By: Shows ticket creator with timestamp
  - Assigned By: Shows who assigned the ticket (or "Not assigned")
  - Assigned To: Shows current assignee (or "Not assigned")
  - Status: Current status with colored badge
- **Bug Fixes**: Resolved edit ticket template errors and property access issues
- **Security**: Enhanced client/server separation and secure configuration

### Previous Major Updates
- **June 26, 2025 - v2.0.5**: Enhanced user management with complete CRUD operations
- **June 23, 2025 - v2.0.4**: Improved file upload system supporting PDF, Word, Excel files
- **June 22, 2025 - v2.0.3**: Added visual reports dashboard and MySQL support
- **June 21, 2025 - v2.0.0**: Initial PostgreSQL integration and setup

## License

This project is proprietary software developed for GTN Engineering (India) Ltd.

## Contact

For technical support or questions:
- **Email**: it-support@gtnengineering.com
- **Internal Helpdesk**: Use this system to create tickets
- **Emergency**: Contact IT department directly

---

**GTN Engineering (India) Ltd - IT Team**  
*Professional IT Support Solutions*

Last Updated: June 27, 2025  
Version: 2.1.0