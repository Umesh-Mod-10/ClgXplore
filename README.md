

# ClgXplore AI

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="prompt_engineering/clgxplore-high-resolution-logo.png" height="100">
  <img alt="SambaNova logo" src="./images/SambaNova-dark-logo-1.png" height="100">
</picture>


# Overview

This project is a **College Recommendation Chatbot** designed to assist fresh high school graduates in selecting the most suitable college based on their personal preferences. Developed using the **Prompt Engineering Starter Kit**, the chatbot gathers information such as geographical preferences, budget, entrance exam scores, campus facilities, and post-graduation opportunities. 

The user-friendly interface provides both sliders and text boxes for ease of input, while advanced options like accreditation and specialized courses are hidden until prompted. Based on the input provided, the chatbot offers personalized, data-driven college recommendations to help students make informed decisions. This tool simplifies the complex process of college selection, ensuring that each student receives accurate suggestions tailored to their unique requirements.

# The technical working

The **College Recommendation Chatbot** is powered by the **SambaNova Fast API**, using the **LLaMA3-405B** model for natural language processing and prompt engineering. The chatbot is designed with a custom template to ensure the most accurate and contextually relevant answers based on user preferences. The interface is built using **Streamlit** and hosted locally, providing users with a seamless experience.

1. **LLM Integration**: The chatbot leverages the LLaMA3-405B model via the SambaNova API. User inputs, such as geographical preferences, budget, exam scores, and facilities, are passed through a carefully designed prompt template that ensures accurate and tailored responses from the model.
2. **Prompt Engineering**: A custom template is created to standardize user inputs, helping the model better interpret preferences and provide high-quality recommendations. This template-driven approach enhances the precision of the LLM's output.
3. **Streamlit Interface**: The front end is developed using Streamlit, providing an intuitive UI that includes sliders for budget and percentile inputs, checkboxes for additional preferences, and dynamically hidden advanced options. The UI is hosted locally for testing and iteration.
4. **Backend Processing**: User preferences are captured and passed through the API, where the LLaMA3-405B model generates college recommendations based on the input. The backend logic weighs the inputs against the model’s trained data, ensuring personalized recommendations.
5. **Output**: The chatbot outputs a list of suggested colleges, providing users with detailed, data-driven recommendations aligned with their preferences, including factors like location, budget, and post-graduation opportunities.

This system is flexible and allows for future expansions or integrations, with the LLaMA3-405B model ensuring robust and accurate decision-making capabilities.

# Execution the project

To run the project using a virtual environment (either virtualenv or conda), follow these steps in your project terminal:

Navigate to the project directory:
```
cd ai-starter-kit/prompt-engineering
```
Create a virtual environment: For virtualenv, run:
```
python3 -m venv prompt_engineering_env
```
Activate the virtual environment: On macOS or Linux, run:
```
source prompt_engineering_env/bin/activate
```
On Windows, run:
```
.\prompt_engineering_env\Scripts\activate
```
Install the required packages:

```
pip install -r requirements.txt
```

Run the application by:
```
streamlit run streamlit/app.py --browser.gatherUsageStats false 
```


Once the College Recommendation Chatbot is set up, users can input their preferences such as location, budget, entrance exam scores, and campus facilities through the Streamlit UI. These inputs are processed by the LLaMA3-405B model via SambaNova Fast API to generate personalized college recommendations. The chatbot then displays a list of colleges tailored to the user's preferences, helping them make informed decisions.
