from flask_mail import Message

from app.config import Config
from app.core.services.mail.mail_config import MailConfig


class MailService:

    @staticmethod
    def send_mail(
            to: str,
            subject: str,
            body: str = '',
            html: str | None = None,
    ):

        try:
            msg = Message(
                subject=subject,
                recipients=[to],
                body=body,
                html=html,
            )

            MailConfig.mail.send(msg)

            print(f'Mail sent to {to}')

        except Exception as e:
            raise Exception(f'Send mail failed: {str(e)}')

    @staticmethod
    def send_doctor_account_email(doctor_name, doctor_email='cnatro23@gmail.com', ):

        html = f"""
        <h2>MediGo</h2>

        <p>Xin chào bác sĩ <b>{doctor_name}</b>,</p>

        <p>Tài khoản của bạn đã được tạo thành công.</p>

        <ul>
            <li>Email: {doctor_email}</li>
            <li>PASS: 123</li>
        </ul>

        <p>
            Đăng nhập:
            <a href="{Config.MOMO_RETURN_URL}">
                MediGo
            </a>
        </p>
        """

        MailService.send_mail(
            to=doctor_email,
            subject='Tài khoản bác sĩ MediGo',
            html=html,
        )

    @staticmethod
    def send_appointment_success_email(
            patient_name: str,
            doctor_name: str,
            appointment_date: str,
            appointment_time: str,
            patient_email: str = 'cnatro23@gmail.com',
    ):

        html = f"""
        <h2>MediGo</h2>

        <p>Xin chào <b>{patient_name}</b>,</p>

        <p>Bạn đã đặt lịch khám thành công.</p>

        <ul>
            <li>Bác sĩ: {doctor_name}</li>
            <li>Ngày khám: {appointment_date}</li>
            <li>Giờ khám: {appointment_time}</li>
        </ul>

        <p>Cảm ơn bạn đã sử dụng MediGo.</p>
        """

        MailService.send_mail(
            to=patient_email,
            subject='Đặt lịch khám thành công',
            html=html,
        )

    @staticmethod
    def send_refund_success_email(
            patient_name: str,
            amount: float,
            doctor_name: str,
            appointment_date: str,
            appointment_time: str,
            patient_email: str = 'cnatro23@gmail.com',
    ):

        html = f"""
        <div style="
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: auto;
            padding: 24px;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
        ">

            <h2 style="color: #4f46e5;">
                MediGo - Hoàn tiền thành công
            </h2>

            <p>
                Xin chào <b>{patient_name}</b>,
            </p>

            <p>
                Yêu cầu hoàn tiền cho lịch hẹn khám bệnh của bạn đã được xử lý thành công.
            </p>

            <div style="
                background: #f9fafb;
                padding: 16px;
                border-radius: 10px;
                margin: 20px 0;
            ">
                <p><b>Bác sĩ:</b> {doctor_name}</p>
                <p><b>Ngày khám:</b> {appointment_date}</p>
                <p><b>Giờ khám:</b> {appointment_time}</p>
                <p>
                    <b>Số tiền hoàn:</b>
                    <span style="color:#16a34a;">
                        {amount:,.0f} VNĐ
                    </span>
                </p>
            </div>

            <p>
                Tiền sẽ được hoàn về phương thức thanh toán của bạn
                trong vòng 5-15 phút tùy hệ thống ngân hàng/ví điện tử.
            </p>

            <p>
                Cảm ơn bạn đã sử dụng MediGo.
            </p>

        </div>
        """

        MailService.send_mail(
            to=patient_email,
            subject='Hoàn tiền lịch khám thành công',
            html=html,
        )
