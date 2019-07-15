#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Ulrich Thiel, 2019

################################################################################
#Imports
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import getpass, imaplib
from lib import Functions
from Account import *
try:
  from Account_local import *
except:
  None

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
mailboxes = Functions.GetMailboxes(M)

################################################################################
#Mailbox selection dialog
print "Mailboxes:"
for i in range(0, len(mailboxes)):
  print " (" + str(i+1) + ") " + mailboxes[i] + " (" + str(Functions.GetNumberOfMessages(M, mailboxes[i])) + ")"
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
  Functions.BackupMailbox(M, mailbox)

elif action == 2:
  Functions.DeleteDuplicates(M, mailbox)

################################################################################
#Logout properly
M.logout()
sys.exit(0)


#Hack to call functions which are defined later in the code
#Leave this at the bottom
#From https://stackoverflow.com/questions/1590608/is-it-possible-to-forward-declare-a-function-in-python
if __name__=="__main__":
   main()
