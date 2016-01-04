#!/usr/bin/env python3

import sys
import html
import argparse
from pygmail2.Pygmail import mo

emails = ["kindlychung.5d718c5@m.evernote.com", "kindlychung.mathstuff@blogger.com", "linda.leeuws001@yahoo.com", "kindlychung@gmail.com", "trigger@recipe.ifttt.com"]

parser = argparse.ArgumentParser(description="Send email to Evernote or Blogger")
parser.add_argument("--filename", "-f", help="File to send as email body")
parser.add_argument("--evernote", "-e", action="store_true", help="Send to evernote")
parser.add_argument("--blogger", "-b", action="store_true", help="Send to blogger")
parser.add_argument("--yahoo", "-y", action="store_true", help="Send to yahoo")
parser.add_argument("--gmail", "-g", action="store_true", help="Send to gmail")
parser.add_argument("--pre", "-p", action="store_true", help="Wrapp with a pre tag")
parser.add_argument("--stdin", "-s", action="store_true", help="Wrapp with a pre tag")
parser.add_argument("--attach", "-a", nargs="+", help="Files to attach")
parser.add_argument("--ifttt", "-i", action="store_true", help="Send to ifttt")
args = parser.parse_args()
print(args)

address_idx = []

if args.evernote:
    address_idx.append(0)
if args.blogger:
    address_idx.append(1)
if args.yahoo:
    address_idx.append(2)
if args.gmail:
    address_idx.append(3)
if args.ifttt:
    address_idx.append(4)
if len(address_idx) == 0:
    print("No addresses given, nothign to do...")
    exit(0)

address = [emails[i] for i in address_idx]


filecontent = ""

def pre_lines(filecontent):
    """
    Parse a string and wrap each line with a pre tag.
    Return the first line (as subject) and wrapped string (as content).
    """
    filecontent = html.escape(filecontent)
    filecontent = filecontent.split("\n")
    subject = filecontent[0]
    filecontent = "".join(["<pre>" + i + "</pre>" for i in filecontent])
    return (subject, filecontent)

if args.filename != None:
    with open(args.filename) as fh:
        filecontent_all = fh.read()
        subject, filecontent = pre_lines(filecontent_all)
    if args.pre:
        filecontent = filecontent_all
else:
    subject, filecontent = pre_lines(sys.stdin.read())

mo.sm(address, subject, filecontent, args.attach)

# s, c = pre_lines("what is a < b? \n what is a > b?")
# mo.sm("kindlychung@gmail.com", s, c)
