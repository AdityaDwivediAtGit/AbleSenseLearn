from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user
import os
from datetime import datetime

from config import config
from models import db, User, Content, LearningProfile, AccessibilityProfile
from ai_services import (
    TextSimplifier, 
    ImageProcessor,
    EngagementAnalyzer,
    PathwayGenerator
)
from api.routes import api_bp
from utils.accessibility_check import AccessibilityChecker

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize extensions
CORS(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if not current_user.is_authenticated:
        return render_template('login.html')
    
    # Get user's learning stats
    recent_content = Content.query.filter_by(user_id=current_user.id)\
        .order_by(Content.created_at.desc())\
        .limit(5)\
        .all()
    
    return render_template('dashboard.html', 
                          user=current_user,
                          recent_content=recent_content)

@app.route('/content/<int:content_id>')
def view_content(content_id):
    """View and interact with content"""
    content = Content.query.get_or_404(content_id)
    
    # Get user's accessibility preferences
    profile = AccessibilityProfile.query.filter_by(user_id=current_user.id).first()
    
    # Adapt content based on preferences
    adapted_content = adapt_content_for_user(content, profile)
    
    return render_template('content_viewer.html',
                          content=adapted_content,
                          accessibility_profile=profile)

@app.route('/tools/accessibility')
def accessibility_tools():
    """Accessibility tools and settings"""
    return render_template('accessibility_tools.html')

@app.route('/api/content/simplify', methods=['POST'])
def simplify_content():
    """Simplify text content using AI"""
    data = request.json
    text = data.get('text', '')
    level = data.get('level', 'intermediate')
    
    simplifier = TextSimplifier()
    simplified = simplifier.simplify(text, level)
    
    return jsonify({
        'original': text,
        'simplified': simplified,
        'level': level
    })

@app.route('/api/image/describe', methods=['POST'])
def describe_image():
    """Generate alt-text for images"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    image_processor = ImageProcessor()
    
    try:
        description = image_processor.generate_alt_text(image_file)
        return jsonify({
            'description': description,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning/pathway', methods=['POST'])
def generate_pathway():
    """Generate personalized learning pathway"""
    data = request.json
    user_id = data.get('user_id')
    topic = data.get('topic')
    difficulty = data.get('difficulty', 'beginner')
    
    generator = PathwayGenerator()
    pathway = generator.generate_pathway(user_id, topic, difficulty)
    
    return jsonify(pathway)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'database': 'connected' if db.session.execute('SELECT 1').first() else 'disconnected',
            'ai_models': 'loaded'
        }
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

def adapt_content_for_user(content, profile):
    """Adapt content based on user's accessibility profile"""
    adapted = content.to_dict()
    
    if profile:
        # Apply text adaptations
        if profile.preferred_font_size:
            adapted['font_size'] = profile.preferred_font_size
        
        if profile.high_contrast_mode:
            adapted['theme'] = 'high-contrast'
        
        # Apply content adaptations
        if profile.requires_simplified_text:
            simplifier = TextSimplifier()
            adapted['body'] = simplifier.simplify(
                content.body, 
                profile.simplification_level
            )
    
    return adapted

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)