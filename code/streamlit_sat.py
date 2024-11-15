import ast
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def load_data(file):
    data = pd.read_csv(file)
    return data


# Function to display details of each problem entry
def display_problem_details(problem_data):
    try:
        problem_dict = ast.literal_eval(problem_data)
    except (ValueError, SyntaxError):
        st.error("Invalid format in problem data. Unable to parse.")
        return

    question = problem_dict.get('question', 'N/A')
    choices = problem_dict.get('choices', [])
    answer = problem_dict.get('answer', 'N/A')
    st.write(f"**Question:** {question}")
    st.write(f"**Choices:** {choices}")
    st.write(f"**Answer:** {answer}")


# Function to plot length distribution as a histogram
def plot_length_histogram(data, column_name, title, isDict=False, dictName=None):
    if isDict:
        lengths = data[column_name].apply(lambda x: len(str(ast.literal_eval(x).get(dictName, ''))) if pd.notnull(x) else 0)
    else:
        lengths = data[column_name].apply(lambda x: len(str(x)) if pd.notnull(x) else 0)

    # Plot histogram
    fig, ax = plt.subplots()
    ax.hist(lengths, bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'{title} Length Distribution')
    ax.set_xlabel('Length')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)


# Main Streamlit app
st.title("Korean CSAT Language Section EDA")

# File uploader for user-uploaded data
file = st.file_uploader("Upload your dataset CSV file", type=["csv"])

if file is not None:
    # Load the uploaded data
    data = load_data(file)

    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Basic dataset information
    st.write("### Dataset Information")
    st.write(f"Number of entries: {len(data)}")
    st.write(f"Columns: {data.columns.tolist()}")

    # Display samples of each field
    st.write("### Field Analysis")

    # Display a sample paragraph
    st.subheader("Sample Paragraph")
    st.write(data['paragraph'].iloc[0])

    # Display a sample problem with details
    st.subheader("Sample Problem")
    display_problem_details(data['problems'].iloc[0])

    # Display a sample 'question_plus' entry
    st.subheader("Sample Question Plus")
    st.write(data['question_plus'].iloc[0])

    # Additional statistics
    st.write("### Additional Statistics")

    # Plot length distributions for each field
    plot_length_histogram(data, 'paragraph', 'Paragraph')
    plot_length_histogram(data, 'problems', 'Question', True, 'question')
    plot_length_histogram(data, 'problems', 'Choices', True, 'choices')
    plot_length_histogram(data, 'question_plus', 'Question Plus')

    # Answer count analysis
    st.write("#### Answer Distribution")
    answer_counts = data['problems'].apply(lambda x: ast.literal_eval(x)['answer']).value_counts()
    st.bar_chart(answer_counts.sort_index())


output_file = st.file_uploader("Upload your output CSV file", type=["csv"])

if output_file is not None:
    data = load_data(output_file)

    st.write("### Answer Distribution")
    answer_counts = data['answer'].value_counts()
    st.bar_chart(answer_counts.sort_index())