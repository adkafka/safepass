# SafePass
A simple, safe password storage system. safepass works by keeping an encrypted password safe at the location specified in your configuration file. The safe maps passwords at the 'domain' level, allowing multiple passwords per 'domain', and simple search. All interaction with passwords is via stdin or the clipboard. When a password is requested from the safe, it is copied to the clipboard for 60 seconds, after which it is over written.

The configuration file is stored in ~/.safepass.

## Instalation
### Dependencies
You need a modern gpg tool installed on the machine (`brew install gpg`). 

Additionally, you will need python2.7 with the gnupg python wrapper (`pip install python-gnupg`).

If there are any issues, please let us know so we can fix them!

This was developed and tested on a Mac. This can be easily ported to linux by modifying the ClibBoard.py file to work with your system's clipboard manager.

## Getting started
After installation, you need to 'initialize' the system, with `$ safepass init`. This will create the configuration file, if it was not previously present. The default path to store the encrypted passwords is ~/.safepassstore, but can be changed to anywhere on your system. If you use Google Drive, DropBox, or a simliar tool, storing the passwords on the cloud is as simple as setting your "pass\_store\_path" to inside the relevant folder.

Simply execute `$ safepass` to get the help page.

### Examples:
```
$ safepass add Google "my personal google account"
$ safepass add Google "my work google account"
$ safepass add Facebook
$ safepass ls
$ safepass ls Google
$ safepass search "work"
$ safepass get Facebook
$ safepass edit Facebook note "My current facebook account"
...
```

### Good reference projects (Similar password managers):

[pass](https://www.passwordstore.org/) - Cons: it stores the passwords in a series of files (directories), giving away that a user has an account with a given site - Pros: ``pass -c`` is really cool, we should steal that. Their design is very solid and well though through. We should steal most of it...

[KeePass](https://en.wikipedia.org/wiki/KeePass) - Mainly windows based...

LessPass is terrible, it just uses a master password and the website name to generate a password.
 No data storage. [See this article for an explanation why deterministic PM's are terrible](https://tonyarcieri.com/4-fatal-flaws-in-deterministic-password-managers)
