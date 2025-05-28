from src.web import create_app
from src.web.helpers.extensions import mail


app = create_app()

# Configure mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='diamondcodedev@gmail.com',
    MAIL_PASSWORD='dywt tizx ywps iwlp', #contra del mail: admin123 (creo xd)
)

mail.init_app(app)

if __name__ == "__main__":
    app.run()
