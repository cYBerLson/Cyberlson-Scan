import datetime

class SecurityRecommendations:
    """Security recommendations engine."""

    @staticmethod
    def get_recommendations(analysis_data):
        """Generate rule-based suggestions based on system analysis."""
        recommendations = []

        cpu = analysis_data.get('cpu_usage') or analysis_data.get('cpu', 0)
        mem = analysis_data.get('memory_usage') or analysis_data.get('memory', 0)
        open_ports = analysis_data.get('open_ports', [])

        # CPU/Memory Recommendations
        if cpu > 80:
            recommendations.append({
                "category": "Resource Management",
                "recommendation": "High CPU usage detected. Monitor resource-intensive processes using Task Manager or 'top'.",
                "risk_level": "Medium"
            })

        if mem > 90:
            recommendations.append({
                "category": "Resource Management",
                "recommendation": "Memory usage is very high. Consider closing unused applications or increasing RAM if this persists.",
                "risk_level": "Medium"
            })

        # Open Ports Recommendations
        if len(open_ports) > 10:
            recommendations.append({
                "category": "Network Security",
                "recommendation": "Multiple open ports detected. Review firewall settings and ensure only necessary services are exposed.",
                "risk_level": "Medium"
            })

        # Common risky ports check
        risky_ports = {
            21: "FTP (Unencrypted file transfer)",
            23: "Telnet (Unencrypted remote access)",
            445: "SMB (File sharing - potential for lateral movement if unpatched)",
            3389: "RDP (Remote Desktop Protocol - ensure it's behind a VPN/MFA)"
        }

        for port_info in open_ports:
            port = port_info.get('port')
            if port in risky_ports:
                recommendations.append({
                    "category": "Network Security",
                    "recommendation": f"Port {port} ({risky_ports[port]}) is open. Ensure this is necessary and properly secured.",
                    "risk_level": "High"
                })

        # Identity Protection
        recommendations.extend([
            {
                "category": "Identity Protection",
                "recommendation": "Use a reputable password manager (e.g., Bitwarden, 1Password) to manage unique, strong passwords.",
                "risk_level": "Low"
            },
            {
                "category": "Identity Protection",
                "recommendation": "Enable Multi-Factor Authentication (MFA) on all critical accounts where possible.",
                "risk_level": "Low"
            }
        ])

        # OS Updates
        recommendations.append({
            "category": "System Integrity",
            "recommendation": "Ensure your operating system and all installed software are up-to-date with the latest security patches.",
            "risk_level": "High"
        })

        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": recommendations
        }

    @staticmethod
    def calculate_risk_score(analysis_data):
        """Calculate a summary risk score (Low/Medium/High)."""
        score = 0
        open_ports = analysis_data.get('open_ports', [])
        cpu = analysis_data.get('cpu_usage') or analysis_data.get('cpu', 0)
        mem = analysis_data.get('memory_usage') or analysis_data.get('memory', 0)

        # Port-based risk
        if len(open_ports) > 15:
            score += 30
        elif len(open_ports) > 5:
            score += 15

        # Resource-based risk
        if cpu > 90:
            score += 10
        if mem > 90:
            score += 10

        # Risky ports
        risky_ports = [21, 23, 445, 3389]
        for port_info in open_ports:
            if port_info.get('port') in risky_ports:
                score += 20

        # Final evaluation
        if score < 20:
            return "Low"
        elif score < 50:
            return "Medium"
        else:
            return "High"