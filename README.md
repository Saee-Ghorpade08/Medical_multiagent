# Medical Healthcare Multi-Agent Assistant — Assignment 10

Undergraduate GenAI & ML DevOps lab project for **even roll numbers**. This project includes a Streamlit user interface and a FastAPI API, powered by an Agno multi-agent team and the Groq API.

## Agents

1. **Healthcare Query Analyzer** — identifies the user's question and organizes the request.
2. **Medical Research Agent** — searches a small local library of educational sample notes and prepares an evidence-informed response.
3. **Medical Answer Reviewer** — reviews the draft for clarity, safety, unsupported certainty, and appropriate educational disclaimers.

The team coordinates the workflow. This is an educational demo, not a diagnostic or treatment tool. Do not enter personal health information. For urgent symptoms, contact local emergency services or a qualified healthcare professional.

## 1. Requirements

- Python 3.10 or 3.11 recommended
- A Groq API key: https://console.groq.com/keys
- Optional: Docker Desktop for containerization

## 2. Set up on Windows

Open Command Prompt in this folder:

```cmd
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set your actual `GROQ_API_KEY`. Keep `.env private; do not upload it to GitHub.

## 3. Run Streamlit UI

```cmd
streamlit run streamlit_app.py
```

Open the local URL printed in the terminal, usually http://localhost:8501.

## 4. Run FastAPI separately (optional)

Open a second terminal in this folder and activate the same environment:

```cmd
.venv\\Scripts\\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API docs: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health
- API POST endpoint: http://127.0.0.1:8000/ask

## 5. Run tests

```cmd
pytest -v
```

## 6. Docker

Ensure Docker Desktop is running and `.env` exists:

```cmd
docker compose up --build -d
docker compose ps
docker compose logs -f
```

Open http://localhost:8501. Stop with:

```cmd
docker compose down
```

## 7. Kubernetes starter manifests

The `k8s/` directory contains starter manifests. Update the image name to one available to your cluster, configure the Groq API key through a Kubernetes Secret, then apply the ConfigMap, Secret, Deployment, and Service. Do not commit a real API key.

## 8. GitHub Actions

`.github/workflows/ci.yml` runs the unit tests and builds the Docker image. Push the repository to GitHub (without `.env` or `.venv`) to trigger the workflow.
