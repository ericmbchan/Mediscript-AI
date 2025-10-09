import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', '5000')),
        debug=app.config.get('DEBUG', False),
    )
