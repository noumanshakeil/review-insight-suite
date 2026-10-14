# Dev server for review-insight-suite
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
