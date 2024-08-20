# TODO Web Application


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)


## Introduction

Welcome to the TODO Web Application! This is a Django-based project that allows users to manage their tasks and stay organized. The application provides a user-friendly interface to add, edit, and mark tasks as completed.

## Features

- User authentication: Register and log in to access your personalized TODO list.
- Add tasks: Easily add new tasks with a title, description, and due date.
- Edit tasks: Modify task details such as title, description, and due date.
- Mark tasks as completed: Keep track of your progress by marking completed tasks.
- Filter tasks: Filter tasks based on completion status or due date or priority to find what you need quickly.
- RESTful APIs: Utilizes Django Rest Framework (DRF) for easy integration with external applications.(not completed yet)

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/todo-app.git
```

2. Navigate to the project directory:

```bash
cd todo-app
```

3. Create a virtual environment (recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

```bash
source env/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run database migrations:

```bash
python manage.py migrate
```
7. Start the development server:


```bash
python manage.py runserver
```


## Usage

1. Visit the application in your web browser.
2. Register a new account or log in with your existing credentials.
3. Add new tasks by clicking on the "Add Task" button and filling out the form.
4. Edit or delete tasks by clicking on the respective task's edit or delete icon.
5. Mark tasks as completed by clicking on the checkbox next to each task.

### API Endpoints (For developers)

not completed yet.


## Technologies Used

- Python
- Django
- Django Rest Framework (DRF)
- HTML
- CSS
- JavaScript
- SQLite (for development)

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.


