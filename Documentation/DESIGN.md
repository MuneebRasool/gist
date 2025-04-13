# GTPS (Generalized Task Prioritization System) Design Documentation

## Table of Contents
- [1. System Overview](#1-system-overview)
- [2. Architecture Components](#2-architecture-components)
- [3. API Design](#3-api-design)
- [4. Data Models](#4-data-models)
- [5. Deployment Architecture](#5-deployment-architecture)
- [6. Security Considerations](#6-security-considerations)
- [7. Monitoring and Observability](#7-monitoring-and-observability)
- [8. Testing Strategy](#8-testing-strategy)
- [9. Future Considerations](#9-future-considerations)

## 1. System Overview

GIST is a task management system that processes various data sources to create prioritized, actionable tasks. The system follows a modular architecture with clear separation of concerns.

### Core Value Proposition
- Automated task extraction from multiple data sources
- Intelligent prioritization based on user context
- Adaptive learning from user behavior
- Scalable and extensible architecture

## 2. Architecture Components

### 2.1 User Onboarding Flow

The onboarding flow is designed to create a seamless user experience while building a comprehensive understanding of the user's email patterns and task management needs. Here's a detailed breakdown of each step:

#### Initial Flow
1. **User Onboarding**
   - User signs up and creates their account
   - Sets up i
   
2. **Email Integration with Nylas**
   - Connects to user's email account via Nylas API
   - Fetches and processes emails from the last 3-4 weeks
   - Selects the top 5 most important emails to show to user for triaging


3. **Domain Inference Agent**
   - Analyzes initial email dataset which user have rated
   - Identifies important domains and stakeholders, user's preferences
   - Creates a network map of professional relationships
   - Understands organizational context and hierarchy
   - Asks 5 questions to user based on his sent emails to understand user in detail.

4. **Personality Generation**
   - Analyzes the user's domain, rated emails, and answered questions to generate the initial personality profile
   - Allows users to review and edit their persona if needed

5. **Task Extraction**
   - Extracts emails from the last 2 weeks
   - Processes email content using natural language processing
   - Identifies action items and potential tasks
   - Tasks are processed by feature agents to extract utility and cost features

   **Utility Features:**
   - Priority (1-10 scale)
   - Deadline time (calculated via tool)
   - Intrinsic interest (high/moderate/low)
   - User emphasis (high/low)
   - Task type relevance (high/medium/low)
   - Emotional salience (strong/weak)
   - Domain relevance (high/low)
   - Novel task (high/low)
   - Reward pathways (yes/no)
   - Time of day alignment (appropriate/inappropriate)
   - Learning opportunity (high/low)
   - Urgency (1-10 scale)

   **Cost Features:**
   - Task complexity (1-5 scale)
   - Time required (hours)
   - Emotional stress factor (high/medium/low)
   - Location dependencies (count/none)
   - Resource requirements (count/none)
   - Interruptibility (high/low)

   **Scoring Process:**
   - Utility and cost prediction SGD models calculate respective scores
   - Relevance score is calculated using formula: alpha * utility score - beta * cost score
   - All data is saved in relational database and graph database
   - UI displays top 5 emails for user triaging

#### Task Processing Flow
5. **Q&A Agent**
   - Interacts with users to clarify task details
   - Gathers additional context when needed
   - Helps refine task priorities and deadlines
   - Feeds information to User Story Agent

6. **User Story Agent**
   - Transforms extracted information into structured user stories
   - Creates task narratives with clear context
   - Shows UI where user can add more details once confirmed
   - Prepares stories for task extraction

7. **Content Classification Agent**
   - Categorizes tasks based on type and domain
   - Applies machine learning models for classification
   - Identifies task patterns and similarities
   - Stores classified emails temporarily for reference

8. **Task Extraction Agent**
   - Converts user stories into actionable tasks
   - Processes content fed from classification agent
   - Prepares tasks for scoring and prioritization
   - In prompt, will add final category/important task

9. **Utility/Cost/Relevance/Score Prediction**
   - Calculates task importance scores
   - Evaluates resource requirements
   - Predicts completion time and effort
   - Assigns priority levels based on multiple factors

10. **Task Management Interface**
    - Presents tasks in an organized dashboard
    - Shows domain-specific transactional messages
    - Shows domain reminder messages
    - Tasks are visible in the waiting state

This flow ensures that emails are not just processed, but transformed into meaningful, actionable tasks while maintaining context and relationships. The system continuously learns from user interactions to improve task classification and prioritization over time.

## 5. Deployment Architecture

### 5.1 Services
- Frontend: Next.js application
- Backend API: FastAPI service in Docker containers
- Database: Neo4j instance for graph data, Postgres instance for general data
- OpenAI LLMs for emails processing. 

## 6. Security Considerations

### 6.1 Authentication
- JWT-based authentication
- OAuth2 for third-party integrations


### 6.2 Data Protection
- Encryption at rest for sensitive data
- Secure API keys management
- Regular security audits
- We do not store the user emails, emails are only fetched temporarily for task extraction process.

## 9. Future Considerations

### 9.1 Scalability Improvements
- Implement caching layer
- Add support for batch processing
- Optimize database queries
- message queue to process user email

### 9.2 Feature Enhancements
- Additional data source integrations
- Advanced ML models for better prediction
- Mobile app development
- Real-time collaboration features 