# 🚩 Doctor Bye Bye - FortID CTF Writeup

**Category:** Web (SQL Injection)  
**Difficulty:** Medium  
**Author:** Pepega

## 📝 Challenge Description
> Dr. Bye Bye has retired from St. Codd's Hospital. The hospital insists that retired records can never be displayed. Can you recover Dr. Bye Bye's private farewell note anyway?

## 🔍 Initial Reconnaissance & Analysis
I was testing the `/api/on-call?sort=` endpoint because whatever parameter I gave it, it was inserted directly into the code.

At first, my idea was to perform something like a `UNION` attack to pull the hidden records. However, after some research (and a bit of prompting 😅), I learned that you cannot inject a `UNION` statement directly into an `ORDER BY` clause—which makes perfectly good sense when you think about SQL query structure.

Since we can't just append a new query, I searched for `ORDER BY` vulnerabilities and for SQL statements.

## 🐛 The Vulnerability
The core vulnerability is an **Order By (Boolean-Based Blind) SQL Injection**. 

Because we completely control the `ORDER BY` clause, we can inject a `CASE WHEN` statement. By making a conditional check (e.g., checking if the length of a string is greater than a specific number), we can force the database to return `0` or `1` for specific rows. This completely changes the sort order. 

If our injected condition is True, the application sorts 'Dr. Ada Pulse' to the top of the response. If it is False, 'Dr. Zoe Last' appears at the top instead. This gives us a reliable oracle to ask the database Yes/No questions.

## 💥 Exploitation
The exploitation happens in two phases:

1.  **Determine the Length of the flag:** We start with a `variable` (starting at 8 because we know the format of the flag) and ask the database if the length of the `farewell_note` is greater than this variable. We check the response text for "Dr. Ada Pulse" to know if the condition evaluated to true.
2.  **Extract the Flag:** Once we have the length, we extract a single character using `substr(farewell_note, position, 1)` and convert it to its decimal value using `unicode()`. We then brute-force the ASCII values from 32 to 127 until the response returns "Dr. Zoe Last", which confirms a match. 

Knowing the flag format is `FortID{...}`, the script offsets the extraction by 7 characters to skip the known prefix and directly grab the inner string.

### Exploit Script
Here is the automated Python solver for the challenge (I know that I could use a sort of some kind and make fewer requests, but it was 3 AM when I wrote the script and I thought it was easier to do it this way):
