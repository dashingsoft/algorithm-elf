@ECHO OFF
::
:: 用于将 src/*.py src/algorithm/*.py 中的
:: 国际化字符串提取出来，生成 messages.pot
:: 
:: 赵俊德 (jondy.zhao@gmail.com)
::
:: 2009/07/04 10:30 
::

SETLOCAL

SET PYTHON=C:Python26\python.exe
SET PYGETTEXT=C:Python26\Tools\i18n\pygettext.py
SET SRCPATH=D:\projects\dsAssistant\src
SET OPTIONS=-k _( -p %SRCPATH%\po -x %SRCPATH%\po\messages_zh.po
:: SET OPTIONS=-k _( -p %SRCPATH%\po
SET DOS2UNIX=C:\Cygwin\bin\dos2unix.exe
SET MSGMERGE=C:\Cygwin\bin\msgmerge.exe

@ECHO 开始生成 PO 文件

CD %SRCPATH%

%PYTHON% %PYGETTEXT% %OPTIONS% about.py aftype.py algorithm-elf.py buildprocess.py datapool.py dscore.py dsgraph.py dsplayer.py dsvision.py pascal.py register.py 
%DOS2UNIX% po/messages.pot

@ECHO 合并 messages.pot 到文件 messages_zh.po

CD po
%MSGMERGE% -U messages_zh.po messages.pot
%DOS2UNIX% messages_zh.po

ENDLOCAL

Pause ...
