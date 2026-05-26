import os
from dotenv import load_dotenv
from src.web import create_app
from src.web.helpers.extensions import mail

load_dotenv()

app = create_app()

# Configure mail
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True').lower() == 'true',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
)

mail.init_app(app)

if __name__ == "__main__":
    app.run()
