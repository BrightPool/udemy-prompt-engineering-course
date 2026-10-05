# Introduction to Jupyter Notebooks + Python

Part 7: Prompting in the API. Instructor: James.

## Slide 1: Introduction to Jupyter Notebooks + Python

Welcome to the coding part of the course. Throughout the coding lessons, we'll use Jupyter notebooks containing the code for the examples. If you've never written Python before, you can still follow along. We'll supply the code and explain what each step does. Your first aim is to run an example successfully, then change a small part and see what happens. If you're already a developer, the same material is available on GitHub so you can explore and build on it.

Source: https://github.com/BrightPool/udemy-prompt-engineering-course

## Slide 2: Jupyter Notebooks + Python

A Jupyter notebook is a document made of cells. Text cells explain the lesson, code cells contain instructions, and outputs appear below the code. Python is the language we use to give those instructions. A notebook normally has the .ipynb file extension. Here, print displays the words Hello, AI! When you run that cell, you see the result immediately. In the course examples, you'll also see cells that install packages, ask for an API key and call an AI service. Run those setup cells in the order shown. You don't need to understand every line on the first pass.

Sources: https://jupyter.org/ and https://docs.python.org/3/tutorial/
Logo sources: https://github.com/jupyter/design/blob/main/logos/Square%20Logo/squarelogo-greytext-orangebody-greymoons/squarelogo-greytext-orangebody-greymoons.svg and https://www.python.org/community/logos/

## Slide 3: Two Ways to Follow Along

Both routes use the course notebooks. If you're new to coding, I recommend Google Colab: it runs Python in your browser, so you can follow the lesson without installing Python on your computer. You will need a Google account to save your own copy and run the notebook. If you're technical, download the repository as a ZIP or clone it with Git. That gives you the code and supporting files available in the repository, including examples for APIs, retrieval, agents and evaluations. Open the .ipynb files in JupyterLab or a notebook-capable editor such as VS Code. GitHub contains the coding companion rather than the entire video course. For a plain Python download, open a notebook in Colab and use File, Download, Download .py. A .py export contains the code, whereas .ipynb preserves the notebook format. Some notebook-specific commands or uploaded-file steps may need adapting before you run the exported script locally.

Sources: https://github.com/BrightPool/udemy-prompt-engineering-course, https://research.google.com/colaboratory/faq.html
Links: https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/ and https://github.com/BrightPool/udemy-prompt-engineering-course
Logo sources: https://colab.research.google.com/img/colab_favicon_256px.png and https://brand.github.com/GitHub_Logos.zip

## Slide 4: Following Along in Google Colab

Open the course notebook using the link on this slide. Click Copy to Drive to save your own editable version. Connect to a runtime, which is the computer that executes your code, then use the play control next to each code cell. Run from top to bottom because later cells may depend on earlier ones. You can also use Shift+Enter to run a selected cell. If Colab disconnects, reconnect and rerun the earlier setup cells.

For a short live demonstration, first open a blank Colab notebook and run print("Hello, AI!"). Change AI to your own name and run it again. This shows what a cell and its output look like without requiring an API key. Then return to a course notebook to show the supplied code. There is no need to run an API example in this introduction. We'll cover provider account setup and API keys in the next lessons. API usage can incur separate charges from the provider.

Source: https://research.google.com/colaboratory/faq.html
Course notebook link: https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/openai_features_and_functionality/responses_api_and_messages.ipynb
Screenshot: actual public course notebook captured in Colab during deck preparation. Existing output visible in the notebook is saved notebook output.

## Slide 5: The Course Code on GitHub

This is the repository for the course. The folders group the code by topic, and the README helps you find a starting point. Use the green Code menu and choose Download ZIP to download the repository. If you use Git, clone it instead so you can pull later updates. The repository provides the coding materials, including notebooks and supporting prompts, example apps and datasets where available. Some notebooks use extra uploaded files or external services. Follow the setup instructions for the notebook you are using.

Developer route: git clone https://github.com/BrightPool/udemy-prompt-engineering-course.git
For a minimal local notebook environment, the repository README shows how to create a Python virtual environment, install JupyterLab, and start jupyter lab. Notebook cells install many additional dependencies inline.

If you're new to coding, you can stay with Colab and return to the local setup when you're ready. Let's open a notebook and run the first cell together.

Sources and screenshot page: https://github.com/BrightPool/udemy-prompt-engineering-course
Direct repository ZIP: https://github.com/BrightPool/udemy-prompt-engineering-course/archive/refs/heads/main.zip
