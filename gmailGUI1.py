#!/usr/bin/python2.7

import pygtk
pygtk.require('2.0')
import gtk
import time
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

att_filelist=[]

class GUIAPI:
  
  def get_login(self, widget, user_entry, pass_entry, window):
    user = user_entry.get_text()
    passw = pass_entry.get_text()
    window.destroy()
    login(user, passw)
  
  def __init__(self):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_size_request(300, 100)
    window.set_title('Gmail API - 1.1')
    window.connect('delete_event', lambda w,e : gtk.main_quit())

    vbox = gtk.VBox(False, 0)
    window.add(vbox)
    vbox.show()
    
    user_entry = gtk.Entry()
    user_entry.set_max_length(30)
    user_entry.set_text('Username')
    vbox.pack_start(user_entry, False, False, 0)
    user_entry.show()
    
    pass_entry = gtk.Entry()
    pass_entry.set_max_length(30)
    pass_entry.set_visibility(False)
    pass_entry.set_text('password')
    vbox.pack_start(pass_entry, False, False, 0)
    pass_entry.show()
    
    button = gtk.Button('Sign In')
    button.connect('clicked', self.get_login, user_entry, pass_entry, window)
    vbox.pack_start(button, False, False, 3)
    button.set_flags(gtk.CAN_DEFAULT)
    button.grab_default()
    button.show()
    
    window.show()
    
class MainWindow:
  def sendmail(self, widget, user, server, window):
    window.destroy()
    send_mail(user, server)
    
    
  def __init__(self, user, server, mail):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_size_request(800, 600)
    window.set_title('Gmail API - 1.1')
    window.connect('delete_event', lambda w,e : gtk.main_quit())

    
    vbox = gtk.VBox(False, 2)
    vbox.set_size_request(800,600)
    
    hbox = gtk.HBox(False, 2)
    hbox.set_size_request(800,50)
    
    vbox.pack_start(hbox, False, False, 2)    
    
    vpaned = gtk.VPaned()
    vbox.add(vpaned)
    
    label = gtk.Label(user)
    vpaned.add1(label)
    label.show()
    
    panedbox = gtk.HBox(False, 2)
    vpaned.add2(panedbox)
    panedbox.show()

    button = gtk.ToggleButton('Send Mail')
    button.connect('toggled', self.sendmail, user, server, window)
    button.set_size_request(100,30)
    hbox.pack_start(button, False, False, 2)
    button.show()
    
    button = gtk.ToggleButton('Recieve Mail')
    button.set_size_request(100,30)
#    button.connect('toggled', self.callback, 'toggle button 2')
    hbox.pack_start(button, False, False, 2)
    button.show()
    
    button = gtk.Button('Quit')
    button.set_size_request(100,50)  
    button.connect('clicked', lambda wid: gtk.main_quit())
    hbox.pack_end(button, False, False, 2)
    button.show()        
    
    window.add(vbox)
    
    vpaned.show()
    vbox.show()
    hbox.show()    
    window.show()

class PanedWindow:
  def sendmail(self, widget, user, server, window):
    window.destroy()
    send_mail(user, server)
  
  def mailcontent(self, widget, fromaddr_entry, to_entry, sub_entry, textview, filelist, window, user, server):
    fromaddr = fromaddr_entry.get_text()
    to = to_entry.get_text()
    sub = sub_entry.get_text()

    textbuffer = textview.get_buffer()
    startiter = textbuffer.get_start_iter()
    enditer = textbuffer.get_end_iter()
    body = textbuffer.get_text(startiter, enditer)

    window.destroy()
    sendthemail(user, server, fromaddr, to, sub, body, filelist)
    gtk.main_quit()   
       
    
  def select_file(self, widget, data = None):
    self.filew = gtk.FileSelection('Attach file')
    self.filew.ok_button.connect('clicked', self.file_ok_sel)
    self.filew.cancel_button.connect("clicked", lambda w: self.filew.destroy())
    self.filew.set_filename('Attach File')
    self.filew.show()
    
  def file_ok_sel(self, w):
    print "%s" % self.filew.get_filename()
    att_filelist.append(self.filew.get_filename())
    print att_filelist
    # append to a list
    self.filew.destroy()
    
  def __init__(self, user, server):
    att_filelist = []
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_size_request(800, 600)
    window.set_title('Gmail API - 1.1')
    window.connect('delete_event', lambda w,e : gtk.main_quit())

    
    vbox = gtk.VBox(False, 2)
    vbox.set_size_request(800,600)
    
    hbox = gtk.HBox(False, 2)
    hbox.set_size_request(800,50)
    
    vbox.pack_start(hbox, False, False, 2)
    vbox.show()    
    
    vpaned = gtk.VPaned()
    vbox.add(vpaned)
    
    label = gtk.Label(user)
    vpaned.add1(label)
    label.show()
    
    panedbox = gtk.HBox(False, 2)
    vpaned.add2(panedbox)
    panedbox.show()

    button = gtk.ToggleButton('Send Mail')
    button.connect('toggled', self.sendmail, user, server, window)
    button.set_size_request(100,30)
    hbox.pack_start(button, False, False, 2)
    button.show()
    
    button = gtk.ToggleButton('Recieve Mail')
    button.set_size_request(100,30)
#    button.connect('toggled', self.callback, 'toggle button 2')
    hbox.pack_start(button, False, False, 2)
    button.show()
    
    button = gtk.Button('Quit')
    button.set_size_request(100,50)  
    button.connect('clicked', lambda wid: gtk.main_quit())
    hbox.pack_end(button, False, False, 2)
    button.show()        
    
    window.add(vbox)
    
    pvbox = gtk.VBox(False, 0)
    panedbox.add(pvbox)
    pvbox.show()
    
    fromaddr_entry = gtk.Entry()
    fromaddr_entry.set_max_length(30)
    fromaddr_entry.set_text('From')
    pvbox.pack_start(fromaddr_entry, False, False, 0)
    fromaddr_entry.show()
    
    to_entry = gtk.Entry()
    to_entry.set_text('To: ')
    pvbox.pack_start(to_entry, False, False, 0)
    to_entry.show()
    
    sub_entry = gtk.Entry()
    sub_entry.set_max_length(30)
    sub_entry.set_text('Subject')
    pvbox.pack_start(sub_entry, False, False, 0)
    sub_entry.show()
    
    att_file_box = gtk.EventBox()
    att_file_box.set_size_request(30,20)
    pvbox.pack_start(att_file_box,False, False, 2)
    att_file_box.show()
    
    att_file_label = gtk.Label('Attach a file')
    att_file_box.add(att_file_label)
    att_file_label.show()
    
    att_file_label.set_size_request(10,20)
    att_file_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    att_file_box.connect("button_press_event", self.select_file)
    
    att_file_box.realize()
    att_file_box.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

        # Set background color to green
    att_file_box.modify_bg(gtk.STATE_NORMAL, att_file_box.get_colormap().alloc_color("orange"))
    
    sw = gtk.ScrolledWindow()
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    textview = gtk.TextView()
    textbuffer = textview.get_buffer()
    sw.add(textview)
    sw.show()
    textview.show()

    pvbox.pack_start(sw)
    textbuffer.set_text('')
    
    send_button = gtk.Button('send')
    send_button.set_size_request(400,30)
    send_button.connect('clicked', self.mailcontent, fromaddr_entry, to_entry, sub_entry, textview, att_filelist, window, user, server)
    pvbox.pack_end(send_button, False, False, 0)
    send_button.show()
    
    vpaned.show()
    pvbox.show()
    hbox.show()    
    window.show()

def send_mail(user, server):
  panedwindow = PanedWindow(user, server)
    
def sendthemail(user, server, fromaddr, to, sub, body, filelist):
  
  msg = email.MIMEMultipart.MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = to
  msg['Subject'] = sub
  tolist = to.split()  
  msg.attach(MIMEText(body))
  msg.attach(MIMEText('\nsent via python', 'plain'))
  print att_filelist
  for i in range(len(att_filelist)):
    msg = attach_files(msg, att_filelist[i]) 
  server.sendmail(user,tolist,msg.as_string())
  print 'sent'
  
  return
  
def attach_files(msg, filename):
  
  ctype, encoding = mimetypes.guess_type(filename)
  
  if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
    
  maintype, subtype = ctype.split('/', 1)
  f = open(filename, 'rb')      
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

def login(user, passw):   
  smtp_host = 'smtp.gmail.com'
  smtp_port = 587
  server = smtplib.SMTP()
  print 'server created'
  server.connect(smtp_host,smtp_port)
  server.ehlo()
  server.starttls()
  server.login(user,passw)
  
  imap_host = 'imap.gmail.com'
  mail = imaplib.IMAP4_SSL(imap_host)
  mail.login(user,passw)
  
  main_window = MainWindow(user, server, mail)
  
def main():
  win = GUIAPI()
  gtk.main()

if __name__ == '__main__':
  main()
