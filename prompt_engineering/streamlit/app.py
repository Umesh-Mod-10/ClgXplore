import os
import sys
import logging

# Setting up directories and paths
current_dir = os.path.dirname(os.path.abspath(__file__))
kit_dir = os.path.abspath(os.path.join(current_dir, ".."))
repo_dir = os.path.abspath(os.path.join(kit_dir, ".."))

sys.path.append(kit_dir)
sys.path.append(repo_dir)

import streamlit as st
import base64
from dotenv import load_dotenv
from src.llm_management import LLMManager

# Load environment variables
load_dotenv(os.path.join(repo_dir, '.env'))

# Logging setup
logging.basicConfig(level=logging.INFO)
logging.info("App started at: http://localhost:8501")


@st.cache_data
def call_api(llm_manager: LLMManager, prompt: str, llm_expert: str) -> str:
    """Calls the API endpoint with the prompt and returns the completion text."""
    llm = llm_manager.set_llm(model_expert=llm_expert)
    completion_text = llm.invoke(prompt)
    return completion_text


def render_image(image_path: str) -> None:
    """Renders an image (PNG) from the specified file path in an attractive way."""
    with open(image_path, 'rb') as file:
        image_data = file.read()
    b64 = base64.b64encode(image_data).decode("utf-8")

    # Adding styling: center, add a border, shadow, and adjust size
    html = f'''
    <div style="
        text-align: center;
        padding: 10px;
    ">
        <img src="data:image/png;base64,{b64}" style="
            width: 280px;
            height: auto;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
        " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'"/>
    </div>
    '''
    st.write(html, unsafe_allow_html=True)


def format_inr(value: int) -> str:
    """Formats the number in Indian numeric system."""
    value_str = str(value)[::-1]
    parts = []
    for i in range(len(value_str)):
        if i == 3:
            parts.append(",")
        elif i > 3 and (i - 3) % 2 == 0:
            parts.append(",")
        parts.append(value_str[i])
    return ''.join(parts)[::-1]


def main():
    # Streamlit page configuration
    st.set_page_config(page_title='ClgXplore AI', layout="centered", initial_sidebar_state="auto",
                       menu_items={'Get help': 'https://github.com/sambanova/ai-starter-kit/issues/new'})

    # Construct the full path to the image
    logo_path = os.path.join(current_dir, '..', 'clgxplore-high-resolution-logo.png')

    col1, _, col2 = st.columns([1, 1, 20])
    st.markdown(
        f"""
        <div style="
            padding-bottom: 10px;
        ">
            <div style="
                display: flex;
                align-items: center;   /* Vertically center the image and text */
                justify-content: flex-start;  /* Align items to the left */
                margin-left: 50px;     /* Adjust this for spacing */
                margin-top: 20px;      /* Adjust this for top margin */
            ">
                <div>
                    <img src="data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" 
                    style="width: 300px; height: auto; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">
                </div>
                <div style="margin-left: 50px;">  <!-- Adjust margin between image and text -->
                    <h1 style="color: #4ab3e8; font-size: 70px;">ClgXplore.ai</h1>
                    <h5 style="color: grey; font-weight: bold;">
                        "YOU" Be the one to make the first important decision of your life - Your College Life!!
                    </h5>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <hr style="border: 2px solid cyan;">
        """,
        unsafe_allow_html=True
    )

    # Initialize LLM Manager
    llm_manager = LLMManager()
    llm_info = llm_manager.llm_info

    # Display the model information
    st.text(f"Using Model: {llm_info['select_expert']} - Using Sambanova Fast API")

    # Introductory text
    st.markdown(
        """
        <div style="font-size: 30px;">
            \nFind Your Perfect College with your choices as preference! At ClgXplore, we’ve optimized our model to deliver personalized college recommendations, considering every crucial factor to help you make the best decision which
            is best for your future.

            \n**The steps to use our service:**
            \n\n* Select Your Preferences – Choose the options that resonate with your interests and priorities.
            \n* Trust the Process – Our advanced model will curate a list of colleges that fit your personal criteria.

            \n**Take control of your future, Start now and find the college that’s just right for you!**
        </div>
        """,

        unsafe_allow_html=True
    )

    st.markdown(
        """
        <hr style="border: 2px solid cyan;">
        """,
        unsafe_allow_html=True
    )

    # Form to collect student details
    st.subheader("Enter Your Details")

    col1, col2 = st.columns([1, 1])
    with col1:
        name = st.text_input("Enter your name")
        field = st.selectbox("Select your field of interest", ['Engineering', 'Arts', 'Commerce'])

        # Budget input with text box - Step set to 1000
        if 'budget' not in st.session_state:
            st.session_state.budget = 200000
        budget = st.number_input("Your budget (in INR annually)", min_value=25000, max_value=3500000,
                                 value=st.session_state.budget, step=5000)  # Step changed to 1000
        st.session_state.budget = budget
        st.write(f"Selected Budget: {format_inr(st.session_state.budget)} INR")  # Indian style formatting applied here

        financial_bg = st.selectbox("Financial background", ['Low', 'Medium', 'High'])

    with col2:
        student_interests = st.text_area("Student Interests (e.g., Robotics, AI, Marketing)", height=90)
        additional_exp = st.text_area("Additional Expectations (e.g., Internships, Campus Culture)", height=90)
        geo_pref = st.text_input("Geographic Preferences (e.g., State, City, Proximity to Home)")

    # Entrance Exam Dropdown and Text Box Inputs
    exams = st.multiselect("Select Entrance Exam", ['JEE', 'JEE Advanced', 'State Board'])

    # Initialize empty variables for storing percentile/percentage values
    exam_results = []

    # Initialize default percentiles if not already set
    if 'jee_percentile' not in st.session_state:
        st.session_state.jee_percentile = 0
    if 'jee_advanced_percentile' not in st.session_state:
        st.session_state.jee_advanced_percentile = 0

    # Handle JEE percentile
    if 'JEE' in exams:
        jee_percentile = st.number_input("JEE Percentile", min_value=0, max_value=100,
                                         value=st.session_state.jee_percentile)
        st.session_state.jee_percentile = jee_percentile
        exam_results.append(f"JEE: {jee_percentile}% Percentile")

    # Handle JEE Advanced percentile
    if 'JEE Advanced' in exams:
        jee_advanced_percentile = st.number_input("JEE Advanced Percentile", min_value=0, max_value=100,
                                                  value=st.session_state.jee_advanced_percentile)
        st.session_state.jee_advanced_percentile = jee_advanced_percentile
        exam_results.append(f"JEE Advanced: {jee_advanced_percentile}% Percentile")

    # Handle State Board percentage
    if 'State Board' in exams:
        if 'state_board_percentage' not in st.session_state:
            st.session_state.state_board_percentage = 75
        state_board_percentage = st.number_input("State Board Percentage", min_value=50, max_value=100,
                                                 value=st.session_state.state_board_percentage)
        st.session_state.state_board_percentage = state_board_percentage
        exam_results.append(f"State Board: {state_board_percentage}% Percentage")

    # Advanced preferences
    with st.expander('Advanced College Preferences (click to expand)', expanded=False):
        st.subheader("Advanced College Preferences")

        col3, col4 = st.columns([1, 1])
        with col3:
            college_reputation = st.selectbox("College Reputation & Alumni Network",
                                              ['Not Important', 'Moderately Important', 'Very Important'])
            job_placement = st.selectbox("Job Placement Statistics", ['Low', 'Medium', 'High'])
            faculty_research = st.selectbox("Faculty & Research Opportunities",
                                            ['Not Important', 'Moderately Important', 'Very Important'])
            internship_exposure = st.selectbox("Internship & Industry Exposure", ['Low', 'Moderate', 'High'])
        extracurriculars = st.text_area("Extracurricular Activities (Technical/Non-Technical Clubs)", height=90)

        with col4:
            scholarships_aid = st.selectbox("Scholarships & Financial Aid Opportunities",
                                            ['Not Important', 'Moderately Important', 'Very Important'])

            # Campus Facilities with checkboxes
            campus_facilities = st.multiselect("Campus Facilities",
                                               ['Labs', 'Libraries', 'Event Halls', 'Canteens', 'Incubation Centers',
                                                'Other'])
            if 'Other' in campus_facilities:
                other_facilities = st.text_input("Other Facilities")

            # Accreditation & Approval with checkboxes
            accreditation = st.multiselect("Accreditation & Approval", ['AICTE', 'NBA', 'NAAC'])

            # Post-Graduation Opportunities with checkboxes
            post_grad_opps = st.multiselect("Post-Graduation Opportunities", ["Master's", "PhD", "Abroad Options"])

    # Generate the prompt template
    prompt_template = f"""
    You are a college recommendation assistant. A student named {name} is looking for colleges. just 5 colleges
    - Field of study: {field}
    - Exam Results: {', '.join(exam_results)}
    - Budget: {budget:,} INR annually
    - Financial background: {financial_bg}
    - Student interests: {student_interests}
    - Additional expectations: {additional_exp}
    - Geographic preferences: {geo_pref}

    Instructions to keep in mind
    - If location given is 'Any', give colleges for student cutoffs is lesser than students marks and follow the bulletins. 
    - If the college does’t meet the criteria of interest, don't show any details of the college.
    - If the cutoff of students is low compared to the requirement, Dont show the college 
    - If the location is outside India, display: We currently offer services only for locations in India in a brief manner and stop generation fully.

    Provide details in bullet points in one sentence:
    - Website link
    - Distance from location in kms
    - Cutoff comparison in each mark with the students marks
    - Offered course
    - Budget and scholarships in simple terms and suggest the hostel fees
    While generating follow these:
    - Do not generate half points
    - Do not generate incomplete sentences.
    - For reference, visit https://collegedunia.com.
    """

    st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
        font-size: 16px;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # prompt = st.text_area(label='prompts', value=prompt_template, height=100)

    # Process the prompt when the user clicks the 'Send' button
    if st.button('Get your college'):
        response_content = call_api(llm_manager, prompt_template, llm_info["select_expert"])
        st.write(response_content)


if __name__ == "__main__":
    main()
