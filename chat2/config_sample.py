#
# This is where you put all of your secret settings.
#
# The licence (AGPL) does not apply to this file, obviously, but 
#    just in case somebody feels like rules-lawyering.
#
import datetime

server = "example.com:8080"
websocket_server = "example.com:8081"
websocket_ip = "10.1.1.2"
websocket_port = 8081
web_port = 8080

operator = "Bob <bob@example.com>"
operator_name = "Bob"

mail_server = 'mail.example.com'
mail_user = 'bob@example.com'
mail_password = 'Sekr1t_p455w0rD'

password_salt = "herpderp1234"

timezone = datetime.timedelta(hours=10)
static_path = '/home/pi/chat2/static'
