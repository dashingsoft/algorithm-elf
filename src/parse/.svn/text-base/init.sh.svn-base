# 脚本功能：
# 
#     删除 autobuild 工具产生的中间文件
#     使用 sed 替换 configure.ac 中 AC_CONFIG_FILES 的行
#     使用 sed 替换 Makefile.am 中 EXTRA_DIST 和 SUBDIRS 的行
#
#    一般和 makeconf.sh 配合使用，首先使用本文件把原来用
#    autobuild 工具自动产生的文件全部清除，然后调用
#    makeconf.sh，调用 autobuild 的系列工具生成 configure 文
#    件。
#
# 使用方法：
#
#    在包含 configure.ac 和 Makefile.am 的目录下直接调用
#
#    $ ./init.sh
#    
rm -rf autom4te.cache po ABOUT-NLS aclocal.m4 configure makefile.in ChangeLog config.h.in
sed -i -e "s/^AC_CONFIG_FILES.*/AC_CONFIG_FILES([Makefile])/g" configure.ac
sed -i -e "s/^SUBDIRS.*/SUBDIRS =/g" Makefile.am
sed -i -e "s/^EXTRA_DIST.*/EXTRA_DIST = /g" Makefile.am
cd build-aux
rm -rf m4 config.* install-sh ltmain.sh missing ylwrap