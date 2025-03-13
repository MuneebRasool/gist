# Onboarding Workflow

## Overview
The onboarding process involves integrating the user's email, analyzing their emails, and generating a personality-based task list. Below is the improved step-by-step workflow.

## Steps

### 1. User Email Integration
- The user signs up with Nylas, generating a grant ID.
- The user connects their email account.
- The frontend fetches 15 recent emails from the user's inbox.
- Spam detection is applied, removing the top 5 spam emails.
- The remaining 10 emails are sent to the user for importance ranking.

### 2. Email Marking
- The user ranks the 10 emails based on importance.
- The marked emails are sent to the backend for analysis.

### 3. Question Generation
- The backend analyzes the marked emails and the user’s email domain.
- It generates relevant questions tailored to the user’s email activity.
- These questions are sent to the frontend.

### 4. User Question Response
- The user answers the generated questions.
- The frontend submits the marked emails, questions, and answers to the backend.

### 5. Personality Generation
- The backend processes the submitted data to generate an initial personality profile.
- It creates a list of 10 personality points based on the user’s email behavior and responses.
- This personality data is stored in the system.

### 6. Task Generation
- Based on the personality and email content, the backend generates personalized tasks.
- Task generation runs in the background.

## Frontend Flow
1. **Welcome Message** – The user is introduced to the process and integrates their email.
2. **Email Marking (`/app/mark-emails`)** – The user ranks 10 emails in order of importance.
3. **Onboarding (`/app/onboarding`)** – The user answers the generated questions.
4. **Dashboard (`/app/dashboard`)** – The user sees their generated tasks.

## Implementation Notes
- When the user integrates their email with Nylas, they are redirected to `/app/mark-emails`.
- The backend fetches 15 emails, filters out spam, and returns 10 emails.
- After the user ranks the emails, the backend generates relevant questions.
- Once the user submits their answers, the system finalizes the personality profile.
- Background tasks are then triggered based on the user’s personality.

## Affected Files

### Web
- `/app/onboarding/page.tsx`
- `/app/mark-emails/page.tsx`
- `/store/task.ts`
- `/services/nylas/email.service.ts`
- `/components/onboarding/WelcomeMessage`
- `/service/agent/agent.service.ts`

### Server
- `/src/modules/agent/*`
- `/src/modules/nylas/*`

## Backend Service Changes

### New and Modified Functions in `service.py`

1. **Function to Generate and Store Initial Personality**
   - This function will process the user’s email domain and any available data to generate an initial personality profile.
   - The generated personality will be stored in the system for further refinement.

2. **Function to Fetch and Filter Emails**
   - A new function will be created to fetch 15 emails from Nylas.
   - It will apply spam detection, removing the top 5 spam emails.
   - The remaining 10 emails will be sent to the frontend for importance marking.
   - Currently, `/api/nylas/email/messages` performs a similar task, but it does not filter spam. This new function will handle spam filtering.

3. **Modification of `async def infer_user_domain(self, email: str)`**
   - This function will be repositioned to run after email marking.
   - It will now receive the 10 marked emails alongside the email domain.
   - Based on these inputs, it will generate user-specific questions and answers.

4. **Reuse of the Final Onboarding Submission Function**
   - The final onboarding submission function, which takes `emails + questions/answers` as input, can be reused with minimal modifications.

This refined workflow and service update will enhance the onboarding experience, ensuring a structured and intelligent user integration process.


we will update the system prompt of agents and output types next. 


1. current flow includes the email marking step but it comes after the questions/answering stage. and we are using /app/mark-emails/page.tsx for that. we fetch 10 emails from backend for marking currenctly. and it's fetching logic is present in email.service.ts

2. there is already a function to clasify the spams and you can reuse it. if needed you may create new functions reusing the same ai agent. do in it case return type or input type you need is different. as that function is being used in other places as well so we can not change it.

3. infer_user_domain currently runs in very beginning. when user comes on the /app/onboarding page. this function sends the questinos to user generated based on email domain. 

4. Personality generation : generate personality right after user answers questions and sbumit form. as it will be used in task generation process later on. 

5. UI for marking emails and questions answering exist already. you just need to change few redirects so that after email integration, user comes to /mark-emails and then /onboarding.  