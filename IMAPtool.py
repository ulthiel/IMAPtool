#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

################################################################################
#Imports
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import getpass, imaplib, hashlib
from Functions import *
from Account import *
from Account_local import *

################################################################################
#Open connection
print "Account: " + user
if ssl == True:
  M = imaplib.IMAP4_SSL(host=host,port=port)
else:
  M = imaplib.IMAP4(host=host,port=port)
M.login(user, password)

################################################################################
#Get mailboxes (returned in some weird format)
mailboxes = GetMailboxes(M)

################################################################################
#Mailbox selection dialog
print "Mailboxes:"
for i in range(0, len(mailboxes)):
  print " (" + str(i+1) + ") " + mailboxes[i] + " (" + str(GetNumberOfMessages(M, mailboxes[i])) + ")"
mailbox = int(raw_input("Select mailbox: "))
mailbox = mailboxes[mailbox-1]

################################################################################
#Action selection dialog
print "Actions:"
print "  (1) Backup"
print "  (2) Delete duplicates"
action = int(raw_input("Select action: "))

################################################################################
#Perform action
if action == 1:
  BackupMailbox(M, mailbox)

################################################################################
#Logout properly
M.logout()
sys.exit(0)



M.select(mailbox, readonly=True)
typ, messages = M.search(None, 'ALL')
messageIDs = str(messages[0]).split(" ")
numMessages = len(messageIDs)
hashes = []
dupes = []
try:
  for line in open(mailbox+".txt"):
    hashes.append(line)
except:
  None
hashFile = open(mailbox+".txt", "a")
dupeFile = open(mailbox+"_dupes.txt", "a")
for i in range(len(hashes),len(messageIDs)):
  id = messageIDs[i]
  typ, msg = M.fetch(id, '(RFC822)')
  hash = hashlib.sha512(msg[0][1]).hexdigest()
  if hash in hashes:
    dupes.append(id)
    dupeFile.write(str(id)+"\n")
  hashes.append(hash)
  hashFile.write(hash+"\n")
  sys.stdout.write('\r' + "Searching for duplicates in "+mailbox+": " + str(id) + "/" + str(numMessages) + ", " + str(len(dupes)) + " duplicates found")
  sys.stdout.flush()

print ""

hashFile.close()
dupeFile.close()
M.logout()


#Hack to call functions which are defined later in the code
#Leave this at the bottom
#From https://stackoverflow.com/questions/1590608/is-it-possible-to-forward-declare-a-function-in-python
if __name__=="__main__":
   main()
