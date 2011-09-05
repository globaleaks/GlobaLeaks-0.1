#import modules to work with MIME messages
from gluon.tools import MIMEMultipart, MIMEText, MIMEBase, Encoders
import smtplib

class MultiPart_Mail(object):
    def __init__(self, s):

    """Helper to create MIME message
     Arguments:
        sender = email address of sender (string). Required
        recipients = email address(es) of recipient(s). List. Required.
                examples: ["name <someone@host.com>"] 
                or if multiple 
                ["name1 <name1@host1.com>, name2 <name2@host2.net>"]
                or 
                ["person@host.org, person@host.info"]
        subject = subject for message. String. Required
        message_text = body of message in plain text. String. Required
        message_html = body of message in html. String. Optional
        attachments = list of tuples representing attachments with each 
                tuple having 2 elements - a filename & the file's contents. Optional. 
                example: [('image1.jpg',file_io),('file2.pdf',file_contents)]
                if the filename ends in an image extension (jpg, jpeg, png, gif, bmp) 
                it will be attached as an embedded image
                and you may refer to it in the message_html by 
                <img src="cid:filename"> where filename is the first element in
                the tuple.
                DO NOT include spaces in the filename or it won't appear as an 
                embedded image in your html email!
                for all other file types, the file will be attached as octet-stream 
                and be known by the filename passed as the first element in tuple
        cc = email address(es) of people to send message to via Carbon Copy. 
               String. Optional
        bcc = email address(es) of people to send message to via Blind Carbon 
                 Copy. String. Optional
        reply_to = email address for replies to be send to. String. Optional
    """
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
            if self.settings.email_server == 'gae':
                from google.appengine.api import mail
                #untested on GAE, but in theory should work
                #http://code.google.com/appengine/docs/python/mail/emailmessagefields.html
                mail.send_mail(sender=self.settings.email_sender, to=to,
                               subject=subject, body=message_text, html=message_html, attachments=attachments, cc = cc,
                               bcc = bcc, reply_to = reply_to)
            else:
                msg = self.buildMIME(sender = self.settings.email_sender, 
                    recipients = to, subject = subject, 
                    message_text = message_text, message_html = message_html,
                    attachments = attachments, 
                    cc = cc, bcc = bcc, reply_to = reply_to)
                print 'message'+msg.as_string()

                #Build MIME body
                (host, port) = self.settings.email_server.split(':')
                server = smtplib.SMTP(host, port)
                if self.settings.email_login:
                    server.ehlo()
                    if self.settings.use_tls:
                        server.starttls()
                    server.ehlo()
                    (username, password) = self.settings.email_login.split(':')
                    server.login(username, password)
                server.sendmail(self.settings.email_sender, to, msg.as_string())
                server.quit()
        except Exception, e:
            return False
        return True

