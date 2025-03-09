# Task: User Personality Analysis Based on Onboarding Data

**Objective:** Analyze onboarding form responses and email ratings to create a concise, insightful paragraph (40-60 words) that summarizes the user's professional personality, work preferences, and email habits.

## Input Format

You will receive a JSON object containing:
1. **domain** - The professional domain/industry of the user (e.g., "tech", "medical", "consulting")
2. **questions** - Array of objects with:
   - `question`: The question text
   - `answer`: The user's selected answer
   - `options`: Array of all possible options for that question
3. **emails** - Array of email objects with:
   - `subject`: Email subject line
   - `snippet`: Brief preview of the email content
   - `from`: Sender name
   - `rating`: User's importance rating (1-10, where 10 is most important)

## Analysis Guidelines

1. **Domain Context:** Consider how the user's domain influences their preferences and priorities
2. **Question Responses:** Analyze patterns in their responses - do they prioritize efficiency, collaboration, etc?
3. **Email Ratings:** Look for patterns in what types of emails they rate highly
   - Subject matter (technical, administrative, personal)
   - Communication style (formal vs. casual)
   - Sender relationships
   - Length and complexity

## Output Guidelines

1. **Professional Persona:** Describe their likely working style, priorities, and professional approach
2. **Email Preferences:** Note their apparent email habits and priorities
3. **Work Style:** Comment on organizational preferences, communication style, and potential pain points
4. **Tone:** Write in third person, objective but warm professional tone
5. **Length:** Create a single paragraph of 40-60 words
6. **Specific:** Make observations that feel personal and specific to this user
7. **Balanced:** Include both strengths and potential challenges

## Example Output

"Jane appears to be a detail-oriented tech professional who values efficient, purpose-driven communication. She prioritizes technical emails over administrative ones and seems to prefer structured workflows. Her analytical approach suggests she appreciates clear expectations and well-defined processes, though may find it challenging to navigate ambiguous situations." 