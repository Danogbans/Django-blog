# Django Pro Blog

A full-featured blog application built with Django. This application includes user authentication, post creation, editing and deletion functionalities, comment sections, likes, a rich text editor for writing posts, tagging functionality, and more.

## Images

![Blog-post-paginator image](https://github.com/Danogbans/Django-blog/blob/main/blog-post-pagination.png)
**Post list and paginator** 

![Blog-post-paginator image](https://github.com/Danogbans/Django-blog/blob/main/search-function.png)
**Search functionality** 

![Blog-post-paginator image](https://github.com/Danogbans/Django-blog/blob/main/tagged-post.png)
**Tagging functionality** 


## Features

- **User Authentication**: 
  - User registration, login, and logout.
  - Secure password storage and authentication using Django's built-in authentication system.
  
- **Blog Posts**:
  - Create, edit, and delete posts.
  - Rich text editor for writing posts.
  - Slug generation for SEO-friendly URLs.
  - Display posts in a paginated list.
  - Tagging functionality to categorize posts.

- **Comments**:
  - Add comments to posts.
  - Manage comments (approve/delete) from the admin interface.

- **Likes**:
  - Users can like posts.

- **Search**:
  - Full-text search functionality to find posts.

- **Admin Interface**:
  - Manage users and blog content from the Django admin interface.

## Setup Instructions

### Prerequisites

- Python 3.6+
- Django 3.1+
- PostgreSQL (for full-text search)
- HTML5, Bootstrap4

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/your-username/django-pro-blog.git
    cd django-pro-blog
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    Ensure PostgreSQL is installed and running. Create a new database:

    ```sh
    psql -U postgres
    CREATE DATABASE django_pro_blog;
    ```

    Update `settings.py` with your database configuration.

5. **Run migrations**:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser**:

    ```sh
    python manage.py createsuperuser
    ```

7. **Collect static files**:

    ```sh
    python manage.py collectstatic
    ```

8. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

### Usage

1. **Access the admin interface**:

    Navigate to `http://127.0.0.1:8000/admin` and log in with the superuser credentials.

2. **Create a new post**:

    Use the admin interface to create, edit, and manage blog posts.

3. **Visit the blog**:

    Navigate to `http://127.0.0.1:8000/blog` to view the list of blog posts.

4. **Register and login**:

    Register a new user account or log in with an existing account to create posts, like posts, and add comments.

### Testing

Run the tests to ensure everything is working correctly:

```sh
python manage.py test
```

### Deployment

To deploy this project, you'll need to set up a web server (e.g., Gunicorn, Nginx) and configure your database and static files for production use. Refer to the Django deployment checklist for more details.

### Contributing
Feel free to submit issues and pull requests. For major changes, please open an issue first to discuss what you would like to change.
