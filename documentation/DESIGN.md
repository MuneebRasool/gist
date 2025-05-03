# Gist: Task Management Powered by AI and Math

This document explains how Gist works at a high level.

## 1. Overview

Gist is an intelligent task management system designed to reduce digital overload. It extracts, organizes, and prioritizes tasks using AI.

### Key Features

* **Auto task extraction** from emails
* **Smart prioritization** based on context
* **Learns and adapts** over time
* **Scalable** for individuals or teams

## 2. How It Works

Gist uses a **dynamic graph** to manage tasks:

* Each task = a node
* Connections show relationships and dependencies
* Each task gets a **relevance score** that updates over time

**Relevance formula:**

```
Relevance = (Importance × α) – (Cognitive cost × β)
```

→ High importance and low effort = higher priority.

It also uses:

* **Task dependencies** to plan order
* **User feedback** to keep improving

## 3. Onboarding

When you sign up:

1. Connect your email
2. Gist analyzes recent emails to find tasks
3. You review suggested tasks
4. Gist builds your work profile
5. Tasks are organized and prioritized

## 4. System Architecture

* **Frontend:** Next.js
* **Backend:** FastAPI
* **Databases:** Neo4j (graph), PostgreSQL (data)
* **AI Models:** OpenAI LLMs for email processing

All components run in Docker.

## 5. Security

* OAuth2 + JWT authentication
* Data encryption
* Emails are processed temporarily (no permanent storage)

## 6. Monitoring

We monitor AI performance with Langfuse:

* Track token usage
* Debug AI issues
* Analyze response times
* Improve prompts

## 7. Future Plans

We plan to add:

* More integrations
* Better ML models for predictions
