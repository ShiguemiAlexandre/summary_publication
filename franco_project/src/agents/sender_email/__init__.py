import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from dotenv import load_dotenv
import os
from datetime import datetime
import logging

load_dotenv()

class SenderEmail:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.SENDER = os.getenv("EMAIL_USERNAME")
        self.PASSWORD = os.getenv("EMAIL_PASSWORD")

        self.RECIPIENT = [
            os.getenv("EMAIL_RECIPIENT"),
            "shiguemialexandre@gmail.com",
            "japantechsolutions@gmail.com"
        ]

    def _construct_email(self, quantity: int):
        msg = MIMEMultipart()
        msg["From"] = self.SENDER
        msg["To"] = ", ".join(self.RECIPIENT)
        msg["Subject"] = f"Resumo de Publicações Judiciais – {datetime.now().strftime('%d/%m/%Y')}"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #ffffff; color: #000000;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 30px; border-radius: 8px; background-color: #fff;">
            <img src="https://i.imgur.com/YbAmnmm.jpeg" alt="Logo" style="width: 150px; margin-bottom: 20px;" />
            <h2 style="color: #d00000;">Resumo das Publicações Judiciais</h2>
            <p>Prezados,</p>
            <p>Segue em anexo a planilha contendo o resumo das publicações judiciais atualizadas.</p>
            <p><strong>Total de publicações:</strong> {quantity}</p>
            <p style="margin-top: 40px;">
                Atenciosamente,<br />
                <strong style="color: #d00000;">JapanTech</strong><br />
                Departamento de Desenvolvimento
            </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, "html"))

        return msg
    
    def _send_message(self, msg):
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(self.SENDER, self.PASSWORD)
            servidor.send_message(msg)

    def send(self, df: bytes, quantity: int):
        msg = self._construct_email(quantity=quantity)
        
        part = MIMEApplication(df, Name="resumo_publicacoes.xlsx")
        part["Content-Disposition"] = 'attachment; filename="resumo_publicacoes.xlsx"'
        msg.attach(part)

        self._send_message(msg=msg)

        self.logger.info("Email enviado com sucesso")


