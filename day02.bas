100 dim m(1000)

105 REM Part 1
110 gosub 500
115 m(1) = 12: m(2) = 2
120 gosub 200
130 print "Part 1:"; m(0)

135 REM Part 2
140 for n = 0 to 99
145 for v = 0 to 99
150 gosub 500
151 m(1) = n: m(2) = v
155 gosub 200
160 if m(0) = 19690720 then 180
165 next v
170 next n
175 print "No answer found!": end
180 print "Part 2: noun ="; n; ", verb ="; v; ", answer ="; 100*n+v
190 end

200 REM Run the IntCode program
205 ip = 0
210 op = m(ip): a = m(ip+1): b = m(ip+2): c = m(ip+3)
230 if op = 1 then m(c) = m(a) + m(b): goto 300
240 if op = 2 then m(c) = m(a) * m(b): goto 300
250 if op = 99 then return
300 ip = ip + 4
310 goto 210

500 REM Read the data into m()
510 restore 1000
520 mi = 0
530 read x
540 if x = -99999 then return
550 m(mi) = x
560 mi = mi + 1
570 goto 530

1000 data 1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,13,27,1,10,27,31,2,31,13,35,1,10,35,39,2,9,39,43,2,43,9,47,1,6,47,51,1,10,51,55,2,55,13,59,1,59,10,63,2,63,13,67,2,67,9,71,1,6,71,75,2,75,9,79,1,79,5,83,2,83,13,87,1,9,87,91,1,13,91,95,1,2,95,99,1,99,6,0,99,2,14,0,0
1010 data -99999
