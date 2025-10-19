🍳 Cerr's Recipes - Recipe Management API
A full-stack recipe management application built with Django REST Framework and vanilla JavaScript. 
Users can create, manage, and discover recipes, with integration to TheMealDB API for importing thousands of recipes.



✨ Features
Core Functionality
🔐 User Authentication - JWT-based registration and login
📝 Recipe CRUD Operations - Create, read, update, and delete recipes
🔍 Advanced Search & Filtering - Search by title, ingredients, or category
📁 Category Management - Organize recipes by categories
👤 User Recipe Management - Each user can manage their own recipes
TheMealDB Integration
🌐 Recipe Discovery - Search and browse recipes from TheMealDB
📥 Import Recipes - One-click import from external API
🎲 Random Recipe - Get random recipe suggestions
🖼️ Rich Media - Images, video tutorials, and source links
🔄 Bulk Import - Admin feature to populate database quickly
User Interface
💅 Beautiful Gradient Design - Modern purple gradient theme
📱 Responsive Layout - Works on desktop, tablet, and mobile
🎨 Interactive Cards - Hover effects and smooth animations
🖼️ Recipe Images - Display thumbnails and full images
🎥 Video Tutorials - Links to YouTube cooking videos
🚀 Quick Start
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Internet connection (for TheMealDB API)
Installation
Clone or Download the Project
bash
mkdir cerrs_recipes
cd cerrs_recipes
Create Virtual Environment
bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
Install Dependencies
bash
pip install django djangorestframework djangorestframework-simplejwt django-filter requests
Create Django Project
bash
python -m django startproject recipe_project
cd recipe_project
python manage.py startapp accounts
python manage.py startapp recipes
Configure Settings
Update recipe_project/settings.py:

python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'accounts',
    'recipes',
]

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MEALDB_API_BASE_URL = 'https://www.themealdb.com/api/json/v1/1'

Setup Database
bash
python manage.py makemigrations
python manage.py migrate
Create Superuser
bash
python manage.py createsuperuser
Seed Database (Optional)
bash
# Import 20 recipes from TheMealDB
python manage.py seed_recipes --count=20
Run Development Server
bash
python manage.py runserver
Access the Application
Frontend: http://localhost:8000/
API: http://localhost:8000/api/
Admin Panel: http://localhost:8000/admin/

📁 Project Structure
recipe_project/
├── manage.py
├── db.sqlite3
├── templates/
│   └── index.html                 # Frontend UI
├── accounts/                       # Authentication app
│   ├── models.py                  # Custom User model
│   ├── serializers.py             # User serializers
│   ├── views.py                   # Auth views
│   └── urls.py                    # Auth endpoints
├── recipes/                        # Recipe management app
│   ├── models.py                  # Recipe & Category models
│   ├── serializers.py             # Recipe serializers
│   ├── views.py                   # Recipe views
│   ├── filters.py                 # Search & filter logic
│   ├── services.py                # TheMealDB integration
│   ├── urls.py                    # Recipe endpoints
│   ├── admin.py                   # Admin configuration
│   └── management/
│       └── commands/
│           └── seed_recipes.py    # Database seeding
└── recipe_project/                 # Project settings
    ├── settings.py
    ├── urls.py
    └── wsgi.py
    
🔌 API Endpoints
Authentication
Endpoint	Method	Description
/api/register/	POST	Register new user
/api/login/	POST	Login and get JWT token
/api/token/refresh/	POST	Refresh access token

Recipes
Endpoint	Method	Description	Auth Required
/api/recipes/	GET	List all recipes	No
/api/recipes/	POST	Create new recipe	Yes
/api/recipes/{id}/	GET	Get recipe details	No
/api/recipes/{id}/	PUT	Update recipe	Yes (Owner)
/api/recipes/{id}/	DELETE	Delete recipe	Yes (Owner)
/api/recipes/my_recipes/	GET	Get user's recipes	Yes
/api/recipes/?category=breakfast	GET	Filter by category	No
/api/recipes/?ingredient=chicken	GET	Search by ingredient	No
/api/recipes/?search=pasta	GET	Full text search	No

TheMealDB Integration
Endpoint	Method	Description	Auth Required
/api/recipes/search_mealdb/?q=chicken	GET	Search TheMealDB	Yes
/api/recipes/random_mealdb/	GET	Get random recipe	Yes
/api/recipes/import_from_mealdb/	POST	Import single recipe	Yes
/api/recipes/bulk_import_mealdb/	POST	Bulk import recipes	Admin

Categories
Endpoint	Method	Description	Auth Required
/api/categories/	GET	List all categories	No
/api/categories/	POST	Create category	Admin
/api/categories/{id}/	PUT	Update category	Admin
/api/categories/{id}/	DELETE	Delete category	Admin
/api/categories/sync_from_mealdb/	GET	Sync from TheMealDB	Admin

📝 API Usage Examples
Register User
bash
POST /api/register/
Content-Type: application/json

{
    "username": "john",
    "email": "john@example.com",
    "password": "secure123",
    "password2": "secure123"
}
Login
bash
POST /api/login/
Content-Type: application/json

{
    "username": "john",
    "password": "secure123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
Create Recipe
bash
POST /api/recipes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Spaghetti Carbonara",
    "description": "Classic Italian pasta",
    "ingredients": "400g spaghetti, 200g bacon, 4 eggs, 100g parmesan, black pepper",
    "steps": "1. Boil pasta\n2. Fry bacon\n3. Mix eggs with cheese\n4. Combine all ingredients",
    "prep_time": 30,
    "category": 1
}
Import from TheMealDB
bash
POST /api/recipes/import_from_mealdb/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "meal_id": "52772"
}
💻 Management Commands
Seed Database
bash
# Import 20 recipes
python manage.py seed_recipes

# Import 50 recipes
python manage.py seed_recipes --count=50

# Import 100 recipes
python manage.py seed_recipes --count=100
This command will:

Create a mealdb_importer user
Import all categories from TheMealDB
Fetch and import random recipes
Skip duplicates automatically
Show progress in terminal
🎨 Frontend Features
Tabs
Browse Recipes - View all recipes with search and filter
Discover from MealDB - Search and import external recipes
My Recipes - Manage your own recipes (login required)
Create Recipe - Add new recipes (login required)
Key Functions
Real-time search
Category filtering
Recipe cards with images
Modal detail views
One-click import
Video tutorial links
Responsive design
🛠️ Technologies Used
Backend
Django 5.0+ - Web framework
Django REST Framework - API development
djangorestframework-simplejwt - JWT authentication
django-filter - Advanced filtering
requests - HTTP library for API calls
Frontend
Vanilla JavaScript - No frameworks needed
HTML5 & CSS3 - Modern web standards
Fetch API - Async data fetching
External APIs
TheMealDB API - Recipe data source
Free tier: https://www.themealdb.com/api.php
🐛 Troubleshooting
Common Issues
1. ModuleNotFoundError: No module named 'rest_framework'

bash
pip install djangorestframework djangorestframework-simplejwt django-filter requests
2. No module named 'static' or 'templates'

Remove 'static' and 'templates' from INSTALLED_APPS in settings.py
3. TheMealDB Connection Error

Error: Failed to resolve 'www.themealdb.com'
Solutions:

Check internet connection
Flush DNS: ipconfig /flushdns (Windows)
Try different network
Temporarily disable firewall
4. CORS Issues (if running frontend separately)

bash
pip install django-cors-headers
Add to settings.py:

python
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOW_ALL_ORIGINS = True  # Development only
5. Migration Errors

bash
# Delete db.sqlite3 and migrations folders (except __init__.py)
python manage.py makemigrations
python manage.py migrate
📚 Database Schema
User Model
python
- username (CharField, unique)
- email (EmailField, unique)
- password (CharField, hashed)
Category Model
python
- name (CharField, unique)
- created_at (DateTimeField)
Recipe Model
python
- title (CharField)
- description (TextField)
- ingredients (TextField)
- steps (TextField)
- prep_time (IntegerField)
- category (ForeignKey -> Category)
- created_by (ForeignKey -> User)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- mealdb_id (CharField, optional)
- thumbnail_url (URLField, optional)
- video_url (URLField, optional)
- source_url (URLField, optional)
🔒 Security Features
JWT-based authentication
Password hashing with Django's built-in system
CSRF protection
User-specific recipe ownership
Admin-only category management
SQL injection protection (Django ORM)
🚀 Deployment Tips
For Production
Update settings.py
python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

Use PostgreSQL
python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipe_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Static Files
bash
python manage.py collectstatic
Use Production Server
Gunicorn for WSGI
Nginx for reverse proxy



📧 Contact
Project Creator: Cerr178
Project Link: https://github.com/Cerr1738/Cerrs-Recipes-.git

🙏 Acknowledgments
Django - Web framework
Django REST Framework - API toolkit
TheMealDB - Recipe API
Simple JWT - Authentication

Made with ❤️ by Cerr | Happy Cooking! 🍳

