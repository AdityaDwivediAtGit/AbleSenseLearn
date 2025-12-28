@echo off
set ROOT=C:\Users\dwive\OneDrive\Documents\AbleSenseLearn

echo Creating project structure...

:: Root directory
mkdir %ROOT%

:: Root files
type nul > %ROOT%\README.md
type nul > %ROOT%\requirements.txt
type nul > %ROOT%\config.py
type nul > %ROOT%\.env.example
type nul > %ROOT%\app.py
type nul > %ROOT%\setup_database.py

:: ---------------------------
:: MODELS
:: ---------------------------
mkdir %ROOT%\models
type nul > %ROOT%\models\__init__.py
type nul > %ROOT%\models\user.py
type nul > %ROOT%\models\content.py
type nul > %ROOT%\models\learning.py

:: ---------------------------
:: AI SERVICES
:: ---------------------------
mkdir %ROOT%\ai_services
type nul > %ROOT%\ai_services\__init__.py
type nul > %ROOT%\ai_services\text_simplifier.py
type nul > %ROOT%\ai_services\image_processor.py
type nul > %ROOT%\ai_services\engagement_analyzer.py
type nul > %ROOT%\ai_services\pathway_generator.py
type nul > %ROOT%\ai_services\voice_services.py

:: ---------------------------
:: API
:: ---------------------------
mkdir %ROOT%\api
type nul > %ROOT%\api\__init__.py
type nul > %ROOT%\api\routes.py
type nul > %ROOT%\api\auth.py
type nul > %ROOT%\api\content_api.py

:: ---------------------------
:: STATIC (css/js/images)
:: ---------------------------
mkdir %ROOT%\static
mkdir %ROOT%\static\css
mkdir %ROOT%\static\css\themes
mkdir %ROOT%\static\js
mkdir %ROOT%\static\images
mkdir %ROOT%\static\images\logos

:: CSS files
type nul > %ROOT%\static\css\main.css
type nul > %ROOT%\static\css\accessibility.css
type nul > %ROOT%\static\css\themes\high-contrast.css
type nul > %ROOT%\static\css\themes\dyslexia-friendly.css
type nul > %ROOT%\static\css\themes\low-distraction.css

:: JS files
type nul > %ROOT%\static\js\main.js
type nul > %ROOT%\static\js\accessibility.js
type nul > %ROOT%\static\js\voice_commands.js
type nul > %ROOT%\static\js\engagement_tracker.js

:: ---------------------------
:: TEMPLATES
:: ---------------------------
mkdir %ROOT%\templates
mkdir %ROOT%\templates\admin

type nul > %ROOT%\templates\base.html
type nul > %ROOT%\templates\index.html
type nul > %ROOT%\templates\login.html
type nul > %ROOT%\templates\dashboard.html
type nul > %ROOT%\templates\profile_setup.html
type nul > %ROOT%\templates\content_viewer.html
type nul > %ROOT%\templates\accessibility_tools.html

type nul > %ROOT%\templates\admin\admin.html
type nul > %ROOT%\templates\admin\analytics.html

:: ---------------------------
:: UTILS
:: ---------------------------
mkdir %ROOT%\utils
type nul > %ROOT%\utils\__init__.py
type nul > %ROOT%\utils\validators.py
type nul > %ROOT%\utils\security.py
type nul > %ROOT%\utils\accessibility_check.py
type nul > %ROOT%\utils\content_parser.py

:: ---------------------------
:: TESTS
:: ---------------------------
mkdir %ROOT%\tests
type nul > %ROOT%\tests\__init__.py
type nul > %ROOT%\tests\test_api.py
type nul > %ROOT%\tests\test_ai_services.py
type nul > %ROOT%\tests\test_accessibility.py

:: ---------------------------
:: DATA
:: ---------------------------
mkdir %ROOT%\data
mkdir %ROOT%\data\sample_content
mkdir %ROOT%\data\ml_models

type nul > %ROOT%\data\sample_content\science_lesson.txt
type nul > %ROOT%\data\sample_content\math_problem.json

:: ---------------------------
:: DOCS
:: ---------------------------
mkdir %ROOT%\docs
type nul > %ROOT%\docs\api_documentation.md
type nul > %ROOT%\docs\setup_guide.md
type nul > %ROOT%\docs\accessibility_guidelines.md

echo.
echo Project structure created successfully!
pause
