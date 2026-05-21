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
    def send_doctor_account_email(
            doctor_name: str,
            doctor_email: str = 'cnatro23@gmail.com',
            password: str = '123',
    ):

        html = f"""
        <div style="
            font-family: Arial, sans-serif;
            max-width: 620px;
            margin: auto;
            background: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        ">

            <div style="
                background: linear-gradient(135deg,#6366f1,#8b5cf6);
                padding: 28px;
                text-align: center;
                color: white;
            ">
                <h1 style="margin:0;font-size:28px;">
                    MediGo
                </h1>

                <p style="
                    margin-top:10px;
                    opacity:0.9;
                    font-size:14px;
                ">
                    Hệ thống quản lý khám bệnh thông minh
                </p>
            </div>

            <div style="padding:32px;">

                <h2 style="
                    margin-top:0;
                    color:#111827;
                ">
                    Xin chào bác sĩ {doctor_name},
                </h2>

                <p style="
                    color:#4b5563;
                    line-height:1.7;
                ">
                    Tài khoản bác sĩ của bạn trên hệ thống
                    <b>MediGo</b> đã được tạo thành công.
                </p>

                <div style="
                    background:#f9fafb;
                    border-radius:12px;
                    padding:20px;
                    margin:24px 0;
                    border:1px solid #e5e7eb;
                ">

                    <p style="margin:0 0 12px 0;">
                        <b>Email đăng nhập:</b>
                        {doctor_email}
                    </p>

                    <p style="margin:0;">
                        <b>Mật khẩu tạm thời:</b>
                        {password}
                    </p>

                </div>

                <div style="text-align:center;margin:32px 0;">
                    <a
                        href="{Config.MOMO_RETURN_URL}/login"
                        style="
                            background:linear-gradient(135deg,#6366f1,#8b5cf6);
                            color:white;
                            text-decoration:none;
                            padding:14px 28px;
                            border-radius:10px;
                            display:inline-block;
                            font-weight:bold;
                        "
                    >
                        Đăng nhập MediGo
                    </a>
                </div>

                <p style="
                    color:#ef4444;
                    font-size:14px;
                    line-height:1.6;
                ">
                    Vui lòng đổi mật khẩu sau lần đăng nhập đầu tiên
                    để đảm bảo an toàn tài khoản.
                </p>

                <hr style="
                    border:none;
                    border-top:1px solid #e5e7eb;
                    margin:28px 0;
                ">

                <p style="
                    color:#6b7280;
                    font-size:13px;
                    text-align:center;
                ">
                    © MediGo Healthcare Platform
                </p>

            </div>
        </div>
        """

        MailService.send_mail(
            to=doctor_email,
            subject='[MediGo] Tài khoản bác sĩ của bạn',
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
        <div style="
            font-family: Arial, sans-serif;
            max-width: 620px;
            margin: auto;
            background: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        ">

            <div style="
                background: linear-gradient(135deg,#10b981,#059669);
                padding: 28px;
                text-align: center;
                color: white;
            ">

                <h1 style="margin:0;font-size:28px;">
                    MediGo
                </h1>

                <p style="
                    margin-top:10px;
                    opacity:0.9;
                    font-size:14px;
                ">
                    Đặt lịch khám thành công
                </p>

            </div>

            <div style="padding:32px;">

                <h2 style="
                    margin-top:0;
                    color:#111827;
                ">
                    Xin chào {patient_name},
                </h2>

                <p style="
                    color:#4b5563;
                    line-height:1.7;
                ">
                    Bạn đã đặt lịch khám thành công trên hệ thống
                    <b>MediGo</b>.
                </p>

                <div style="
                    background:#f9fafb;
                    border-radius:12px;
                    padding:20px;
                    margin:24px 0;
                    border:1px solid #e5e7eb;
                ">

                    <p style="margin:0 0 12px 0;">
                        <b>Bác sĩ:</b>
                        {doctor_name}
                    </p>

                    <p style="margin:0 0 12px 0;">
                        <b>Ngày khám:</b>
                        {appointment_date}
                    </p>

                    <p style="margin:0;">
                        <b>Giờ khám:</b>
                        {appointment_time}
                    </p>

                </div>

                <div style="
                    background:#ecfdf5;
                    color:#047857;
                    padding:16px;
                    border-radius:10px;
                    margin-top:24px;
                    font-size:14px;
                    line-height:1.6;
                ">
                    Vui lòng đến trước giờ hẹn khoảng
                    <b>15 phút</b> để làm thủ tục khám bệnh.
                </div>

                <hr style="
                    border:none;
                    border-top:1px solid #e5e7eb;
                    margin:28px 0;
                ">

                <p style="
                    color:#6b7280;
                    font-size:13px;
                    text-align:center;
                ">
                    Cảm ơn bạn đã sử dụng MediGo
                </p>

            </div>
        </div>
        """

        MailService.send_mail(
            to=patient_email,
            subject='[MediGo] Đặt lịch khám thành công',
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
                Yêu cầu hoàn tiền cho lịch hẹn khám bệnh của bạn
                đã được xử lý thành công.
            </p>

            <div style="
                background: #f9fafb;
                padding: 16px;
                border-radius: 10px;
                margin: 20px 0;
            ">

                <p>
                    <b>Bác sĩ:</b>
                    {doctor_name}
                </p>

                <p>
                    <b>Ngày khám:</b>
                    {appointment_date}
                </p>

                <p>
                    <b>Giờ khám:</b>
                    {appointment_time}
                </p>

                <p>
                    <b>Số tiền hoàn:</b>

                    <span style="
                        color:#16a34a;
                        font-weight:bold;
                    ">
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
            subject='[MediGo] Hoàn tiền lịch khám thành công',
            html=html,
        )
