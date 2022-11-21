import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def get_params(param, message = None, args = sys.argv):
    params = args

    if params.count(param) > 0:
        return params[params.index(param) + 1]
    else:
        if message is not None:
            print(message)
        return None

def get_emails(param, message = None):
    emails = []
    to_count = sys.argv.count(param)
    args = sys.argv

    for i in range(to_count):
        emails.append(get_params(param, message, args))
        args = args[args.index(param) + 1:]
        
    return emails

def read_html(path):
    with open(path, 'r') as f:
        return f.read()

def show_help():
    print('''
    Usage: python3 main.py -f <from> -t <to> -s <subject> -m <message> -a <file> -k <key>
    -f: Sender email address
    -t: Recipient email address (can be used multiple times)
    -s: Subject of the email
    -m: Message of the email 
    -a: Path to the html file (it replaced the message if both are specified)
    -k: SendGrid API key
    ''')

def main():
    if sys.argv.count('-h') > 0:
        show_help()
        return

    print("[Core] Initializing...")
    from_user = get_params('-f', '[Error] No sender specified (-f)')
    to = get_emails('-t', '[Error] No recipient specified (-t)')
    subject = get_params('-s', '[Error] No subject specified (-s)')
    message = get_params('-m')
    file = get_params('-a')
    key = get_params('-k', '[Error] No API key specified (-k)')
    html = read_html(file) if file is not None else None
    body = html if file is not None else message

    if body is None:
        print('[Error] No file (-a) or message (-m) specified')
        exit()

    for mail in to:
        try:
            message = Mail(
            from_email=from_user,
            to_emails=mail,
            subject=subject,
            html_content=body)
            
            sg = SendGridAPIClient(key)
            sg.send(message)
            print('[Success] Email sent to ' + mail)

        except Exception as e:
            print("[Error] Error to send mail to " + mail + " (" + str(e) + ")")
            continue

    print("[Core] Finished script")

if __name__ == "__main__":
    main()