#
# 使用说明
#
# 一般和 init.sh 配合使用，用于创建 configure 文件，在当前目录下
#
# $ ./init.sh
# $ ./makeconf.sh
#
# 这样就创建了 configure 文件，然后使用该文件编译 Windows 或
# 者 Linux 的可执行文件：
#
# $ mkdir build ; cd build
# $ ../configure --host=i686-pc-mingw32 \
#                --with-libintl-prefix=/usr/local/mingw
# $ make
#
# 注意： 要把编译好的 gettext 模块安装到 /usr/local/mingw 下面
#
# 如果是编译 Linux 下可执行文件，注意要增加路径：
#
# $ mkdir build ; cd build
# $ PATH=/toolschain/i686-pc-linux-gnu/sys-root/usr/bin:$PATH
# $ ../configure --host=i686-pc-linux-gnu
# $ make
# 
libtoolize
gettextize --symlink --no-changelog
mv po/Makevars.template po/Makevars
ls parse.c format_expr.c algorithm-elf.y >> po/POTFILES.in
cp /usr/share/aclocal/bison-i18n.m4 build-aux/m4/
aclocal -I build-aux/m4
autoheader
autoconf
automake --add-missing
