# 🍳 Recipe Management App

## 📋 Overview
A full-stack recipe management application that allows users to create, share, and manage their personal recipe collections. The app features user authentication, personal recipe management, and a community aspect where users can browse recipes from other members.

## 🛠️ Technical Stack

### 🐍 Backend (Flask)
- **Framework**: Flask with Python
- **Database**: SQLite with SQLAlchemy ORM 🗄️
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended 🔐
- **Security**: Werkzeug password hashing, CORS enabled 🛡️
- **Architecture**: Blueprint-based modular design 🏗️

### ⚛️ Frontend
- **Framework**: React (developed in VS Code) 💻
- **Communication**: REST API integration with Flask backend 🔗

## ✨ Core Features

### 🔑 Authentication System
- **User Registration**: Secure account creation with unique usernames 📝
- **User Login**: JWT token-based authentication 🎫
- **Password Security**: Bcrypt hashing for secure password storage 🔒
- **Session Management**: Token-based authentication for protected routes ⏱️

### 📖 Recipe Management
- **Public Recipe Browsing**: View all recipes from the community without authentication 🌍
- **Personal Recipe Collection**: Authenticated users can view only their own recipes 👤
- **Recipe Creation**: Add new recipes with title, ingredients, and instructions ➕
- **Recipe Editing**: Update existing recipes (owner-only access) ✏️
- **Recipe Deletion**: Remove recipes from personal collection (owner-only access) 🗑️
- **Recipe Details**: View detailed information for specific recipes 🔍

### 🛡️ Security Features
- **Ownership Verification**: Users can only edit/delete their own recipes ✅
- **Protected Endpoints**: JWT authentication required for sensitive operations 🚪
- **Input Validation**: JSON data validation and error handling ⚠️
- **Cross-Origin Resource Sharing**: CORS configured for frontend-backend communication 🌐

## 🏗️ Database Schema

### 👤 User Model
- Unique user identification system 🆔
- Secure password storage with hashing 🔐
- One-to-many relationship with recipes 🔗

### 📝 Recipe Model
- Comprehensive recipe storage (title, ingredients, instructions) 📊
- Foreign key relationship linking recipes to their creators 🔗
- Support for detailed cooking instructions and ingredient lists 📋

## 🌐 API Endpoints

### 🔑 Authentication Routes (`/auth`)
- `POST /auth/register` - User registration 📝
- `POST /auth/login` - User authentication 🚪

### 🍽️ Recipe Routes (`/api`)
- `GET /api/recipes` - Get all public recipes 📖
- `POST /api/add` - Create new recipe (authenticated) ➕
- `GET /api/myrecipes` - Get user's personal recipes (authenticated) 👤
- `GET /api/recipes/<id>` - Get specific recipe details (authenticated) 🔍
- `PUT /api/recipes/<id>` - Update recipe (owner only) ✏️
- `DELETE /api/recipes/<id>` - Delete recipe (owner only) 🗑️

## 💻 Development Environment
- **Backend IDE**: PyCharm for Flask development 🐍
- **Frontend IDE**: VS Code for React development ⚛️
- **Database**: SQLite for development (easily configurable for production databases) 🗄️
- **Environment Management**: dotenv for configuration management ⚙️

## 🚀 Key Technical Highlights
- **Modular Architecture**: Blueprint-based organization separating authentication and recipe functionality 🏗️
- **RESTful API Design**: Standard HTTP methods and status codes 📡
- **Comprehensive Error Handling**: Database rollback mechanisms and 404 handling ⚠️
- **Scalable Database Design**: Proper foreign key relationships and indexing 📈
- **Security-First Approach**: Authentication, authorization, and input validation throughout 🛡️

## 🎯 Use Cases
- Personal recipe organization and storage 📚
- Recipe sharing within a community 👥
- Secure multi-user recipe management 🔐
- CRUD operations with proper ownership controls ✅

This application demonstrates full-stack development best practices with a clean separation of concerns, robust security implementation, and a user-friendly recipe management system suitable for both personal use and community recipe sharing. 🌟
