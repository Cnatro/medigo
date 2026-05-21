from flask_mail import Mail

from app.config import Config


class MailConfig:

    mail = Mail()

    _initialized = False

    @classmethod
    def initialize(cls, app):

        if cls._initialized:
            return

        try:
            app.config['MAIL_SERVER'] = Config.MAIL_SERVER
            app.config['MAIL_PORT'] = int(Config.MAIL_PORT)
            app.config['MAIL_USE_TLS'] = (
                str(Config.MAIL_USE_TLS).lower() == 'true'
            )

            app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
            app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD

            app.config['MAIL_DEFAULT_SENDER'] = (
                Config.MAIL_DEFAULT_SENDER
            )

            cls.mail.init_app(app)

            cls._initialized = True

            print(' Mail initialized')

        except Exception as e:
            raise Exception(f'Mail init failed: {str(e)}')