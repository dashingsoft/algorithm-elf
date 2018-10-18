# -*- coding: utf-8 -*-
#
import sys
import os
import locale
import codecs
import gettext

output_encoding = locale.getpreferredencoding()
inner_encoding = 'utf-8'

def decode_handler(e):
    if type(e) is UnicodeDecodeError:
        s = e.args[1]
        text = s[e.start:].strip().decode(inner_encoding)
    return (text, -1)

def printf(s):
    if isinstance(s, str):
        s = s.decode(inner_encoding)            
    sys.__stdout__.write(s.encode(output_encoding))
    
def set_locale(domain, lang=None):
    try:
        if lang is None:
            lang, encode = locale.getdefaultlocale()
        if lang:
            os.environ["LANG"] = lang
        else:
            lang = os.environ.get("LANG", "")
        lang = lang.split('.')[0].strip()            
        lang = lang.split('_')[0].lower()
        if lang == "zh":       
            codecs.register_error("strict", decode_handler)
    except Exception, inst:
        sys.stderr.write("Warning: setting locale failed: " + str(inst))        
    gettext.install(domain, "locale", True, inner_encoding)
    for i in range(len(sys.argv)):
        if isinstance(sys.argv[i], str):
            sys.argv[i] = sys.argv[i].decode(output_encoding)