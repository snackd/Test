import imaplib
import email as em
from email.header import decode_header
from datetime import datetime
import configparser
import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import re

# 读取 config.ini 文件
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中获取配置信息
IMAP_SERVER = config['EMAIL']['IMAP_SERVER']
EMAIL_ACCOUNT = config['EMAIL']['EMAIL_ACCOUNT']
PASSWORD = config['EMAIL']['PASSWORD']
LABEL = config['EMAIL']['LABEL']
GOOGLE_CREDENTIALS_FILE = config['GOOGLE']['CREDENTIALS_FILE']
GOOGLE_SHEET_URL = config['GOOGLE']['SHEET_URL']

# Google Sheets 认证
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url(GOOGLE_SHEET_URL)
wks = sh.sheet1  # 假设我们要写入第一个工作表

today = datetime.today().strftime('%d-%b-%Y')
# wks = sh.worksheet_by_title(today)
try:
    today1 = datetime.today().strftime('%Y%m%d')
    spreadsheet = gc.open('turnkey 錯誤發票')  # 替换为你的工作表名称

    # 在工作表中添加新的分页
    # new_worksheet = spreadsheet.add_worksheet(title=today1, rows=None, cols=None)
    header = ['email_time', '事件時間', '錯誤代碼', 'invoiceNumber', 'allowanceNumber', 'sellerId', 'buyerId', '訊息']

    worksheet = sh.worksheet(today1)

    # 将标题行写入工作表的第一行
    worksheet.update('A1:H1', [header])
    
    # print(f"New sheet created: {new_worksheet.title}")
except Exception as e:
    print(f"An error occurred while creating new sheet: {e}")
# wks = sh.sheet1 
# today = datetime.today().strftime('%Y-%m-%d')
# worksheet_list = sh.worksheets()
# # 根据日期选择要写入的工作表
# wks = None
# for worksheet in worksheet_list:
#     if worksheet.title == today:
#         wks = worksheet
#         break

# 获取邮件正文的函数
def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    return body
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
            except Exception as e:
                print(f"读取邮件部分出错: {e}")
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
    return body

def match_message(message):
    extracted_info = {}
    extracted_info['error_code'] = ""
    extracted_info['invoice_number'] = ""
    extracted_info['allowance_number'] = ""
    extracted_info['seller_id'] = ""
    extracted_info['buyer_id'] = ""

    # match = re.search(r'\[(.*?)\].*?invoiceNumber=(.*?), Seller=(.*?), buyerId=(.*?), invoiceDate=(.*?)\|.*?\$\$=(.*?)\$\$=(.*?)\$\$=(.*?)\$\$=(.*)', message)

    match = re.search(r'\[(.*?)\].*', message)
    if match:
        extracted_info['error_code'] = match.group(1)

    match = re.search(r'invoiceNumber=(.*?)(?:,|\||$)', message)
    if match:
        extracted_info['invoice_number'] = match.group(1)

    match = re.search(r'InvoiceNumber=(.*?)(?:,|\||$)', message)
    if match:
        extracted_info['invoice_number'] = match.group(1)

    match = re.search(r'_(.*?)_', message)
    if match:
        extracted_info['invoice_number'] = match.group(1)


    match = re.search(r'Seller=(.*?)(?:,|\||$)', message)
    if match:
        extracted_info['seller_id'] = match.group(1)

    match = re.search(r'SellerId=(.*?)(?:,|\||$)', message)
    if match:
        extracted_info['seller_id'] = match.group(1)
     
    match = re.search(r'buyerId=(.*?)(?:,|\||$)', message)
    if match:
        extracted_info['buyer_id'] = match.group(1)
    
    match = re.search(r'invoiceDate=(.*?)(?:,|\||$)', message)
    if match:
        extracted_info['invoice_date'] = match.group(1)
        
        # extracted_info['allowance_number'] = match.group(3)
    match = re.search(r'\$\$=(.*?)\$\$=(.*?)\$\$=(.*?)\$\$=(.*)$', message)
    if match:
        extracted_info['invoice_number'] =   match.group(1) if not extracted_info['invoice_number'] else extracted_info['invoice_number'] 
        extracted_info['invoice_date'] = match.group(2) 
        extracted_info['buyer_id'] = match.group(3)
        extracted_info['seller_id'] = match.group(4) if not extracted_info['seller_id'] else extracted_info['seller_id']

    match = re.search(r'\|(.*?)\$\$=(.*?)\$\$=(.*?)\$\$=(.*?)$', message)
    if match:
        extracted_info['invoice_number'] =  match.group(1)  if not extracted_info['invoice_number'] else extracted_info['invoice_number'] 
        extracted_info['invoice_date'] = match.group(2)
        extracted_info['buyer_id'] = match.group(3)
        extracted_info['seller_id'] = match.group(4) if not extracted_info['seller_id'] else extracted_info['seller_id']

    return extracted_info

def main():
    try:
        # 连接到IMAP服务器并登录
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)

        status = None
        messages = None

        # 选择特定标签（Gmail 中的标签是[Gmail]/标签名）
        status, messages = mail.select(LABEL)
        # status, messages = mail.search(None, 'ALL')
        if status != "OK":
            print(f"无法选择标签 {LABEL}")
            exit()

        # 搜索当天的所有邮件
        status, messages = mail.search(None, f'(SINCE {today})')
        if status != "OK":
            print(f"搜索邮件失败")
            exit()

        # 获取邮件ID列表
        email_ids = messages[0].split()
        
        # 如果没有当天的邮件
        if not email_ids:
            print("今天没有邮件")
            mail.close()
            mail.logout()
            exit()

        # 准备保存邮件内容
        email_contents = []

        # 处理所有当天的邮件
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = em.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    if subject != "電子發票客戶端連線程式郵件通知":
                        continue
                    from_ = msg.get("From")
                    date_tuple = em.utils.parsedate_tz(msg["Date"])
                    if date_tuple:
                        local_date = datetime.fromtimestamp(em.utils.mktime_tz(date_tuple))
                        date_str = local_date.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        date_str = None
                    body = get_body(msg)
                    email_contents.append({
                        'subject': subject,
                        'from': from_,
                        'date': date_str,
                        'body': body
                    })

        # 关闭邮件连接
        mail.close()
        mail.logout()

    
        # 解析邮件内容并写入 Google Sheets
        rows = []
        for email in email_contents:
            soup = BeautifulSoup(email['body'], 'html.parser')
            table = soup.find('table')
            if table:
                is_header_row = True  # 表示当前行是否为表头行
                for row in table.find_all('tr'):
                    # 检查是否为标题行
                    if is_header_row:
                        is_header_row = False
                        continue  # 跳过标题行，继续下一行
                    cols = row.find_all(['td', 'th'])
                    if len(cols) == 3:
                        event_time = cols[0].text.strip()
                        error_code = cols[1].text.strip()
                        ori_message = cols[2].text.strip()
                        extracted_info = match_message(ori_message)

                        rows.append([email['date'], event_time, extracted_info['error_code'], extracted_info['invoice_number'], extracted_info['allowance_number'], extracted_info['seller_id'], extracted_info['buyer_id'], ori_message])

        # print(rows)
        # 写入 Google Sheets
        if rows:
            wks.append_rows(values=rows)
            print("finished")

    except imaplib.IMAP4.error as e:
        print(f"IMAP 连接失败: {e}")


if __name__ == "__main__":
    main()


