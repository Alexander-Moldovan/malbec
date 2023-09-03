                 |    1    	p68h11
                 |    2    	ORG	$2000
2000    8603     |    3    	ldaa	#3
2002    C602     |    4    	ldab	#2
2004    1B       |    5    	aba
2005    C601     |    6    	ldab	#1
2007    10       |    7    	sba
2008    20FE     |    8    fin	bra	fin
                 |   10    	END
