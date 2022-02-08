import json

from src.python.whatsapp.models import Chat

chat = Chat()
status = json.loads(chat.get_status_and_save_qr().content.decode())  # Done
print(status)
# chat.get_status_and_save_qr()
# chat.get_name_and_phone()
# chat.send_message()
chat.delete()