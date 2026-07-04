# Cyberlson Scan – Personal Defensive Security Audit Toolkit
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

![Cyberlson Scan Banner] <p align="center">
  <img src="static/images/banner.png" alt="Cyberlson Scan Banner" width="100%">
</p>
## Project Overview

Cyberlson-Scan is a web-based, Flask-powered personal defensive security audit toolkit designed to empower individuals to safely and locally evaluate their own system's security posture. Built with a strong emphasis on secure coding practices and defensive cybersecurity principles, this tool provides insights into system information, open ports, process activity, and password strength, offering actionable recommendations to enhance personal digital security. It is 100% defensive, legal, and educational, explicitly avoiding any offensive capabilities, exploit code, or malware.

## Features

Cyberlson Scan offers a suite of defensive features to help users understand and improve their system's security:

*   **System Information Viewer**: Displays essential system details such as OS version, CPU, memory, and disk usage, along with running services (read-only).
*   **Safe Local Port Visibility Check**: Identifies currently open ports on the local machine, providing clear explanations without aggressive scanning.
*   **Password Strength Analyzer**: Evaluates password entropy and detects common weaknesses, offering educational feedback and improvement suggestions.
*   **Process Analyzer**: Shows top processes by CPU/memory usage and flags unusual resource spikes with educational context.
*   **Security Recommendations Engine**: Provides rule-based suggestions (e.g., firewall checks for many open ports, password manager recommendations for weak passwords).
*   **Generate Security Report**: Creates a downloadable PDF report with a summary risk score, timestamp, and professional formatting.
*   **Legal & Ethical Notice Page**: Clearly outlines the tool's purpose for personal defensive use only, prohibiting unauthorized testing or network-wide scanning.

##  Architecture Overview

Cyberlson Scan follows a modular Flask architecture that separates the user interface, application logic, system analysis, and report generation.

```text
                          +----------------------+
                          |    User Browser      |
                          +----------+-----------+
                                     |
                                  HTTPS
                                     |
                          +----------v-----------+
                          |   Nginx (Optional)   |
                          +----------+-----------+
                                     |
                                 Gunicorn
                                     |
                          +----------v-----------+
                          |  Cyberlson Scan App  |
                          |       (Flask)        |
                          +----------+-----------+
                                     |
          +--------------------------+--------------------------+
          |                          |                          |
          |                          |                          |
+---------v---------+      +---------v---------+      +---------v---------+
|   security.py     |      |   analyzer.py     |      | recommendations.py|
| Password Analysis |      | System Analysis   |      | Risk Suggestions  |
+---------+---------+      +---------+---------+      +---------+---------+
          |                          |                          |
          +--------------------------+--------------------------+
                                     |
                          +----------v-----------+
                          |     report.py        |
                          | PDF Report Generator |
                          +----------+-----------+
                                     |
                          +----------v-----------+
                          |    ReportLab PDF     |
                          +----------------------+

                    Frontend
        +--------------------------------------+
        | templates/ (HTML - Jinja2)           |
        | static/css                           |
        | static/js                            |
        | static/images                        |
        +--------------------------------------+

                 External Libraries
        +--------------------------------------+
        | psutil      → System Information      |
        | bcrypt     → Password Hashing         |
        | ReportLab  → PDF Report Generation    |
        +--------------------------------------+
```

### Project Structure

```text
Cyberlson-scan/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── analyzer.py
│   ├── security.py
│   ├── recommendations.py
│   ├── report.py
│   └── config.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   └── index.html
│
├── uploads/
├── requirements.txt
├── run.py
└── README.md
```

## Security Considerations

Cyberlson Scan is built with security as a paramount concern, adhering to DevSecOps best practices and OWASP secure coding guidelines. Key security measures include:

*   **Environment Variables**: All sensitive configurations (e.g., `SECRET_KEY`) are loaded from environment variables, preventing hardcoding of secrets.
*   **Flask Production Configuration**: Configured for production environments, disabling debug mode and enabling robust error handling.
*   **CSRF Protection**: Implemented using Flask-WTF to protect against Cross-Site Request Forgery attacks.
*   **Input Validation & Sanitization**: All user inputs are sanitized and validated to prevent common vulnerabilities like XSS (Cross-Site Scripting) and SQL Injection (though no database is used, this is a general best practice).
*   **Secure Headers**: Utilizes Flask-Talisman to enforce HTTP Strict Transport Security (HSTS) and Content Security Policy (CSP), mitigating various web-based attacks.
*   **Safe Subprocess Usage**: System interactions are performed via `psutil`, which provides a safe, cross-platform interface for system information, avoiding direct, potentially unsafe subprocess calls.
*   **Error Handling**: Comprehensive exception handling is in place to prevent information leakage and ensure application stability.
*   **Defensive-Only Design**: The core philosophy ensures no offensive capabilities, network scanning beyond localhost, or any potentially illegal functionalities are included.

## Screenshots Section (Placeholder Descriptions)

*   **Dashboard View**: A clean, modern dashboard displaying real-time CPU, memory, and disk usage, along with essential system information.
*   **Open Ports List**: A table showing locally open ports, their associated processes, and clear explanations.
*   **Password Analysis Result**: An interactive display of password strength, entropy, and specific feedback for improvement.
*   **Security Recommendations**: A categorized list of actionable security recommendations based on system analysis, with risk levels.
*   **PDF Report Sample**: A professional, downloadable PDF report summarizing the audit findings and recommendations.

## Installation Instructions

### Local Development Setup

1.  **Clone the repository (or download the project files):**
    ```bash
    git clone https://github.com/cYBerLson/Cyberlson-Scan.git
cd Cyberlson-Scan
    ```

2.  **Create a Python Virtual Environment:**
    ```bash
    ### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and set a strong `SECRET_KEY`:
    ```ini
    SECRET_KEY='your_very_long_and_random_secret_key_here'
    FLASK_CONFIG='development'
    ```

5.  **Run the Application Securely:**
    ```bash
    flask run
    # Or using the provided run.py:
    # python run.py
    ```
    The application will typically be available at `http://127.0.0.1:5000`.

## Usage Instructions

Navigate to the application in your web browser. The intuitive interface allows you to:

*   View system statistics on the **Dashboard**.
*   Check for listening ports under the **Ports** section.
*   Analyze running processes in the **Processes** tab.
*   Test the strength of a password on the **Password Check** page.
*   Generate a comprehensive **Security Report** with personalized recommendations.
*   Review the **Legal & Ethical Notice** for proper usage guidelines.

## Deployment Instructions

Refer to `DEPLOYMENT.md` for detailed instructions on deploying Cyberlson Scan to production environments.

## Future Improvements

*   **Advanced Process Analysis**: Implement more sophisticated logic for flagging suspicious process behavior (e.g., processes running from unusual directories).
*   **File Integrity Monitoring (Local)**: Add a feature to monitor critical system files for unauthorized changes (read-only, hash-based).
*   **Scheduled Scans**: Allow users to schedule regular security checks and receive summarized reports.
*   **User Authentication (Optional)**: For multi-user environments (e.g., small teams), implement secure user authentication and role-based access control.
*   **Enhanced UI/UX**: Further refine the user interface with more interactive elements and visualizations.

## Contribution Guidelines

We welcome contributions to Cyberlson Scan! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Ensure your code adheres to secure coding practices and passes all tests.
4.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Professional GitHub Project Description (Short)

**Cyberlson-Scan**: is a Flask-based defensive cybersecurity toolkit for local system security auditing. It provides system monitoring, local port visibility, password strength analysis, process inspection, and automated security recommendations while following secure coding and DevSecOps best practices.

## Suggested GitHub Tags

`python`, `flask`, `cybersecurity`, `security-audit`, `defensive-security`, `devsecops`, `web-application`, `system-monitoring`, `password-security`, `personal-security`, `education`, `mit-license`

---

#  Author

**Abdulmajid Bello**

Founder, **Cyberlson Team Tech**

### Contact

- **GitHub:** https://github.com/cYBerLson
- **LinkedIn:** https://linkedin.com/in/cyberlsonsc
- **Email:** cyberlsoncs@gmail.com

