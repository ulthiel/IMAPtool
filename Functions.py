#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from tqdm import tqdm
import mailbox

################################################################################
#Returns array with the mailbox names
def GetMailboxes(M):
  return [ m.replace("(\\HasNoChildren) \"/\" ", "").replace("(\\NoInferiors) \"/\" ", "").replace("\"", "") for m in M.list()[1] ]

################################################################################
#Returns number of messages in mailbox
def GetNumberOfMessages(M, mailbox):
  M.select(mailbox, readonly=True)
  typ, messages = M.search(None, 'ALL')
  messageIDs = str(messages[0]).split(" ")
  numMessages = len(messageIDs)
  return numMessages

################################################################################
#Backup mailbox
def BackupMailbox(M, box):
  M.select(box, readonly=True)
  typ, messages = M.search(None, 'ALL')
  messageIDs = str(messages[0]).split(" ")
  numMessages = len(messageIDs)
  mbox = mailbox.mbox(box+"_backup.mbox")
  for i in tqdm(range(0,len(messageIDs))):
    id = messageIDs[i]
    typ, msg = M.fetch(id, '(RFC822)')
    msg = msg[0][1]
    mbox.add(msg)
  mbox.close()
