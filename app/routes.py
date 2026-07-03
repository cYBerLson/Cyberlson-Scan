from flask import Blueprint, render_template, request, make_response
from app.analyzer import SystemAnalyzer
from app.security import SecurityUtils
from app.recommendations import SecurityRecommendations
from app.report import SecurityReportGenerator
import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page with system overview."""
    system_info = SystemAnalyzer.get_system_info()
    return render_template('index.html', system_info=system_info)

@main_bp.route('/ports')
def ports():
    """Detailed port visibility check."""
    open_ports = SystemAnalyzer.get_open_ports()
    return render_template('ports.html', open_ports=open_ports)

@main_bp.route('/processes')
def processes():
    """Detailed process analyzer."""
    top_processes = SystemAnalyzer.get_top_processes()
    return render_template('processes.html', top_processes=top_processes)

@main_bp.route('/password-check', methods=['GET', 'POST'])
def password_check():
    """Password strength analyzer."""
    analysis = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        analysis = SecurityUtils.analyze_password(password)
    return render_template('password_check.html', analysis=analysis)

@main_bp.route('/recommendations')
def recommendations():
    """Security recommendations based on system analysis."""
    system_info = SystemAnalyzer.get_system_info()
    open_ports = SystemAnalyzer.get_open_ports()

    analysis_data = {
        'cpu': system_info.get('cpu_usage', 0),
        'memory': system_info.get('memory_usage', 0),
        'open_ports': open_ports if isinstance(open_ports, list) else []
    }

    recs_data = SecurityRecommendations.get_recommendations(analysis_data)
    recs = recs_data['recommendations']
    timestamp = recs_data['timestamp']
    risk_score = SecurityRecommendations.calculate_risk_score(analysis_data)

    return render_template('recommendations.html',
                           recommendations=recs,
                           risk_score=risk_score,
                           timestamp=timestamp)

@main_bp.route('/download-report')
def download_report():
    """Generate and download a PDF security report."""
    system_info = SystemAnalyzer.get_system_info()
    open_ports = SystemAnalyzer.get_open_ports()

    analysis_data = {
        'system_info': system_info,
        'open_ports': open_ports if isinstance(open_ports, list) else []
    }

    recs_data = SecurityRecommendations.get_recommendations(analysis_data)
    recs = recs_data['recommendations']
    risk_score = SecurityRecommendations.calculate_risk_score(analysis_data)

    pdf_buffer = SecurityReportGenerator.generate_pdf(analysis_data, recs, risk_score)

    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    filename = f"Cyberlson-Scan -Report-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}.pdf"
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

@main_bp.route('/legal')
def legal():
    """Legal and ethical notice page."""
    return render_template('legal.html')

@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500