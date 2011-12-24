#!/usr/bin/python2.7
import smtplib
import imaplib
import getpass
import email
import pickle
import base64
import os
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
import mimetypes

def get_int(string=''):
  while True:
    try:
      n=int(raw_input(string))
      break
    except ValueError:
      print 'Enter int'
  return n

def send_mail(user,server):
  fromaddr = raw_input('Send mail by the name of: ')
  tolist = raw_input('To: ').split()
  sub = raw_input('Subject: ')
  
  msg = email.MIMEMultipart.MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = email.Utils.COMMASPACE.join(tolist)
  msg['Subject'] = sub  
  msg.attach(MIMEText(raw_input('Body: ')))
  msg.attach(MIMEText('\n\n\nsent via python', 'plain'))
  n=42
  while n != 0:
    n = get_int('1. Attach\n0. Send\nChoose an option: ') 
    if n==1:
      msg = attach_files(msg)
    elif n==0: 
      server.sendmail(user,tolist,msg.as_string())
      print 'sent'
  
  return
  
def attach_files(msg):
  
  filename = raw_input('File name: ')
  try:
    f = open(filename,'rb')
  except IOError:
    print 'Attachment not found'
    return msg
  
  ctype, encoding = mimetypes.guess_type(filename)
  
  if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
    
  maintype, subtype = ctype.split('/', 1)
        
  if maintype == 'text':
    part = MIMEText(f.read(), _subtype=subtype)
  elif maintype == 'image':
    part = MIMEImage(f.read(), _subtype=subtype)
  elif maintype == 'audio':
    part = MIMEAudio(f.read(), _subtype=subtype)
  else:
    part = MIMEBase(maintype, subtype)
    msg.set_payload(f.read())
    
  part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))    
  msg.attach(part)
  f.close()        
  
  return msg
    
def get_mail(mail):
  MailboxList=[]
  status, mailbox_list = mail.list()
  for i in range(len(mailbox_list)):
    MailboxList.append(mailbox_list[i].split('"')[-2])
    print MailboxList[i]
  
  mailbox = raw_input('Enter the name of the mailbox: ')
  
  if mailbox in MailboxList:
    mail.select(mailbox)
    mail = get_unseen(mail)
    
#  mail.logout()
  return  

def get_unseen(mail):
  result, data = mail.uid('search', None, 'UNSEEN')
  uid_list = data[0].split()
  print len(uid_list), 'Unseen emails.'
  get_email(uid_list,mail)
  return mail

def get_email(uid_list,mail):
  for i in range(len(uid_list)):
    email_uid = uid_list[i]
    res, dat = mail.uid('fetch', email_uid, '(RFC822)')
    raw_email = dat[0][1]
    msg = email.message_from_string(raw_email)
    get_email_info(i+1,email_uid,msg)
  return
  
def get_email_info(i,email_uid,msg):
  print ''
  print 'New email:\n'
  print i,'UID:', email_uid, 'Sender:', email.utils.parseaddr(msg['From'])[0],email.utils.parseaddr(msg['From'])[1]      
  print 'Subjct:',msg['Subject']
  print 'Message: '
  print get_body(msg)
  attach_list = get_attach_list(msg)
  print len(attach_list),'Attachments:',attach_list
  n = get_int('1. Download All Attachments\n0. Exit\nChoose an option: ')
  if n==1:
    get_attach(msg)
  return 

def get_body(msg):
  for part in msg.walk():
    content_type = part.get_content_type()
    if content_type == 'text/plain' or content_type =='text/html':
      payload = part.get_payload()
      if payload:
        print payload
  return

def get_attach_list(msg):
  attach_list=[]
  for part in msg.walk():
    filename = part.get_filename()
    if filename:
      attach_list.append(filename)
  return attach_list
  
def get_attach(msg):
  for part in msg.walk():
    filename = part.get_filename()
    if filename:
      fp = open('/home/jay/Downloads/'+filename,'wb')
      fp.write(part.get_payload(decode=True))
      fp.close()
  return  
  
def main():
  user = raw_input('Username: ')
  passw = base64.b64encode(getpass.getpass())
  
  smtp_host = 'smtp.gmail.com'
  smtp_port = 587
  server = smtplib.SMTP()
  server.connect(smtp_host,smtp_port)
  server.ehlo()
  server.starttls()
  server.login(user,base64.b64decode(passw))
  
  imap_host = 'imap.gmail.com'
  mail = imaplib.IMAP4_SSL(imap_host)
  mail.login(user,base64.b64decode(passw))
  n=42
  while n != 0:
    n = get_int('1. Send email\n2. Get email\n0. Exit\nChoose an option: ') 
    if n==1:
      send_mail(user,server)
    elif n==2:
      get_mail(mail)
    elif n==0: 
      server.quit()
      mail.logout()
  return



if __name__ == '__main__':
  main()
