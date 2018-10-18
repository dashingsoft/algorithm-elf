procedure myfunction();
type
   tfa		       =  array [1..10] of string;
begin
   {
   i := 1 + 2*3*4+5;
   j := 1 + 2 + 3 + 4 + 5;
   k := 1 * 2 * 3 * 4 + 5 + 6;
   i := 1 * ( 2 + 3 + 4 ) * 5 + 6 + 7;
   j := 1 * -2 * 3 + 4;
   k := 1+2+3 and 4+5+6 and 7 + 8 and 9 and 10;
   k := 1 * 2 * 3 / 4 * 5 + 6;
   i := 1 + 2*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*4+5;
   i := 1 + 2*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*3*4+( 5-6);
   i := 1 * ( 2 + 3 + 4 + 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 4+ 5 ) * 6 * ( 7 + 8);
   printf(1,2);
   printf(1,2,3,4);
   printf(1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4);
   s := 1 + printf(1,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4)
   + 3 * 4 * 5;
   k := 2 * printf( 1,23,5) + 8;
   i := ( k = 0 ) and ( k = 1 ) and ( k = 1 )and ( k = 1 )and ( k = 1 )and ( k = 1 )and ( k = 1 );}
   }
end;

{
 多行注释的测试
 下面的规则
}

function test(var s : integer, x, y : string ):integer;
type
   ta		       = Integer;	
   pa		       = ^Integer;
   Ten		       = (red, green, blue);
			    tr = record of
			    name  : string;
			    value : string;
			 end;	  
   ts		       = set of Ten;
   ta		       = array of integer;
   tfa		       =  array [1..10] of string;
   
var 
   v1, v2, v3 : string;
begin   
   s := 1 + 2*3*4+5;
   x := "1234567890";
   if s >= 0 then
      myfunction(x, y, z);
   f.a.b := c;
   f.a[2].b := c;
   f.a(2,3);
   printf("123", v1, v2);
end; { myfunction }
