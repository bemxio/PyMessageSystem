# PyMessageSystem

I'm new to this Github thing, sorry if something is wrong.

PyMessageSystem is self-explanatory. 
It's a system that works like e-mail and it has it's own database stored online (FTP server).
~~To start & test it on my database, just run the **emailsys.exe** file.~~ i dont host the database anymore, sorry

If you wanna start your own database, upload a **database.json** file to your FTP server, replace the **YOUR_FTP_ADDRESS**, **YOUR_FTP_USERNAME** and **YOUR_FTP_PASSWORD** with your own in **emailsys.py** file.

**note:** yes, i know that code is very bad, its my first project that i made, i improved a lot by now

# `debug` command list
`debug database` - displays you the database in JSON format

`debug user <id>` - display data of an user

`debug delete <id>` - deletes the user

`debug delete database l|all` - reset database locally or reset database locally & online
