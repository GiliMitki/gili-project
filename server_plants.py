#!/usr/bin/python
print "Content-type: text/html\n\n";
print "<html><head>";
print "<title>CGI Test</title>";
print "</head><body>";
M=[[[1,2,3], [200,200,200], [255, 100, 150]],[[1,2,3], [200,200,200], [255, 100, 150]], [[1,2,3], [200,200,200], [255, 100, 150]]]
H=len(M)
W=len(M[0])
<?php
	for($i=0;$i< ?> H <? ;$i++){
		for($j=0;$j< ?> W <? ;$j++){
	      		 $array[]=array('x' =>$i,'y'=>$j ,'color' =>imagecolorallocate($im,?> M[<? $i ?>][<? $j ?>][0], M[<? $i ?>][<? $j ?>][1],M[<? $i ?>][<? $j ?>][2]));
		}
	}
?>
print "</body></html>";
