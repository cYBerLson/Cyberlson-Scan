import math
import re
import datetime

class SecurityUtils:
    """Security utility functions for password analysis and data sanitization."""

    @staticmethod
    def calculate_entropy(password):
        """Calculate password entropy in bits."""
        if not password:
            return 0

        # Determine effective character set size
        charset = set()
        if re.search(r'[a-z]', password): charset.update("abcdefghijklmnopqrstuvwxyz")
        if re.search(r'[A-Z]', password): charset.update("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if re.search(r'[0-9]', password): charset.update("0123456789")
        if re.search(r'[^a-zA-Z0-9]', password): charset.update("!@#$%^&*()-_=+[]{}|;:,.<>?/`~")

        if not charset:
            return 0

        entropy = len(password) * math.log2(len(charset))
        return round(entropy, 2)

    @staticmethod
    def analyze_password(password):
        """Perform detailed analysis of password strength."""
        if not password:
            return {
                "score": 0,
                "status": "Empty",
                "entropy": 0,
                "feedback": ["Please enter a password."],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        entropy = SecurityUtils.calculate_entropy(password)
        feedback = []

        # Length checks
        if len(password) < 8:
            feedback.append("Password is too short. Minimum 8 characters required, 12+ recommended.")
        elif len(password) < 12:
            feedback.append("Password length is acceptable but 12+ is better.")

        # Complexity checks
        if not re.search(r'[A-Z]', password):
            feedback.append("Include uppercase letters for better security.")
        if not re.search(r'[0-9]', password):
            feedback.append("Include numbers for better security.")
        if not re.search(r'[^a-zA-Z0-9]', password):
            feedback.append("Include special characters for better security.")

        # Common dictionary patterns
        common_patterns = ['password', '123456', 'qwerty', 'admin', 'welcome']
        if any(pattern in password.lower() for pattern in common_patterns):
            feedback.append("Avoid common dictionary words or simple patterns.")

        # Score mapping
        if entropy < 40:
            status, score = "Very Weak", 1
        elif entropy < 60:
            status, score = "Weak", 2
        elif entropy < 80:
            status, score = "Moderate", 3
        elif entropy < 100:
            status, score = "Strong", 4
        else:
            status, score = "Very Strong", 5

        return {
            "score": score,
            "status": status,
            "entropy": entropy,
            "feedback": feedback if feedback else ["Excellent password strength!"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def sanitize_input(user_input):
        """Basic input sanitization to prevent common injection attacks."""
        if not isinstance(user_input, str):
            return user_input
        sanitized = re.sub(r'[<>&"\'`]', '', user_input)
        return sanitized.strip()
    