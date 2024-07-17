# Online Judge Primary Backend

Welcome to the Online Judge Backend repository! This project is designed to provide a scalable, secure, and efficient backend for an online coding platform where users can solve listed problems in various programming languages, similar to platforms like LeetCode.

Here is the link to the external [judge server](https://github.com/AbhishekBhosale46/OnlineJudge-JudgeServer) used for code evaluation.

## Features

- **Problem Management**: CRUD operations for creating coding problems including problem description, constraints, and sample test cases.

- **Problem Listing**: Users can browse and select problems to solve.

- **Code Submission**: Users can submit their code in various programming languages including C++, Java, and Python.

- **Web Hook Callback**: Implements a webhook mechanism to receive task completion statuses from an external judge server.

- **Real-Time Feedback**: The system provides immediate feedback on code submissions, including appropriate verdicts

## Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Primary Backend DB Diagram](https://github.com/user-attachments/assets/1ab962c1-a585-43dc-93d9-1c86f518ac3f)


## Installation

Clone the project

```bash
git clone https://github.com/AbhishekBhosale46/OnlineJudge-JudgeServer
```

Install dependencies

```bash
pip install requirements.txt
```

Make migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the dev server

```bash
python manage.py runserver
```
