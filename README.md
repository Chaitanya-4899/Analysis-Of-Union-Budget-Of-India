* Budget Speech Analysis Project

This project is a interactive Budget speech data analysis platform, where insightful visualizations meet powerful analytics. This app enables you to explore, analyze, and understand complex budget data through intuitive visualizations, advanced sentiment analysis and text summarization tools. It also consists of an interactive Trend Analysis dashboard created on Power BI.

============================================================================================================================================================

* Project Structure

The project consists of two main parts:
- `budget_analysis/`: Contains the Django project files, including views, models, templates, static files, etc.
- "TrendAnalysis.pbix": A Power BI file containing Trend analysis dashboard.

============================================================================================================================================================

* Getting Started

- Prerequisites

- Install Power BI desktop app.

- Setup

1. Download and Extract the Project:
    - Download the `budget_analysis.zip` file.
    - Extract the contents of the zip file to a desired location on your computer.

2. Create virtual environment:
    - Navigate to the project directory using: "cd path_to_the_project/budget_analysis"
    - Run the following command to create virtual environment: "python -m venv budget_analysis_venv"

3. Activate the Virtual Environment:

    Windows:
    ```bash
    cd path\to\ProjectCodeFiles\budget_analysis_venv\Scripts
    activate
    ```

    Mac/Linux:
    ```bash
    cd path/to/ProjectCodeFiles/budget_analysis_venv/bin
    source activate
    ```

4. Install dependencies via - "pip install -r requirements.txt" in the created virtual environment.

** Manual installation of dependencies might be required if the virtual environment is not compatible with the terminal configurations and the current Python version. Some of the dependencies that are required to be manually downloaded are:

- pip install django
- pip install nltk
- pip install matplotlib
- pip install wordcloud

5. Post installation script, execute following command: "python post_install.py"

6. Run the Django Development Server:
    - Navigate to the `budget_analysis` directory:
      ```bash
      cd path\to\budget_analysis
      ```
    - Run the Django development server:
      ```bash
      python manage.py runserver
      ```
7. Access the Application:- Open your web browser: 
a) Go to `http://127.0.0.1:8000/admin/login/?next=/admin/` to access the Django admin page for my web app.

   Credentials - username :chait
               - password :chait040899

b) `http://127.0.0.1:8000/` to access the Budget Speech analysis application.

8. Open the "TrendAnalysis.pbix" file in your Power BI desktop app, to access the Trend Analysis dashboard.
===========================================================================================================================================================

* Notes

- No additional software is required**: The project is configured such that all necessary libraries are bundled within the project directories, so there's no need to install them separately or modify environment variables.
- Running the Application: Ensure the virtual environment is activated each time before running the application.

============================================================================================================================================================
  
* Troubleshooting

- nltk version Issues: If you encounter issues with `nltk` version during installation, you can manually install the latest version in the virtual environment.  

============================================================================================================================================================

