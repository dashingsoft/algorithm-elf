program hanoi;

procedure hanoi(n:integer; x,y,z:char);
{将塔座x上编号从1至n，直径依小至大的n个圆盘移到塔座z上，y可用作辅助塔座}
begin
    if n=1
        then move(x,1,z) {将编号为1的圆盘从x移到z}
    else begin
        {将x上编号从1至n-1的圆盘移动到y上，z为辅助塔座}
        hanoi(n-1,x,z,y); {将编号n-1的圆盘从x移到z}
        move(x,n,z);
        {将y上编号从1至n-1的圆盘移动到z上，x为辅助塔座}
       hanoi(n-1,y,x,z);
    end;
end; {hanoi}

function move (x1 : char; x2: char):integer;
var
   v0	    : integer;
   v1,v2,v3 : char;
   V4	    : integer;
begin
   v0 := 1;
   for v0 := 1 to 100 do
   begin
      v1 := "xxx";
   end;
   s++;
   repeat
      v2 := "yyy";
   until v2 = 0;

procedure copy_node(x1 : integer);
begin

begin
   hanoi(2, 'a', 'b', 3, 'c');
end.