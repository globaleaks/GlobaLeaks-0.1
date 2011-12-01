#import modules to work with MIME messages
from gluon.tools import MIMEMultipart, MIMEText, MIMEBase, Encoders
from gluon import *
from gluon.utils import logger
import smtplib
import os

from socksipy import socks

# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 9050)

# socks.wrapmodule(smtplib)

class MultiPart_Mail(object):
    def __init__(self, s):
        self.settings = s
    def buildMIME(self,
        sender,
        recipients,
        subject,
        message_text,
        message_html = None,
        attachments = None,
        cc = None,
        bcc = None,
        reply_to = None):
        #bases off of http://code.activestate.com/recipes/473810/

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart.MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = sender

        if not isinstance(recipients, list):
            #presumably only given a string representing a single email address
            #convert to single element list
            to = [recipients]
        msgRoot['To'] = ', '.join(recipients)

        if cc and isinstance(cc, list):
            cc = ', '.join(cc)
            msgRoot['CC'] = cc

        if bcc and isinstance(cc, list):
            bcc = ', '.join(bcc)
            msgRoot['BCC'] = bcc

        if reply_to:
            msgRoot['Reply-To'] = reply_to

        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart.MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        #text only version
        msgText = MIMEText.MIMEText(message_text)
        msgAlternative.attach(msgText)

        #html version of message
        if message_html:
            msgText = MIMEText.MIMEText(message_html, 'html')
            msgAlternative.attach(msgText)
        # We reference the image in the IMG SRC attribute by the ID we give it
        #below <img src="cid:content-id">

        #attach images to message
        #attachments are a list as in (['filename1',filecontents1], ['filename2',filecontents2])
        #where the filecontents are as provided by open(file_path, 'rb') or other method (retreived from DB?)
        if attachments:
            for attachment in attachments:
                if attachment[0].split('.')[-1] in ('jpg','jpeg','png','gif','bmp'):
                    #attachment's contents
                    msgImage = MIMEImage(attachment[1])

                    # Define the image's ID as referenced above
                    msgImage.add_header('Content-ID', '<'+attachment[0]+'>')
                    msgRoot.attach(msgImage)
                else:
                    #based on http://snippets.dzone.com/posts/show/2038
                    part = MIMEBase.MIMEBase('application', "octet-stream")
                    part.set_payload(attachment[1])
                    Encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="%s"' % attachment[0])
                    msgRoot.attach(part)
        #print msgRoot.as_string()
        return msgRoot

    def send(
        self,
        to = '', #list of email addresses - Required
        subject='None', #message's subject - Required
        message_text='None', #message body in plain text - Required
        message_html=None, #message body in html - Optional
        attachments=None, #list of truples [(filename, file_contents)] - Optional
        cc = None, #list of email addresses to CC message to
        bcc = None, #list of email addresses to BCC message to
        reply_to = None, #single email address to have replies send to
        ):
        """
        Sends an email. Returns True on success, False on failure.
        """        
        if not isinstance(to, list):
            to = [to]

        try:
            if self.settings.private.email_server == 'gae':
                from google.appengine.api import mail
                #untested on GAE, but in theory should work
                #http://code.google.com/appengine/docs/python/mail/emailmessagefields.html
                mail.send_mail(sender=self.settings.private.email_sender, to=to,
                               subject=subject, body=message_text, html=message_html, attachments=attachments, cc = cc,
                               bcc = bcc, reply_to = reply_to)
            else:

                msg = self.buildMIME(sender = self.settings.private.email_sender,
                    recipients = to, subject = subject,
                    message_text = message_text, message_html = message_html,
                    attachments = attachments,
                    cc = cc, bcc = bcc, reply_to = reply_to)
                #print 'message'+msg.as_string()
                #Build MIME body
                (host, port) = self.settings.mail.server.split(':')

                if self.settings.mail.ssl:                    
                    try:
                        server = smtplib.SMTP_SSL(host, port)
                    except:
                        # ERROR python <= 2.6
                        pass
                else:
                    server = smtplib.SMTP(host, port)

                if self.settings.mail.login:
                    try:
                        server.ehlo_or_helo_if_needed()
                    except SMTPHeloError:
                        logger.info("SMTP Helo Error in HELO")

                    if self.settings.mail.use_tls:
                        try:
                            server.starttls()
                        except SMTPHeloError:
                            logger.info("SMTP Helo Error in STARTTLS")
                        except SMTPException:
                            logger.info("Server does not support TLS")

                        except RuntimeError:
                            logger.info("Python version does not support TLS (<= 2.6?)")

                    try:
                        server.ehlo_or_helo_if_needed()
                    except SMTPHeloError:
                        logger.info("SMTP Helo Error in HELO")

                    (username, password) = self.settings.mail.login.split(':')
                    try:
                        server.login(username, password)
                    except SMTPHeloError:
                        logger.info("SMTP Helo Error in LOGIN")

                    except SMTPAuthenticationError:
                        logger.info("Invalid username/password combination")

                    except SMTPException:
                        logger.info("SMTP error in login")

                try:
                    server.sendmail(self.settings.private.email_sender, to, msg.as_string())
                    server.quit()

                except SMTPRecipientsRefused:
                    logger.info("All recipients were refused. Nobody got the mail.")

                except SMTPHeloError:
                    logger.info("The server didn't reply properly to the HELO greeting.")

                except SMTPSenderRefused:
                    logger.info("The server didn't accept the from_addr.")

                except SMTPDataError:
                    logger.info("The server replied with an unexpected error code (other than a refusal of a recipient).")
                                        
        except Exception, e:
            return False
        return True

    def make_txt(self, context, file):
        f = open(os.path.join(os.getcwd(), file))
        return f.read().strip() % context



    def make_html(self, context, file):
        f = open(os.path.join(os.getcwd(), file))
        return f.read().strip() % context
                                                        
                                                        
