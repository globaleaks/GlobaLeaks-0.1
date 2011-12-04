BD=`pwd`"/"
# Add GlobaLeaks user and groups
groupadd globaleaks
useradd -g globaleaks -s /bin/false -d $BD globaleaks
# Change the group of certain folders and files
chgrp globaleaks ${BD}
chgrp globaleaks ${BD}applications/
chgrp globaleaks ${BD}applications/globaleaks/
chgrp globaleaks ${BD}applications/globaleaks/uploads/
mkdir ${BD}applications/globaleaks/material/
chgrp globaleaks ${BD}applications/globaleaks/material/
chgrp globaleaks ${BD}applications/globaleaks/databases/
chgrp globaleaks ${BD}applications/globaleaks/errors/
mkdir ${BD}applications/globaleaks/cache/
chgrp globaleaks ${BD}applications/globaleaks/cache/
mkdir ${BD}applications/globaleaks/sessions/
chgrp globaleaks ${BD}applications/globaleaks/sessions/
touch ${BD}cron.master
chgrp globaleaks ${BD}cron.master
touch ${BD}parameters_8000.py
chgrp globaleaks ${BD}parameters_8000.py
touch ${BD}httpserver.pid
chgrp globaleaks ${BD}httpserver.pid
touch ${BD}info.globaleaks.log
chgrp globaleaks ${BD}info.globaleaks.log
touch ${BD}applications/globaleaks/all.css
touch ${BD}applications/globaleaks/all.js
chgrp globaleaks ${BD}applications/globaleaks/static
chgrp globaleaks ${BD}globaleaks.conf

# Change the permissions
chmod 771 ${BD}
chmod 771 ${BD}applications/
chmod 771 ${BD}applications/globaleaks/
chmod 771 ${BD}applications/globaleaks/static
chmod 770 ${BD}globaleaks.conf
chmod 770 ${BD}cron.master
chmod 770 ${BD}parameters_8000.py
chmod 770 ${BD}httpserver.pid
chmod 770 ${BD}info.globaleaks.log
chmod 770 ${BD}applications/globaleaks/uploads/
chmod 770 ${BD}applications/globaleaks/material/
chmod 770 ${BD}applications/globaleaks/errors/
chmod 770 ${BD}applications/globaleaks/databases/
chmod 770 ${BD}applications/globaleaks/cache/
chmod 770 ${BD}applications/globaleaks/sessions/

