#! /usr/bin/python
# -*- coding: utf-8 -*-

# New current version: Purely cross-platform version - Calls to Beaker.

__author__ = 'georgep'

import wx

import requests
import base64
import urllib2
import traceback
import StringIO

import platform

from settings import Settings

IMG_SIZE = 500

SIZES = {'Windows': (IMG_SIZE+5, IMG_SIZE+75), 'Darwin': (IMG_SIZE, IMG_SIZE+40), 'Linux': (IMG_SIZE, IMG_SIZE+40)}
EVENTS = {'Windows': 'wx.EVT_LEFT_DOWN', 'Darwin': 'wx.EVT_ENTER_WINDOW', 'Linux': 'wx.EVT_LEFT_DOWN'}

SYS = platform.system()


def id2smi(chemblid):
    """
    Use ChEMBL web service to convert an ChEMBL ID to smiles.
    Return None if it fails.
    """
    smi = None
    WS_URL = 'https://www.ebi.ac.uk/chemblws/compounds/{}.json'
    r = requests.get(WS_URL.format(chemblid), verify=False)  # SSL caused problem with pyinstaller.
    if r.ok:
        smi = r.json()['compound']['smiles']
    return smi


def inchikey2smi(inchikey):
    smi = None
    WS_URL = 'https://www.ebi.ac.uk/chemblws/compounds/stdinchikey/{}.json'
    r = requests.get(WS_URL.format(inchikey), verify=False)  # SSL caused problem with pyinstaller.
    if r.ok:
        smi = r.json()['compound']['smiles']
    return smi

def name2smi(name):
    smi = None
    WS_URL = 'http://opsin.ch.cam.ac.uk/opsin/{}.smi'
    r = requests.get(WS_URL.format(name))
    if r.ok:
        smi = r.text
    return smi


def smi2ctab(smi):
    ctab = None
    try:
        WS_URL = Settings.Instance().getBaseURL() + '/smiles2ctab/{}'
        ctab = urllib2.urlopen(WS_URL.format(base64.b64encode(smi))).read()
    except:
        traceback.print_exc()
        pass
    return ctab


def ctab2smi(ctab):
    cansmi = None
    WS_URL = Settings.Instance().getBaseURL() + '/ctab2smiles/{}'
    try:
        cansmi = urllib2.urlopen(WS_URL.format(base64.b64encode(ctab))).read()
    except:
        traceback.print_exc()
        pass
    return cansmi


def ctab2image(ctab, name):
    """Try to convert a ctab to an image. None otherwise"""
    if name.upper().startswith('CHEMBL'):
        legend = name.upper()
    else:
        legend = name
    WS_URL = Settings.Instance().getBaseURL() + '/ctab2image/{0}/{1}'
    try:
        img = urllib2.urlopen(WS_URL.format(base64.b64encode(ctab), IMG_SIZE)).read()
    except:
        raise
    return img


def string2ctab(s):
    """Convert a short string (no spaces) to smiles or None otherwise"""
    ctab = None
    WS_URL = Settings.Instance().getBaseURL() + '/smiles2ctab/{}'
    if (len(s) <= 250) and (" " not in s) and ("\n" not in s):
        try:
            ctab = urllib2.urlopen(WS_URL.format(base64.b64encode(s))).read()
        except:
            raise
    return ctab


def ctab2inchi(ctab):
    inchi = None
    WS_URL = Settings.Instance().getBaseURL() + '/ctab2inchi/{}'
    try:
        inchi = urllib2.urlopen(WS_URL.format(base64.b64encode(ctab))).read()
    except:
        traceback.print_exc()
        pass
    return inchi


def inchi2ctab(inchi):
    ctab = None
    WS_URL = Settings.Instance().getBaseURL() + '/inchi2ctab/{}'
    try:
        ctab = urllib2.urlopen(WS_URL.format(base64.b64encode(inchi))).read()
    except:
        traceback.print_exc()
        pass
    return ctab


def inchi2inchiKey(inchi):
    inchikey = None
    WS_URL = Settings.Instance().getBaseURL() + '/inchi2inchiKey/{}'
    try:
        inchikey = urllib2.urlopen(WS_URL.format(base64.b64encode(inchi))).read()
    except:
        traceback.print_exc()
        pass
    return inchikey


def image2ctab(img):
    """Try with this image:
        http://3.bp.blogspot.com/_7xzZi5UF2yw/TQTsjb9VSFI/AAAAAAAAAC8/HWQsOkiUmAQ/s200/Aspirin+picture.png
        Uses POST"""
    ctab = None
    try:
        sio = StringIO.StringIO()
        img.SaveStream(sio, 1)
        WS_URL = Settings.Instance().getBaseURL() + '/image2ctab'
        r = requests.post(WS_URL, data=sio.getvalue())
        ctab = r.content
    except:
        raise
    return ctab


def isID(s):
    "ChEMBL IDs start with CHEMBL"
    return s.strip().upper().startswith('CHEMBL') and len(s) <= 15

def isctab(s):
    "CTABs contain M  END"
    return s.find('M  END')>0


def isInChI(s):
    return s.strip().startswith('InChI=')


def isInChIKey(s):
    return s.isupper() and len(s) == 27 and s[23] == 'S' and s[14] == '-' and s[25] == '-'

class ServerDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ServerDialog, self).__init__(None, style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, *args, **kw)

        self.InitUI()
        self.SetSize((350, 150))
        self.SetTitle("Add server and port")

    def InitUI(self):
        panel = wx.Panel(self, -1)

        dummyLabel = wx.StaticText(panel, -1, "")
        dummyLabel2 = wx.StaticText(panel, -1, "")
        serverLabel = wx.StaticText(panel, -1, "\tServer IP address: ")
        self.serverText = wx.TextCtrl(panel, -1, Settings.Instance().getHost(), size=(175, -1))
        self.serverText.SetInsertionPoint(0)

        portLabel = wx.StaticText(panel, -1, "\tPort number: ")
        self.portText = wx.TextCtrl(panel, -1, Settings.Instance().getPort(), size=(175, -1))

        sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        sizer.AddMany([dummyLabel, dummyLabel2, serverLabel, self.serverText, portLabel, self.portText])

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(panel, label='OK')
        closeButton = wx.Button(panel, label='Close')
        hbox.Add(okButton, flag=wx.RIGHT)
        hbox.Add(closeButton, flag=wx.LEFT)
        sizer.AddSizer(hbox)
        panel.SetSizer(sizer)

        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOK(self, event):
        Settings.Instance().setHost(self.serverText.GetValue())
        Settings.Instance().setPort(self.portText.GetValue())
        self.Destroy()

    def OnClose(self, event):
        self.Destroy()


class MyFrame (wx.Frame):
    def __init__(self):
        wx.Frame.__init__ (self, None, title="ChEMBL Clippy v1.2", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, size=SIZES[SYS])
        self.SetIcon(wx.Icon('./art/clipper.ico', wx.BITMAP_TYPE_ICO))
               
        filemenu = wx.Menu()
        
        m_about = wx.MenuItem(filemenu, 101, '&About...', 'About ChEMBL Clippy')
        filemenu.AppendItem(m_about)
        filemenu.AppendSeparator()

        m_copy_smi = wx.MenuItem(filemenu, 999, '&Copy SMILES', 'Copy the SMILES')
        filemenu.AppendItem(m_copy_smi)
        # filemenu.AppendSeparator()

        m_copy_inchi = wx.MenuItem(filemenu, 299, '&Copy InChI', 'Copy the InChI')
        filemenu.AppendItem(m_copy_inchi)

        m_copy_inchikey = wx.MenuItem(filemenu, 399, '&Copy InChIKey', 'Copy the InChI Key')
        filemenu.AppendItem(m_copy_inchikey)

        m_copy_im = wx.MenuItem(filemenu, 111, '&Copy Image', 'Copy the Image')
        filemenu.AppendItem(m_copy_im)
        filemenu.AppendSeparator()

        m_server = wx.MenuItem(filemenu, 222, '&Server Details...', 'Configure server IP and port')
        filemenu.AppendItem(m_server)
        filemenu.AppendSeparator()

        m_quit = wx.MenuItem(filemenu, 109, '&Quit\tCtrl+Q', 'Quit the Application')
        m_quit.SetBitmap(wx.Image('./art/exit.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        filemenu.AppendItem(m_quit)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()

        self.Bind(wx.EVT_MENU, self.OnQuit, id=109)
        self.Bind(wx.EVT_MENU, self.OnCopyImageToClipboard, id=111)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=101)
        self.Bind(wx.EVT_MENU, self.OnCopySMILESToClipboard, id=999)
        self.Bind(wx.EVT_MENU, self.OnCopyInChIToClipboard, id=299)
        self.Bind(wx.EVT_MENU, self.OnCopyInChIKeyToClipboard, id=399)
        self.Bind(wx.EVT_MENU, self.OnServerSettings, id=222)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnDrawClipboard)
        self.Bind(wx.EVT_PAINT, self.ShowImage)

        self.bmp = None
        self.ctab = None
        self.smiles = None
        self.inchi = None
        self.inchikey = None
        self.clip = None
        self.cliptype = None

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('./art/clipper.ico', wx.BITMAP_TYPE_ICO))
        info.SetName('ChEMBL Clippy')
        info.SetVersion('1.2')
        info.AddDeveloper('George Papadatos')
        info.SetCopyright('(C) 2013 - 2015 ChEMBL Group, EMBL-EBI')
        info.SetWebSite('https://www.ebi.ac.uk/chembl/')
        wx.AboutBox(info)

    def OnServerSettings(self, event):
        srvset = ServerDialog()
        srvset.ShowModal()
        # srvset.Destroy()

    def check(self, s, typ):
        if typ == 'text' and self.cliptype == 'text':
            return self.clip != s
        if typ == 'image' and self.cliptype == 'image':
            return self.clip.GetData() != s.GetData()
        else:
            return True

    def OnDrawClipboard(self, event):
        # print 'got click'
        ctab = None
        s, typ = self.GetTextFromClipboard()
        if self.check(s, typ):
            # print 'not same'
            self.clip = s
            self.cliptype = typ
            if typ == 'text':
                if isID(s):
                    smi = id2smi(s.upper())
                    ctab = smi2ctab(smi)
                elif isInChIKey(s):
                    smi = inchikey2smi(s)
                    ctab = smi2ctab(smi)
                elif isInChI(s):
                    ctab = inchi2ctab(s)
                elif isctab(s):
                    ctab = s
                else:
                    ctab = string2ctab(s)
                    if not ctab:
                        smi = name2smi(s)
                        ctab = smi2ctab(smi)
            elif typ == 'image':
                ctab = image2ctab(s)
            else:
                print 'unknown type:',typ
                self.ShowNothing()
                self.Refresh(True)

            if ctab:
                self.ctab = ctab
                try:
                    self.smiles = ctab2smi(ctab).replace('SMILES Name ', '').strip()
                    self.inchi = ctab2inchi(ctab).strip()
                    self.inchikey = inchi2inchiKey(self.inchi)
                    # print self.inchikey
                    # print self.smiles
                    imag = ctab2image(ctab, self.smiles)
                except:
                    traceback.print_exc()
                    self.ShowNothing()
                    self.Refresh(True)
                try:
                    myWxImage = wx.ImageFromStream(StringIO.StringIO(imag))
                    self.bmp = myWxImage.ConvertToBitmap()
                    self.Refresh(True)
                except:
                    traceback.print_exc()
                    self.ShowNothing()
                    self.Refresh(True)
            else:
                self.ShowNothing()
                self.Refresh(True)
        else:
            # print 'the same'
            pass
            # self.clip = None
            # self.Refresh(True)

    def OnCopySMILESToClipboard(self, event):
        if self.smiles:
            smi = wx.TextDataObject(self.smiles)
            clipboard = wx.Clipboard()
            if clipboard.Open(): 
                clipboard.SetData(smi) 
                clipboard.Flush() 
                clipboard.Close()

    def OnCopyImageToClipboard(self, event):
        if self.bmp:
            d = wx.BitmapDataObject()
            d.SetBitmap(self.bmp)
            clipboard = wx.Clipboard()
            if clipboard.Open(): 
                clipboard.SetData(d)
                clipboard.Flush() 
                clipboard.Close()

    def OnCopyInChIToClipboard(self, event):
        if self.inchi:
            inchi = wx.TextDataObject(self.inchi)
            clipboard = wx.Clipboard()
            if clipboard.Open():
                clipboard.SetData(inchi)
                clipboard.Flush()
                clipboard.Close()

    def OnCopyInChIKeyToClipboard(self, event):
        if self.inchikey:
            inchikey = wx.TextDataObject(self.inchikey)
            clipboard = wx.Clipboard()
            if clipboard.Open():
                clipboard.SetData(inchikey)
                clipboard.Flush()
                clipboard.Close()

    def OnQuit(self, event):
        self.Close()

    def GetTextFromClipboard(self):
        clipboard = wx.Clipboard()
        if clipboard.Open():
            if clipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                typ = 'text'
                data = wx.TextDataObject()
                clipboard.GetData(data)
                s = str(data.GetText().encode('utf-8'))
                clipboard.Close()
                return s, typ
            elif clipboard.IsSupported(wx.DataFormat(wx.DF_BITMAP)):
                typ = 'image'
                data = wx.BitmapDataObject()
                clipboard.GetData(data)
                img = wx.ImageFromBitmap(data.GetBitmap())
                clipboard.Close()
                return img, typ
            else:
                clipboard.Close()
                return None, None
     
    def ShowImage(self, event):
        if SYS.startswith('Win'):
            event.Skip()
        if self.bmp:
            try:
                dc = wx.PaintDC(self)
                dc.DrawBitmap(self.bmp, 0, 0, True)
            except:
                traceback.print_exc()
                self.ShowNothing()
        
    def ShowNothing(self):
        self.SetBackgroundColour(wx.WHITE)
        self.bmp = None     
        self.ctab = None
        self.smiles = None
        self.inchi = None
        self.inchikey = None

app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()

