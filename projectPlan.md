# Morning News AI Project Plan

## Goal
Build a mobile-first news dashboard that remembers my preferred topics and
sources, generates a balanced morning briefing, and avoids endless-scroll UI.

## MVP stack
- Frontend: React + Vite PWA (Porgressive Web App)
- Hosting: Firebase Hosting (from GCP)
- Authentication: Firebase Google Sign-In
- Backend: Python FastAPI on Cloud Run (from GCP)
- Database: Firestore (from GCP)
- AI: Gemini on Vertex AI
- Automation: Cloud Scheduler
- Secrets: Secret Manager
- Repository and CI/CD: GitHub

## Core workflow
1. Load saved user topics, sources, and briefing settings.
2. Retrieve recent articles from RSS feeds (XML output), APIs, and search fallbacks.
3. Normalize article metadata and canonical URLs.
4. Remove duplicate and near-duplicate stories.
5. Classify each article by topic, sentiment, and content type.
6. Rank by recency, relevance, source diversity, and user preference.
7. Select a configurable positive/negative/neutral mix.
8. Generate short factual summaries with source links.
9. Save the completed briefing in Firestore.
10. Display it in a simple mobile dashboard.

## Phase 1: Local prototype
- Create repository and Python environment.
- Define Article, Source, Topic, Preferences, and Briefing models.
- Add 3 topics and 3 trusted sources.
- Implement RSS/search retrieval.
- Implement deduplication and ranking.
- Generate one local Markdown or JSON briefing.
- Add tests for duplicate removal and sentiment balancing.

## Phase 2: Backend
- Create FastAPI endpoints:
  - GET /briefings/today
  - POST /briefings/generate
  - GET/PUT /preferences
  - POST /scheduler/generate
  - GET /health
- Store preferences and briefings in Firestore.
- Add Gemini summarization and classification.
- Validate citations and retain original article URLs.
- Containerize and deploy the API to Cloud Run.

## Phase 3: Mobile UI
- Create Today, Preferences, and History pages.
- Add topic and source toggles.
- Add briefing length and sentiment-balance controls.
- Add Refresh and Save as default actions.
- Make the app installable as a PWA.
- Deploy the frontend to Firebase Hosting.

## Phase 4: Authentication and automation
- Enable Firebase Google Sign-In.
- Associate preferences with the authenticated user ID.
- Create an authenticated Cloud Scheduler job.
- Generate the briefing 15 minutes before wake time.
- Make scheduled generation idempotent by user and date.
- Add email or push notification when the briefing is ready.

## Phase 5: Quality and safety
- Add source allowlists and domain validation.
- Add maximum stories per source and topic.
- Separate news, analysis, and opinion.
- Track sentiment confidence and allow neutral fallback.
- Add logs for retrieval, AI calls, failures, and costs.
- Store API credentials only in Secret Manager.
- Add a monthly budget alert.

## Later features
- Conversational follow-up questions using GCP ADK.
- Multiple briefing profiles, such as weekday and weekend.
- Feedback buttons to improve rankings.
- Audio briefing.
- Calendar and commute information.
- Native mobile notifications or alarm integration.
- Weekly trend summaries.
- Source credibility and viewpoint-diversity controls.
- Testing Automation

## MVP completion criteria
- Works from a mobile browser.
- Remembers topics and sources.
- Produces a daily briefing from at least 3 sources.
- Every summary links to the original article.
- Avoids duplicate stories.
- Supports configurable emotional balance.
- Automatically generates one briefing each morning.
``