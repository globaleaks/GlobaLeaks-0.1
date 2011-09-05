#import modules to work with MIME messages
from gluon.tools import MIMEMultipart, MIMEText, MIMEBase, Encoders
import smtplib

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
                #print 'message'+msg.as_string()

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

class MessageContent():
    def txt(self, context):
        return """Esteemed %(name)s,

This is an E-Mail message to notify you that someone has selected you as a valuable recipient of WhistleBlowing material in the form of a Globaleaks TULIP. This message has been created by the GlobaLeaks Node %(sitename)s.

This TULIP has been sent to you by an anonymous whistleblower. She/He would like it for you to pay special attention to the information and material contained therein. Please consider that whistleblowers often expose themselves to high personal risks in order to protect the public good. Therefore the material that they provide with this TULIP should be considered of high importance.

You can download the material from the following URL:

http://%(site)s/tulip/%(tulip_url)s

Please do not forward or share this e-mail: each TULIP has a limited number of downloads and access before being destroyed forever, nobody (even the node administrator) can recover and expired or dead TULIP.

--------------------------------------------------
GENERAL INFO
--------------------------------------------------

1. What is Globaleaks?

GlobaLeaks is the first Open Source Whistleblowing Framework. It empowers anyone to easily setup and maintain their own Whistleblowing platform. It is also a collection of what are the best practices for people receiveiving and submitting material. GlobaLeaks works in all environments: media, activism, corporations, public agencies.

2. Is GlobaLeaks sending me this Mail?

No, this mail has been sent to you by the Node called %(sitename)s. They are running the GlobaLeaks Platform, but are not directly tied to the GlobaLeaks organization. GlobaLeaks (http://www.globaleaks.org) will never be directly affiliated with any real world WhistleBlowing sites, GlobaLeaks will only provide software and technical support.

3. Why am I receiving this?

You're receiving this communication because an anonymous whistleblower has chosen you as a trustworthy contact for releasing confidential and/or important information that could be of utmost importance.

4. How can I stop receiving future TULIPs?

You can permanently unsibscrive from this GLobaLeaks Node by clicking on the following leak:
http://%(site)s/target/subscribe/%(tulip_url)s

If in any future you want to be re-enlisted you can add yourself again using this link:
http://%(site)s/target/unsubscribe/%(tulip_url)s


For any other inquire please refer to %(sitename)s to the GlobaLeaks website at http://globaleaks.org

Take Care,
A Random GlobaLeaks Node""" % context



    def html(self, context):
        return """<!html>
<html><head><title>You have received a TULIP from %(sitename)s - %(name)s</title>
</head>
<body>

<p>Esteemed %(name)s,</p>

<p>This is an E-Mail message to notify you that someone has selected you as a valuable recipient of WhistleBlowing material in the form of a Globaleaks TULIP. This message has been created by the GlobaLeaks Node %(sitename)s.</p>

<p>This TULIP has been sent to you by an anonymous whistleblower. She/He would like it for you to pay special attention to the information and material contained therein. Please consider that whistleblowers often expose themselves to high personal risks in order to protect the public good. Therefore the material that they provide with this TULIP should be considered of high importance.</p>

<p>You can download the material from the following URL:</p>

<p><a href="http://%(site)s/tulip/%(tulip_url)s">http://%(site)s/tulip/%(tulip_url)s"</a></p>

<p>Please do not forward or share this e-mail: each TULIP has a limited number of downloads and access before being destroyed forever, nobody (even the node administrator) can recover and expired or dead TULIP.</p>

<h2>GENERAL INFO</h2>

<ol>
<li><h3>What is Globaleaks?</h3>

<p>GlobaLeaks is the first Open Source Whistleblowing Framework. It empowers anyone to easily setup and maintain their own Whistleblowing platform. It is also a collection of what are the best practices for people receiveiving and submitting material. GlobaLeaks works in all environments: media, activism, corporations, public agencies.</p>
</li>

<li><h3>Is GlobaLeaks sending me this Mail?</h3>

<p>No, this mail has been sent to you by the Node called %(sitename)s. They are running the GlobaLeaks Platform, but are not directly tied to the GlobaLeaks organization. GlobaLeaks (http://www.globaleaks.org) will never be directly affiliated with any real world WhistleBlowing sites, GlobaLeaks will only provide software and technical support.</p>
</li>

<li><h3>Why am I receiving this?</h3>

<p>You're receiving this communication because an anonymous whistleblower has chosen you as a trustworthy contact for releasing confidential and/or important information that could be of utmost importance.</p>
</li>

<li><h3>How can I stop receiving future TULIPs?</h3>
<p>
You can permanently unsubscribe from this GLobaLeaks Node by clicking on the following leak:
<a href="http://%(site)s/target/unsubscribe/%(tulip_url)s">http://%(site)s/target/unsubscribe/%(tulip_url)s</a>
</p>
<p>
If in any future you want to be re-enlisted you can add yourself again using this link:
<a href="http://%(site)s/target/subscribe/%(tulip_url)s">http://%(site)s/target/subscribe/%(tulip_url)s"/a>
</p>
</li>
</ol>

<p>
For any other inquire please refer to %(sitename)s to the GlobaLeaks website at http://globaleaks.org
</p>

<p>Take Care,<br/>
A Random GlobaLeaks Node</p>


""" % context





