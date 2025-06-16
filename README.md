<h1 align="center" style="border-bottom: none">
    <div>
        Gist
    </div>
    AI-powered task management System<br>
</h1>

<p align="center">
The goal of Gist is to reduce cognitive overload and make sure daily life task management easy.
</p>

<div align="center">

[![License]( https://img.shields.io/badge/Apache-%202.0-blue)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-%23000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-%230D96F6?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Database-%234581C3?logo=neo4j&logoColor=white)](https://neo4j.com/)

</div>

![Gist thumbnail](web/public/logo.png)


## What is Gist?

Gist is an agentic task management system that solves the problem of cognitive overload by using AI to extract, prioritize, and present actionable information.

<br>

You can use Gist for:
* **Smart Task Management:**

  * **Task Extraction:** Gist automatically discovers tasks from your digital communications like emails, eliminating the need for manual entry
  
  * **Intelligent Prioritization:** Tasks are scored and prioritized based on their relevance to you

* **AI-powered Organization:**

  * **Dynamic Relevance Scoring:** Gist uses AI models to calculate task relevance in real-time based on user feedback
  
  * **Automated Email Processing:** Integration with Nylas allows Gist to analyze your email communications and extract actionable items

  * **Personalized Experience:** The system learns your preferences and adapts to your unique work patterns over time

* **Cognitive Load Management:**

  * Tasks are surfaced at the optimal moment, maintaining your cognitive balance
  
  * Gist understands your professional context and the relationships between different tasks

  * Stop juggling between different apps and systems - everything important is in one place


> Gist gets smarter the more you use it. Your feedback and interactions help the system learn and adapt to your specific needs.

<br>

## Product Demo

Watch Gist in action: [Product Demo Video](https://drive.google.com/file/d/1BkQGVtxdQBgCZuvNychpjkI-XIWlxWDu/view)

This video shows:
- How tasks are extracted from emails
- How Gist prioritizes tasks
- How you can manage tasks in the app

## Installation

For installation and setup instructions, see the [Setup Guide](SETUP.md).

Once running, visit [localhost:3000](http://localhost:3000) in your browser.


## Getting Started

To start using Gist, follow these simple steps:

1. **Create an account** by signing up with your email
2. **Connect your email accounts** through our secure Nylas integration
3. **Answer a few questions** to help Gist understand your work context
4. **Review your personalized profile** and make any necessary adjustments
5. **Start managing tasks** with Gist's intelligent prioritization

### How Gist Prioritizes Your Tasks

Gist uses a sophisticated mathematical model to score and prioritize tasks:

```math
R_i(t) = α·U_i(t) - β·C_i(t)
```

Where:
- R_i(t): Overall relevance score
- U_i(t): Utility factor (importance/urgency)
- C_i(t): Cognitive cost factor
- α, β: Learning-adjusted scaling parameters

This approach ensures that tasks with high utility and low cognitive cost are surfaced first, helping you work with your brain's natural tendencies rather than against them.

### Key Features

* **Email Integration:** Gist connects to your email accounts via Nylas to extract tasks automatically
* **Domain Inference:** The system analyzes your professional context to understand the importance of different tasks
* **Dynamic Scoring:** Tasks are continuously reprioritized based on changing circumstances and deadlines
* **Personalized Experience:** Gist learns from your interactions to better serve your specific needs
* **Graph-Based Task Model:** Tasks and their relationships are modeled as a dynamic graph, allowing for complex dependencies


## Contributing

There are many ways to contribute to Gist:

* Submit bug reports and feature requests
* Submit Pull Requests to improve it

To learn more about how to contribute, please see our [contributing guidelines](CONTRIBUTING.md)

## Additional Resources

* [System Design](documentation/DESIGN.md)
* [Our Mission](documentation/Mission.md)
* [Scoring Models](documentation/Scoring_models.md)
* [Environment Variables](documentation/environment-variables.md)
* [Webhook](documentation/webhook.md)

