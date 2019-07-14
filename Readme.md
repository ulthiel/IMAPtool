# IMAPtool

A little Python script to backup and delete duplicate messages in IMAP mailboxes.

**Note:** This is an experimental software. Use at your own risk.

<!--
## Motivation
I noticed some strange issues with Apple Mail when trying to move (thousands of) messages from one account to another. If I tried to move more than a few hundred messages at once, the first time simply nothing happened – the mails I wanted to move still showed up in the old mailbox; then I tried again and this time it indeed started moving but it took ages and sometimes it looked like nothing is happening anymore (the status/progress indicator in Apple Mail is somehow useless). I only managed to move my messages by moving just a few hundred each time and sometimes I had to do this several times as they just didn't move. After a long time it was finally done. But then I noticed that my quota was almost exceeded, which was strange. After closer inspection I found that although Apple Mail shows 20,000 messages in my mailbox, the account information (by clicking on *Get Account Info*) shows more than *4 times* the number of messages (and thus 4 times the disk space). I suspected that the moving process probably created many duplicate messages which are invisible in Apple Mail. This is insane. I've thus written this tool to delete all these duplicates and repair my mailbox as this cannot be done in Apple Mail. Very bizarre. Anyways, it was a good reason to learn IMAP handling in Python.
-->

## Usage
Edit your account information in Account.py. Set ssl=True if you use an
SSL connection (this should be standard). Then run ```python IMAPtool.py```. You may need to install the Python module *tqdm* (which is used for displaying progress bars) by running ```pip install tqdm```.

If you need IMAP access to an iCloud account, you first need to set up an *app-specific password* in your [account settings](https://appleid.apple.com/account/manage).
