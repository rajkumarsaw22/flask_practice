# Student Registration System

A simple **Flask** web application to manage student records with **MongoDB** as the backend database. Users can **add, view, update, and delete** student details.

---

## Features

* List all students on the home page
* Add a new student
* Update existing student details
* Delete a student with confirmation
* Simple and responsive UI using Bootstrap

---

## Tech Stack

* **Backend:** Python, Flask
* **Database:** MongoDB (via Flask-PyMongo)
* **Frontend:** HTML, Jinja2 templates, Bootstrap 5
* **Environment Variables:** Managed via `.env` file

---

## Setup Instructions


### 1. Clone the repository

```bash
git clone https://github.com/rajkumarsaw22/flask_Practice
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
# Linux / Mac:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` example:**

```
Flask
Flask-PyMongo
python-dotenv
bson
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
MONGO_URI=<your-mongodb-connection-string>
SECRET_KEY=<your-secret-key>
```

### 5. Run the application

```bash
python app.py
```

Open your browser at: [http://localhost:8000](http://localhost:8000)

---

## Project Structure

```
project/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   ├── update_student.html
├── app.py
├── requirements.txt
└── .env
```

---

## GitHub Actions CI/CD Pipeline

This project also ships a GitHub Actions workflow at [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) that mirrors the Jenkins pipeline below, natively on GitHub.

### Triggers

| Event | Branches / Refs | Jobs that run |
|---|---|---|
| `push` | `main`, `staging` | test → build → deploy-staging (staging only) |
| `push` (tag) | `v*` (e.g. `v1.0.0`) | test → build → deploy-production |
| `pull_request` | targeting `main`, `staging` | test only |

### Jobs

1. **test** – Checks out the code, sets up Python 3.12, installs `requirements.txt`, and runs `pytest` (with `ENABLE_DB=false` so the suite doesn't need a live MongoDB instance). Publishes a JUnit test report as a workflow artifact.
2. **build** – Runs only after `test` passes, and only on pushes (not PRs). Packages the repository into `build/flask_practice.zip` and uploads it as a build artifact.
3. **deploy-staging** – Runs only on a push to the `staging` branch. Uses [`appleboy/ssh-action`](https://github.com/appleboy/ssh-action) to SSH into the staging server, pull the latest `staging` branch, reinstall dependencies, write `.env` from secrets, and restart `app.py`. Gated behind the `staging` [GitHub Environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment).
4. **deploy-production** – Runs only when a tag matching `v*` is pushed (i.e. a release). SSHes into the production server, checks out the tagged commit, reinstalls dependencies, writes `.env`, and restarts `app.py`. Gated behind the `production` GitHub Environment.

### Configuring secrets

Add these under **Settings → Secrets and variables → Actions → New repository secret** (or as Environment secrets under `staging` / `production` for stricter access control):

| Secret | Used by | Description |
|---|---|---|
| `MONGO_URI` | deploy-staging, deploy-production | MongoDB connection string written to the server's `.env` |
| `SECRET_KEY` | deploy-staging, deploy-production | Flask session secret key |
| `STAGING_HOST` | deploy-staging | Hostname/IP of the staging server |
| `STAGING_USER` | deploy-staging | SSH username on the staging server |
| `STAGING_SSH_KEY` | deploy-staging | Private SSH key with access to the staging server |
| `PROD_HOST` | deploy-production | Hostname/IP of the production server |
| `PROD_USER` | deploy-production | SSH username on the production server |
| `PROD_SSH_KEY` | deploy-production | Private SSH key with access to the production server |

To create a `staging` [Environment](https://github.com/settings) with its own secrets/approval rules: **Settings → Environments → New environment**, name it `staging` (and repeat for `production`).

### Triggering a deployment

* **Staging:** push (or merge) to the `staging` branch.
* **Production:** create and push a release tag, e.g.:

  ```bash
  git tag v1.0.0
  git push origin v1.0.0
  ```

  or cut a GitHub Release through the UI, which creates the tag automatically.

---

## Jenkins CI/CD Pipeline

This project uses a Jenkins CI/CD pipeline executed on a central Jenkins server.

### Jenkins Server
https://jenkinsacademics.herovired.com/

### Pipeline Stages
1. Build – Install Python dependencies
2. Test – Run unit tests using pytest
3. Deploy – Simulated deployment to staging environment







