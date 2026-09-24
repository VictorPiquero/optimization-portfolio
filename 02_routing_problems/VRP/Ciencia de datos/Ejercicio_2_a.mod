param n;

set CIUDADES:=1..n;

param dist{CIUDADES,CIUDADES};

var asig{CIUDADES,CIUDADES}>=0 <=1;

minimize cost:
         sum{i in CIUDADES, j in CIUDADES:i>1 and j<i} (asig[i,j]*dist[i,j]);
         
subject to grado{j in CIUDADES}:
        sum{i in CIUDADES:i>1 and i!=j}(asig[i,j])= 2;
        

data;

param n:=10;

param dist:  
	 1	2	3	4	5	6	7	8	9	10	:=
1     10000     171     369    366     525      540     646     488     504     617
2	171	10000	294	537	696	515	817	659	675     688
3	369	294	10000	663	604	809	958	800	651     484
4	366	537	663	10000	318	717	401	243	229     618
5	525	696	604	318	10000	1022	694	536	89      342
6	540	515	809	717	1022	10000	620	583	918    1284
7	646	817	958	401	694	620	10000	158	605    1058
8	488	659	800	243	536	583	158	10000	447     900
9	504	675	651	229	89	918	605	447	10000   369
10	617	688	484	618	342	1284	1058	900	369	10000;
 