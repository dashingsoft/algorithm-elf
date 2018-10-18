#
#  创建文档，将 Doc Book 格式的 XML 转换成为 HTML
#  
#  创建日期：2010/10/21
#  作者： 赵俊德 (jondy.zhao@gmail.com)
#
#  使用方法：
#      进入 cygwin 环境，运行
#      $ cd d:/projects/dsAssistant/src/docs
#      $ make
#
XSLTPROC=xsltproc
XSLFILE=/usr/share/sgml/docbook/xsl-stylesheets/html/docbook.xsl
XSLTPARA=--stringparam section.autolabel 1 \
         --stringparam section.label.includes.component.label 1 

doc: getting-started.html \
     zh/getting-started.html

getting-started.html: getting-started.xml

zh/getting-started.html: zh/getting-started.xml

%.html: %.xml
	$(XSLTPROC) $(XSLTPARA) --output $@ $(XSLFILE) $<

