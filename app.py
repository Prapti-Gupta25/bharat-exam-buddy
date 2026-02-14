import streamlit as st
import json
import boto3

# Toggle for real Bedrock usage
USE_BEDROCK = False  

st.title("🇮🇳 Bharat Exam Buddy")
st.write("AI-powered Study Assistant for Indian Students")

user_input = st.text_area("Ask your academic question:")

def mock_ai_response(question):
    question_lower = question.lower()

    if "dna" in question_lower:
        explanation = "DNA is the molecule that carries genetic information in living organisms."
    elif "photosynthesis" in question_lower:
        explanation = "Photosynthesis is the process by which plants make their own food using sunlight, carbon dioxide, and water."
    elif "newton" in question_lower:
        explanation = """
Newton’s Three Laws of Motion:

1️⃣ First Law (Law of Inertia):
An object remains at rest or in uniform motion unless acted upon by an external force.

2️⃣ Second Law:
Force = Mass × Acceleration (F = ma).
The acceleration of an object depends on its mass and the force applied.

3️⃣ Third Law:
For every action, there is an equal and opposite reaction.
"""

    else:
        explanation = "This is a demo explanation generated in prototype mode."

    return f"""
### 📘 Simple Explanation

**Question:** {question}

{explanation}

🔗 Powered by a Bedrock-ready AI architecture designed for scalable deployment.
"""




def call_bedrock(question):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    body = json.dumps({
        "prompt": question,
        "max_tokens": 300
    })

    response = client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2",
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read())
    return result

if st.button("Generate Answer"):
    if user_input:
        if USE_BEDROCK:
            answer = call_bedrock(user_input)
        else:
            answer = mock_ai_response(user_input)

        st.markdown(answer)
    else:
        st.warning("Please enter a question.")
