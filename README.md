
<h1 align="center" style="border-bottom: none">
    <div>
        GIST
    </div>
    AI-powered task management that works with your brain, not against it<br>
</h1>

<p align="center">
Turn information chaos into digital harmony. GIST extracts, prioritizes, and surfaces the right tasks at the right time, helping you overcome information overload and achieve focused productivity.
</p>

<div align="center">

[![License]( https://img.shields.io/badge/Apache-%202.0-blue)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-%23000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-%230D96F6?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Database-%234581C3?logo=neo4j&logoColor=white)](https://neo4j.com/)

</div>

![GIST thumbnail](web/public/logo.png)

## 🚀 What is GIST?

GIST is an intelligent task management system that solves the problem of digital overwhelm by using AI to extract, prioritize, and present tasks when you need them most.

<br>

You can use GIST for:
* **Smart Task Management:**

  * **Task Extraction:** GIST automatically discovers tasks from your digital communications, eliminating the need for manual entry
  
  * **Intelligent Prioritization:** Tasks are scored and prioritized based on their relevance to you, considering both utility and cognitive cost

  * **Temporal Sequencing:** Information flows through time - GIST presents what you need, when you need it, and gracefully defers what can wait

* **AI-powered Organization:**

  * **Dynamic Relevance Scoring:** GIST uses AI models to calculate task relevance in real-time based on user feedback
  
  * **Automated Email Processing:** Integration with Nylas allows GIST to analyze your email communications and extract actionable items

  * **Personalized Experience:** The system learns your preferences and adapts to your unique work patterns over time

* **Cognitive Load Management:**

  * **Emergent Actionability:** Tasks are surfaced at the perfect moment, maintaining your cognitive balance
  
  * **Domain-Aware Analysis:** GIST understands your professional context and the relationships between different tasks

  * **Reduced Digital Friction:** Stop juggling between different apps and systems - everything important is in one place

> [!TIP]
> GIST gets smarter the more you use it. Your feedback and interactions help the system learn and adapt to your specific needs.

<br>

## 🛠️ Installation

Mannual Method :

```bash
# Clone the GIST repository
git clone https://github.com/opengig/gist.git

# Navigate to the repository
cd web 
pnpm i
pnpm dev

cd server
uv venv
source .venv/bin/activate
uv sync
fastapi dev

```
OR 

GIST can be self-hosted using Docker Compose, making it easy to set up your own instance:

```bash
git clone https://github.com/opengig/gist.git
chmod +x start-local.sh
./start-local.sh
```

Once all is up and running, you can visit [localhost:3000](http://localhost:3000) on your browser!

## 🏁 Get Started

To start using GIST, follow these simple steps:

1. **Create an account** by signing up with your email
2. **Connect your email accounts** through our secure Nylas integration
3. **Answer a few questions** to help GIST understand your work context
4. **Review your personalized profile** and make any necessary adjustments
5. **Start managing tasks** with GIST's intelligent prioritization

### 📈 How GIST Prioritizes Your Tasks

GIST uses a sophisticated mathematical model to score and prioritize tasks:

```math
R_i(t) = α·U_i(t) - β·C_i(t)
```

Where:
- R_i(t): Overall relevance score
- U_i(t): Utility factor (importance/urgency)
- C_i(t): Cognitive cost factor
- α, β: Learning-adjusted scaling parameters

This approach ensures that tasks with high utility and low cognitive cost are surfaced first, helping you work with your brain's natural tendencies rather than against them.

### 🧠 Key Features

* **Email Integration:** GIST connects to your email accounts via Nylas to extract tasks automatically
* **Domain Inference:** The system analyzes your professional context to understand the importance of different tasks
* **Dynamic Scoring:** Tasks are continuously reprioritized based on changing circumstances and deadlines
* **Personalized Experience:** GIST learns from your interactions to better serve your specific needs
* **Graph-Based Task Model:** Tasks and their relationships are modeled as a dynamic graph, allowing for complex dependencies

## ⚙️ Environment Setup

GIST requires several environment variables to be set for proper functionality. Key configurations include:

* Authentication & OAuth settings
* Database connection parameters (PostgreSQL and Neo4j)
* Email integration via Nylas
* LLM API credentials for AI-powered features

For detailed instructions, see the [environment variables documentation](Documentation/environment-variables.md).

## 🤝 Contributing

There are many ways to contribute to GIST:

* Submit bug reports and feature requests
* Review the documentation and submit Pull Requests to improve it
* Share your experience using GIST with others
* Suggest improvements to the task scoring models

To learn more about how to contribute, please see our contributing guidelines.

## 🔮 Future Plans

We're continuously improving GIST with new features and capabilities:

* Mobile applications for on-the-go task management
* Enhanced collaboration features
* More advanced ML models for task prediction
* Additional third-party integrations
* Real-time collaboration tools
* Reinforcement Learning for task extraction and prioritization
* More ways to get the user feedback to improve personalization

## 📚 Learn More

* [System Design](documentation/DESIGN.md)
* [Our Mission](documentation/Mission.md)
* [Scoring Models](documentation/Scoring_models.md)
* [Environment Variables](documentation/environment-variables.md)