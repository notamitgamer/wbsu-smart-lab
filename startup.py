import os

def create_file(filename, content):
    """Creates a file with the given content."""
    # Using utf-8 encoding ensures emojis inside the files are saved correctly
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content.strip())
    # Removed emoji from print statement to prevent Windows encoding errors
    print(f"[OK] Generated: {filename}")

# --- 1. README.md ---
readme_content = """
# 🎓 WBSU AI Lab Assistant

**Turn your College Code Repository into an Intelligent Study Companion.**

This project uses Retrieval-Augmented Generation (RAG) and Google's Gemini AI to transform a static folder of C/Python lab programs into an active teaching assistant.

## 🚀 Features

1.  **Chat with your Labs (RAG):** Ask questions like "How did I implement the matrix multiplication logic?" and get answers based on *your* specific code.
2.  **Viva Voce Simulator:** The AI acts as an External Examiner, scanning your code and generating strictly graded viva questions to prepare you for exams.
3.  **Auto-Report Generator:** Instantly synthesizes formal "Aim," "Algorithm," and "Conclusion" text for your physical lab notebook.
4.  **License Awareness:** Built-in awareness of the ESAL-1.0 license to prevent academic dishonesty.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/WBSU-AI-Lab-Assistant.git](https://github.com/your-username/WBSU-AI-Lab-Assistant.git)
    cd WBSU-AI-Lab-Assistant
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run wbsu_lab_assistant.py
    ```

## 📜 Project History & Lineage

* **Phase 1 (Aug 2025):** Static WBSU Code Repository (Semester 1).
* **Phase 2 (Dec 2025):** Implementation of ESAL-1.0 Governance.
* **Phase 3 (Jan 2026):** AI Integration (RAG + Generative AI).

## 🤝 Contributing

This project operates under the **Academic Integrity Code of Conduct**. We welcome improvements, but please do not use this tool to facilitate plagiarism.
"""

# --- 2. CODE_OF_CONDUCT.md ---
coc_content = """
# Code of Conduct

## Our Pledge
We are committed to making this project a welcoming and harassment-free experience for everyone. This is a space for learning, not for judgment.

## Academic Integrity
As this is a tool for college students:

* **Do not** use this tool to facilitate cheating or submit generated code as your own without understanding.
* **Do** use this tool to understand concepts you are struggling with.
* **Do** share your own explanations and improvements.

## Enforcement
Violations of the Academic Integrity clause (e.g., using this repo to plagiarize) may result in being blocked from the repository.
"""

# --- 3. SECURITY.md ---
security_content = """
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability or a way to bypass the academic integrity guardrails (e.g., jailbreaking the prompt to make it write your entire exam), please report it to the maintainers immediately.

**Do not create a public GitHub issue for vulnerabilities.**

Please email the project maintainer directly. We will address the issue as soon as possible.
"""

# --- 4. LICENSE (ESAL-1.0) ---
license_content = """
EDUCATIONAL SOURCE-AVAILABLE LICENSE (ESAL-1.0)

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, and publish the Software, SUBJECT TO THE FOLLOWING CONDITIONS:

1. **Academic Integrity:** The Software shall not be used to generate submissions for academic credit where such use would violate the academic integrity policy of the user's educational institution.
2. **Attribution:** The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""

# --- 5. .gitignore ---
gitignore_content = """
# Python
__pycache__/
*.pyc

# Environment Variables
.env

# Streamlit
.streamlit/
"""

# --- 6. requirements.txt ---
requirements_content = """
streamlit
google-generativeai
"""

def main():
    # Removed emoji from print statement to prevent Windows encoding errors
    print("Initializing WBSU-AI-Lab-Assistant Repository...")
    
    create_file("README.md", readme_content)
    create_file("CODE_OF_CONDUCT.md", coc_content)
    create_file("SECURITY.md", security_content)
    create_file("LICENSE", license_content)
    create_file(".gitignore", gitignore_content)
    create_file("requirements.txt", requirements_content)
    
    print("\nRepository setup complete! You can now run 'streamlit run wbsu_lab_assistant.py'")

if __name__ == "__main__":
    main()