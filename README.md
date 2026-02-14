🇮🇳 Bharat Exam Buddy

AI-Powered Study Assistant (Bedrock-Ready Architecture)

📌 Problem Statement

Students often struggle to understand complex academic concepts in simple language. Traditional learning platforms are not interactive or personalized.

🚀 Solution

Bharat Exam Buddy is an AI-powered study assistant that allows students to enter academic questions and receive simplified, structured explanations.

The system is architected to integrate with Amazon Bedrock for scalable AI-based contextual reasoning.

🧠 Key Features

Interactive question input

Simplified concept explanations

Structured AI response format

Bedrock-ready backend integration

Clean web interface using Streamlit

🏗 Architecture Overview

User Input → Streamlit UI → Bedrock Runtime (via boto3 SDK) → AI Model (Claude/Titan) → Response Output

(Current prototype runs in demo mode with structured Bedrock integration logic.)

☁ AWS Services Designed For

Amazon Bedrock (Claude/Titan Model)

AWS IAM

Bedrock Runtime API

Scalable Cloud Deployment (Future Scope)

🔧 Tech Stack

Python

Streamlit

boto3 (AWS SDK)

🔮 Future Enhancements

Live Bedrock API activation

Personalized student profiles

Subject-wise AI tutoring

Exam-focused question generation