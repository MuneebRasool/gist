# Task Extraction Prompt

**Objective:** Extract actionable items from a given email body, considering the personality and context of the email recipient.

**Persona Context:** The extracted action items should be relevant and prioritized based on the provided persona of the email recipient. Consider their role, responsibilities, and preferences when identifying and phrasing action items. For example, a CEO might focus on high-level strategic actions, while a software engineer might focus on technical tasks and bug fixes.

**Input:**

*   **email_body:** (string) The full text content of the email.
*   **recipient_persona:** (string) A description of the email recipient's personality, role, and relevant context.

**Output:**

A JSON object with the following structure:

```json
{
  "items": [
    {
      "task": "string, description of the action item",
      "dependency": "string, optional, any dependencies for this task",
      "deadline": "string, optional, deadline for the task if mentioned in the email"
    }
  ]
}
```

Each item in the `items` array represents an actionable item extracted from the email.

**Example:**

**Input:**

```
email_body: """
Subject: Project Alpha Update & Next Steps

Hi Team,

Hope you're all doing well.

Quick update on Project Alpha: We've successfully completed Phase 1 (user research) and Phase 2 (design). The feedback from user testing has been overwhelmingly positive!

Next Steps:

1.  The development team needs to start working on the backend implementation. John, please coordinate with the team to schedule a kickoff meeting.
2.  Marketing needs to prepare the launch plan. Sarah, can you take the lead on this and share a draft by next Friday?
3.  We need to finalize the budget for Phase 3. David, please review the current projections and send me a summary by EOD tomorrow.
4.  Schedule a meeting with stakeholders to present the progress.

Thanks,
Alex
"""

recipient_persona: """
Name: David
Role: Finance Manager
Responsibilities: Manages project budgets, financial reporting, and resource allocation.
Preferences: Prefers concise summaries and clear deadlines. Values accuracy and efficiency.
"""
```

**Output:**

```json
{
  "items": [
    {
      "task": "Review current budget projections for Project Alpha Phase 3",
      "dependency": null,
      "deadline": null
    },
    {
      "task": "Send a summary of the budget projections to Alex",
      "dependency": null,
      "deadline": "EOD tomorrow"
    }
  ]
}
```

**Instructions:**

1.  Read the email body carefully.
2.  Identify all explicit and implicit requests, tasks, or actions directed towards the recipient, considering the `recipient_persona`.
3.  Prioritize the action items based on urgency, importance, and the recipient's role.
4.  Formulate each action item as a single, concise instruction, starting with a verb.
5.  Exclude general discussions, background information, or greetings. Focus solely on actionable items.
6.  If an action item requires further clarification, rephrase it to be as specific and self-contained as possible.
7. If dates or times are mentioned, include them in the action item.

**Constraints:**

1.  Only extract items that require *action* from the *recipient*.
2.  Do not include actions for other people mentioned in the email, unless the recipient is responsible for delegating or overseeing them.
3.  Avoid creating action items from general statements or observations.
4.  Each action item should be a single, complete sentence.
5.  Do not include any introductory or closing text in the output, only the numbered list of action items.
