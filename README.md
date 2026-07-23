# Morning News AI
A mobile-first AI news aggregator that generates a personalized morning briefing using saved topics, trusted sources, thematic analysis, and a configurable mix of constructive, adverse, and neutral stories.

## Current phase

Phase 1: LOcal prototype

## Comprehension requirements

Technologies in use: FastAPI (pythong web framework)
GCP Servies: Firestore

## Version requirements

Python Version: 3.12.10

## Setup

1. create and activate a python virtual environment (venv):
python -m venv .venv
.\.venv\Scripts\activate.ps1 #Windows Powershell

To deactivate a python venv:
deactivate

2. install project and development dependencies from pyproject.toml in venv:
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

## Operations and Commandflows

- To run tests (make sure this is passing 100% before commiting):
pytest

- To check formatting and linting (make sure at least the first command passes 100% before pushing):
ruff check .
ruff format --check .

- To reformat files to the correct standard structure
ruff format .

- To commit local cahnges to the remote repo:
git status
git pull 
git pull origin master
git add .
git commit -m "example commit message"
git push

- To reinstall the project if dependencies change
python -m pip install -e ".[dev]"

## Models (increeasing by complexity)

from backend.models.common import (BriefingStatus, ContentType, RetrievalMethod, SentimentLabel)
from backend.models.source import NewsSource
from backend.models.topic import NewsTopic
from backend.models.article import Article
from backend.models.preferences import SentimentMix, UserPreferences
from backend.models.briefing import (Briefing, BriefingItem, ThemeSummary, TopicSummary)