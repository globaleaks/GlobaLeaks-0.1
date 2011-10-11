# General configuration
The first place where you should look for customization is the GlobaLeaks config file.
It is located in globaleaks/applications/globaleaks/models/gleaks.cfg.
From here you are able to set the following parameters:

    [global]
    title = <the title of your site>
    subtitle = <subtitle>
    author = <author>
    description = <description of site>
    disclaimer = <submission page disclaimer>
    layout_theme = Default
    author_email = <email address of site maintainer>

    # must be changed to random string
    security_key = CHANGEMEPLEASETOARANDOMSTRINGOFCHARSNUMBERS
    email_server =
    email_sender = node@globaleaks.org
    email_login =
    login_method =
    login_config =

    [tulip]
    max_access = 1
    expire = 2

    [logging]
    server = True
    client = True
    logfile = /tmp/globaleaks.log

    [database]
    uri = sqlite://storage.sqlite

* To add custom FORM elements you should edit the XML file
    * globaleaks/applications/globaleaks/models/extrafields.xml

An example of how custom form elements look like is:
    <fields>
        <field>
            <name>extratext</name>
            <label>Text</label>
            <description>This is a text field</description>
            <type>string</type>
        </field>
        <field>
            <name>textarea</name>
            <label>Text Area</label>
            <description>This is a text area</description>
            <type>text</type>
        </field>
        <field>
            <name>enable</name>
            <label>Enable something</label>
            <description>Enable the thing by checking the box</description>
            <type>boolean</type>
        </field>
        <field>
            <name>date</name>
            <label>Date</label>
            <description>Enter a date realted to your submission</description>
            <type>date</type>
        </field>
        <field>
            <name>menu</name>
            <label>Menu</label>
            <description>Select something from the drop down menu</description>
            <type>list</type>
            <list>
                <el>Element1</el>
                <el>Element2</el>
                <el>Element3</el>
            </list>
        </field>
    </fields>

# Presentation
For customizing the look of your site you should be looking at globaleaks/applications/globaleaks/views/.

* layout.html - Contains the main layout included in every page

    * For customizing the logo in every page look for "header" and replace the image with your own logo.

Inside globaleaks/applications/globaleaks/static you will find all the .css files.

* base.css - the main .css file


