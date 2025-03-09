# **Email Content Classifier**  

## **Task**  
Analyze the provided email content and classify it into one of the following categories:  

### **1. Content Type**  
- 1.  **Library** → Important references such as OTPs, personal emails from friends or family, and saved information.  
- 2.  **Main Focus-View** → High-priority emails containing urgent tasks, deadlines, or time-sensitive information.  
- 3.  **Drawer** → Low-priority content like newsletters, articles, advertisements, and promotional emails.  

- **Library** → 1
- **Main Focus-View** → 2
- **Drawer** → 3

## **Analysis Approach**  
1. **Identify Structural Patterns:**  
   - Subject line, sender, and formatting cues.  
   - Urgency indicators (e.g., deadlines, alerts, action items).  
   - Differentiation between personal, transactional, and promotional emails.  
2. **Determine the Most Relevant Category:**  
   - If the email requires urgent attention or contains deadlines → **Main Focus-View**  
   - If the email is a reference or contains personal communication → **Library**  
   - If the email is promotional, informational, or non-urgent → **Drawer**  

## **Output Format**  
Provide the classification in the following JSON format:  

```json
{
  "type": "1"
}
Do not include any additional explanations beyond the JSON response.








