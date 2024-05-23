import asyncio
import tempfile
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Mailbox
from config import settings

class CustomHandler(Mailbox):
    def __init__(self, mail_dir):
        super().__init__(mail_dir)

    async def handle_DATA(self, server, session, envelope):
        print("Message data:\n", envelope.content.decode("utf8", errors="replace"))
        return "250 Message accepted for delivery"


async def start_server():
    with tempfile.TemporaryDirectory() as mail_dir:
        controller = Controller(
            CustomHandler(mail_dir), hostname=settings.SMTP_URL, port=settings.SMTP_PORT
        )
        controller.start()
        print(f"SMTP server started on {settings.SMTP_URL}:{settings.SMTP_PORT}")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            controller.stop()
            print("SMTP server stopped")


if __name__ == "__main__":
    asyncio.run(start_server())
