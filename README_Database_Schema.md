# GTN Engineering IT Helpdesk - Database Schema

## Overview

This document provides comprehensive documentation for the GTN Engineering IT Helpdesk System database schema. The system uses PostgreSQL as the primary database with support for SQLite (development) and other database systems.

## Database Tables

### 1. Users Table (`users`)

Stores user account information including employees, admins, and super admins.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(50) NOT NULL DEFAULT 'User',
    is_admin BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    system_name VARCHAR(100),
    profile_image VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns Description:
- **id**: Primary key, auto-incrementing integer
- **username**: Unique username (3-80 characters)
- **email**: Unique email address
- **password_hash**: Hashed password using Werkzeug security
- **first_name**: User's first name (2-50 characters)
- **last_name**: User's last name (2-50 characters)
- **department**: Optional department name
- **role**: User role ('user', 'admin', 'super_admin')
- **is_admin**: Boolean flag for admin privileges
- **ip_address**: Last known IP address (IPv4/IPv6)
- **system_name**: Last known system/computer name
- **profile_image**: Optional profile image filename
- **created_at**: Account creation timestamp

#### Indexes:
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### 2. Tickets Table (`tickets`)

Stores IT support tickets with detailed information and tracking.

```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    user_name VARCHAR(100) NOT NULL,
    user_ip_address VARCHAR(45),
    user_system_name VARCHAR(100),
    image_filename VARCHAR(255),
    user_id INTEGER NOT NULL REFERENCES users(id),
    assigned_to INTEGER REFERENCES users(id),
    assigned_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

#### Columns Description:
- **id**: Primary key, auto-incrementing integer
- **title**: Ticket title/summary (5-200 characters)
- **description**: Detailed description of the issue
- **category**: Issue category ('Hardware', 'Software')
- **priority**: Priority level ('Low', 'Medium', 'High', 'Critical')
- **status**: Current status ('Open', 'In Progress', 'Resolved', 'Closed')
- **user_name**: Full name of ticket creator (captured at creation)
- **user_ip_address**: IP address when ticket was created
- **user_system_name**: System name when ticket was created
- **image_filename**: Optional uploaded image filename
- **user_id**: Foreign key to users table (ticket creator)
- **assigned_to**: Foreign key to users table (assigned admin)
- **assigned_by**: Foreign key to users table (who assigned the ticket)
- **created_at**: Ticket creation timestamp
- **updated_at**: Last modification timestamp
- **resolved_at**: Resolution timestamp (null if not resolved)

#### Indexes:
```sql
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_tickets_assigned_by ON tickets(assigned_by);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
```

### 3. Ticket Comments Table (`ticket_comments`)

Stores comments and updates on tickets for communication tracking.

```sql
CREATE TABLE ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns Description:
- **id**: Primary key, auto-incrementing integer
- **ticket_id**: Foreign key to tickets table
- **user_id**: Foreign key to users table (comment author)
- **comment**: Comment text content (minimum 5 characters)
- **created_at**: Comment creation timestamp

#### Indexes:
```sql
CREATE INDEX idx_ticket_comments_ticket_id ON ticket_comments(ticket_id);
CREATE INDEX idx_ticket_comments_user_id ON ticket_comments(user_id);
CREATE INDEX idx_ticket_comments_created_at ON ticket_comments(created_at);
```

### 4. Attachments Table (`attachments`)

Stores file attachments associated with tickets, supporting multiple file types.

```sql
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns Description:
- **id**: Primary key, auto-incrementing integer
- **ticket_id**: Foreign key to tickets table
- **filename**: Original filename with timestamp prefix for uniqueness
- **uploaded_at**: File upload timestamp

#### Supported File Types:
- **Images**: JPG, JPEG, PNG, GIF, BMP
- **Documents**: PDF files
- **Office Files**: Word (.doc, .docx), Excel (.xls, .xlsx)

#### Indexes:
```sql
CREATE INDEX idx_attachments_ticket_id ON attachments(ticket_id);
CREATE INDEX idx_attachments_uploaded_at ON attachments(uploaded_at);
```

## Relationships

### Foreign Key Relationships:

1. **tickets.user_id → users.id**
   - Each ticket belongs to one user (creator)
   - One user can have multiple tickets

2. **tickets.assigned_to → users.id**
   - Each ticket can be assigned to one admin/super admin
   - One admin can have multiple assigned tickets

3. **ticket_comments.ticket_id → tickets.id**
   - Each comment belongs to one ticket
   - One ticket can have multiple comments
   - CASCADE DELETE: Comments are deleted when ticket is deleted

4. **ticket_comments.user_id → users.id**
   - Each comment belongs to one user (author)
   - One user can author multiple comments

5. **attachments.ticket_id → tickets.id**
   - Each attachment belongs to one ticket
   - One ticket can have multiple attachments
   - CASCADE DELETE: Attachments are deleted when ticket is deleted

### Email Notification Integration:
The `tickets.assigned_by` field enables automatic email notifications when Super Admins assign tickets to users. The email functionality is handled by the application layer using SMTP configuration stored in environment variables.

## Database Setup Commands

### Initial Table Creation:

```sql
-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_admin BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    system_name VARCHAR(100),
    profile_image VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tickets table
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    user_name VARCHAR(100) NOT NULL,
    user_ip_address VARCHAR(45),
    user_system_name VARCHAR(100),
    image_filename VARCHAR(255),
    user_id INTEGER NOT NULL REFERENCES users(id),
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

ALTER TABLE tickets ADD COLUMN assigned_by INTEGER REFERENCES users(id);

-- Create Ticket Comments table
CREATE TABLE ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

UPDATE users SET role = 'user' WHERE role = 'User';
UPDATE users SET role = 'admin' WHERE role = 'Admin';
UPDATE users SET role = 'super_admin' WHERE role = 'Superadmin';
```

### Create Indexes for Performance:

```sql
-- Users table indexes
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Tickets table indexes
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);

-- Ticket Comments table indexes
CREATE INDEX idx_ticket_comments_ticket_id ON ticket_comments(ticket_id);
CREATE INDEX idx_ticket_comments_user_id ON ticket_comments(user_id);
CREATE INDEX idx_ticket_comments_created_at ON ticket_comments(created_at);
```

### Add Trigger for Updated Timestamp:

```sql
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for tickets table
CREATE TRIGGER update_tickets_updated_at 
    BEFORE UPDATE ON tickets 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

## Sample Data Insertion

### Create Default Admin Users:

```sql
-- Super Admin User
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_admin) 
VALUES ('superadmin', 'admin@gtnengineering.com', 'hashed_password_here', 'Super', 'Admin', 'super_admin', true);

-- Regular Admin User
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_admin) 
VALUES ('admin', 'support@gtnengineering.com', 'hashed_password_here', 'Admin', 'User', 'admin', true);

-- Sample Regular User
INSERT INTO users (username, email, password_hash, first_name, last_name, department) 
VALUES ('jdoe', 'john.doe@gtnengineering.com', 'hashed_password_here', 'John', 'Doe', 'Engineering');
```

### Sample Ticket Data:

```sql
-- Sample Hardware Ticket
INSERT INTO tickets (title, description, category, priority, user_name, user_id, created_at) 
VALUES ('Computer Won\'t Start', 'My workstation computer will not power on after the weekend.', 'Hardware', 'High', 'John Doe', 3, CURRENT_TIMESTAMP);

-- Sample Software Ticket
INSERT INTO tickets (title, description, category, priority, user_name, user_id, created_at) 
VALUES ('Email Client Issues', 'Outlook keeps crashing when trying to send emails with attachments.', 'Software', 'Medium', 'John Doe', 3, CURRENT_TIMESTAMP);
```

## Data Validation Rules

### Users Table:
- Username: 3-80 characters, unique
- Email: Valid email format, unique
- Password: Minimum 6 characters (hashed)
- Names: 2-50 characters each
- Role: Must be 'user', 'admin', or 'super_admin'

### Tickets Table:
- Title: 5-200 characters
- Description: Minimum 10 characters
- Category: Must be 'Hardware' or 'Software'
- Priority: Must be 'Low', 'Medium', 'High', or 'Critical'
- Status: Must be 'Open', 'In Progress', 'Resolved', or 'Closed'

### Comments Table:
- Comment: Minimum 5 characters

## Backup and Maintenance

### Regular Backup Command:
```bash
pg_dump -h localhost -U username -d gtn_helpdesk > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Database Statistics Query:
```sql
SELECT 
    'Users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 
    'Tickets' as table_name, COUNT(*) as record_count FROM tickets
UNION ALL
SELECT 
    'Comments' as table_name, COUNT(*) as record_count FROM ticket_comments;
```

### Ticket Statistics Query:
```sql
SELECT 
    status,
    COUNT(*) as ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM tickets 
GROUP BY status
ORDER BY ticket_count DESC;
```

## Migration Notes

- **Image Upload Feature**: Added `image_filename` column to tickets table (June 23, 2025)
- **Category Updates**: Removed 'Network' and 'Other' categories, keeping only 'Hardware' and 'Software'
- **System Tracking**: Enhanced user system information capture for better support context

## Security Considerations

1. **Password Security**: All passwords are hashed using Werkzeug's security functions
2. **File Upload Security**: Image uploads are validated and stored securely
3. **Access Control**: Role-based permissions enforced at application level
4. **SQL Injection Protection**: All queries use parameterized statements via SQLAlchemy ORM

## Performance Optimization

1. **Indexes**: Strategic indexing on frequently queried columns
2. **Foreign Key Constraints**: Proper relationships with referential integrity
3. **Cascade Deletes**: Automatic cleanup of related records
4. **Timestamp Triggers**: Automatic update timestamp management

---

**Last Updated**: June 23, 2025  
**Database Version**: PostgreSQL 13+  
**Application**: GTN Engineering IT Helpdesk System
