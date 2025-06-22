# Django Signals and ORM Project

## Overview

This Django project demonstrates how to use **signals**, **custom model managers**, and **ORM techniques** in a chat-like messaging app.

## Features

- **Message Editing**

  - Tracks message edits and stores history using `MessageHistory` model.
  - `pre_save` signal logs content changes.

- **Notification System**

  - Automatically creates a notification whenever a new message is sent.
  - Done using the `post_save` signal.

- **Admin Integration**
  - Admin panel includes `Message`, `MessageHistory`, and `Notification`.

## Technologies

- Python 3.x
- Django 4.x
- SQLite (default database)

## Setup Instructions

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install Django
pip install django

# Migrate database
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```
