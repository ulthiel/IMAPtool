#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from tqdm import tqdm
import mailbox
import hashlib
import sys

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
  try:
    logFile = open(box+"_backup.log", "r")
    start = int(logFile.readline())
    logFile.close()
  except:
    start = -1
  mbox = mailbox.mbox(box+"_backup.mbox")
  for i in tqdm(range(0,len(messageIDs))):
    if i <= start:
      continue
    id = messageIDs[i]
    typ, msg = M.fetch(id, '(RFC822)')
    msg = msg[0][1]
    mbox.add(msg)
    mbox.flush()
    logFile = open(box+"_backup.log", "w")
    logFile.write(str(i))
    logFile.close()
  mbox.close()

################################################################################
#Delete duplicates
def DeleteDuplicates(M, box):
  M.select(box, readonly=True)
  typ, messages = M.search(None, 'ALL')
  messageIDs = str(messages[0]).split(" ")
  numMessages = len(messageIDs)

  hashes = []
  try:
    for line in open(box+"_hashes.log"):
      hashes.append(line)
  except:
    None

  dupes = []
  try:
    for line in open(box+"_dupes.log"):
      dupes.append(line)
  except:
    None

  for i in range(len(hashes),len(messageIDs)):
    id = messageIDs[i]
    typ, msg = M.fetch(id, '(RFC822)')

    hash = hashlib.sha512(msg[0][1]).hexdigest()
    hashFile = open(box+"_hashes.log", "a")
    hashFile.write(hash+"\n")
    hashFile.close()
    if hash in hashes:
      dupes.append(id)
      dupeFile = open(box+"_dupes.log", "a")
      dupeFile.write(str(id)+"\n")
      dupeFile.close()

    hashes.append(hash)

    sys.stdout.write('\r' + "Searching for duplicates in "+box+": " + str(id) + "/" + str(numMessages) + ", " + str(len(dupes)) + " duplicates found")
    sys.stdout.flush()

  print "Deleting "+str(len(dupes))+" duplicates"

  #flag dupes as deleted
  for i in tqdm(range(0,len(dupes))):
    M.store(int(dupes[i]], "+FLAGS", "\\Deleted")

  #expunge
  M.expunge()
