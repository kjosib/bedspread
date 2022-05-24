I/O with Files:
===================

This entire section is going to have to wait until there is clear support for data structuring.

Files break down across a few dimensions.

Some are meant to be interpreted as text, such as ASCII or Unicode.
Others are meant to be binary, although some sections may be text.

Some are divided into fixed-width records of some kind (or have sections that work like this).
Some have a sequential-access record structure (such as CSV files).
Some have a complex, irregular record structure (such as ZIP and graphics files).

Some files are best understood as an unstructured stream of bytes or characters.
This is appropriate when treating files generically, in a manner insensitive to the semantics of their content.
Other files are best accessed through an intermediary layer. This is appropriate for database files.

Each of these major cases should ideally have proper support in a complete system.
But we're building atop Posix, which really only considers *"seekable stream of bytes"* to be a thing.
In any event, any nice layers atop Posix *can* be done as a library.
The key thing in this context is to make sure that the common things are easy and the
uncommon things are still no more difficult than they strictly need to be.

Structured
-----------------

Sequential Structured Text
...........................

Your CSV-type files go here.
Presumably we plug into the existing CSV readers and writers,
because they're mostly good enough.

Block-Structured Random-Access
...............................

This might be perfect for an animals-type game, but not too much else.
In a modern world, the way to store random-access data is with either xDB or SQLite.

In any event, given a base-offset and a record size,
we can create a cursor which can then be told to read or write any given record at random,
without overrunning the allotted record size.

Free-Form
-----------------

Sequential Unstructured Text
.............................

This is basically the same as the structured case, except with the application responsible for analyzing
the content of the file. Typical examples might be arcane configuration files and legacy program code.
You can rely on a codec to read and write these files, but that's about all the help you'll normally get.

Binary Streaming Random-Access
..............................

The wild west: Any data anywhere. But for some applications, this turns out to be exactly what you need.

Non-Posix Concepts
-------------------

Chiefly, I would get rid of the ``seek()`` and ``tell()``interface, or change them considerably.

