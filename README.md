chembl_clippy
=============

### What is Clippy?
Clippy is a simple desktop application that renders chemical structures using different formats as input.
The key thing is that the app reads the input directly from your clipboard (hence the name clippy) rather than a file.
Once you have a rendered structure, you can export it in different formats (via the clipboard again).

[![Downloads](https://pypip.in/v/chembl_clippy/badge.png)](https://pypi.python.org/pypi/epyper)
[![Number of PyPI downloads](https://pypip.in/d/chembl_clippy/badge.png)](https://crate.io/packages/epyper/)

### Why should one prefer it to other free viewers?
Apart from being Open Source and fully configurable, Clippy has some features currently missing from other viewer, such as the ChEMBL ID, name and InChIKey look-ups, as well as image and name conversions.  
Furthermore, the clipboard interface makes Clippy really convenient when one just wants to quickly check a structure. 

Here's a list of input formats that are read from clipboard and rendered in Clippy:
* ChEMBL IDs (via ChEMBL look-up)
* SMILES (via RDKit)
* InChI Strings (via RDKit)
* InChI Keys (via ChEMBL look-up)
* Nomenclature (via OPSIN)
* Images (via OSRA)

### Technical notes and dependencies
The application was written in Python using wxPython and is natively cross-platform. It has been tested on Mac Mountain Lion, Windows XP and Ubuntu 12.04 machines.
Clippy uses web services calls mainly to mnowotka's [Beaker server](https://github.com/mnowotka/chembl_beaker).
Therefore, you'll need a running instance of Beaker in your network.
Clipper comes also packaged for MacOS. As a result, the packaged version doesn't have any other dependencies whatsoever (apart from a network connection and an Apple machine).

### Installation
#### MacOS
#### Linux
The best way to install clippy on Linux is to use `PIP`:

    pip install chembl_clippy
    
Before this, please make sure you have `wxPython` installed in your system, you can check it by opening python intepreter and typing:

    import wx
    
If this passes without any problems you can install clippy via `PIP`. If not install `wxPython`:

    sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n libwxgtk2.8-dev libgtk2.0-dev

#### Windows

Instuctions for Linux are valid but to install `wxPython` you have it download from here:
http://www.wxpython.org/download.php
