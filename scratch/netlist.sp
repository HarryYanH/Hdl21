* `ngspice` Sim Input for `__main__.Tb`
* Generated by `vlsirtools.NgspiceNetlister`
* 
* Anonymous `circuit.Package`
* Generated by `vlsirtools.NgspiceNetlister`
* 

.SUBCKT 2_CL_1e_11_Cc_3e_12_ibias_3e_05_
+ VDD VSS out inp_p inp_n 
* No parameters

mmp1
+ net4 net4 VDD VDD 
+ pmos
+ w='0.5u' l='90n' nf='1' m='10' 

mmp2
+ net5 net4 VDD VDD 
+ pmos
+ w='0.5u' l='90n' nf='1' m='10' 

mmn1
+ net4 inp_n net3 net3 
+ nmos
+ w='0.5u' l='90n' nf='1' m='38' 

mmn2
+ net5 inp_p net3 net3 
+ nmos
+ w='0.5u' l='90n' nf='1' m='38' 

mmn3
+ net3 net7 VSS VSS 
+ nmos
+ w='0.5u' l='90n' nf='1' m='9' 

mmp3
+ out net5 VDD VDD 
+ pmos
+ w='0.5u' l='90n' nf='1' m='4' 

mmn5
+ out net7 VSS VSS 
+ nmos
+ w='0.5u' l='90n' nf='1' m='60' 

cCL
+ out VSS 
+ 1E-11
* No parameters


mmn4
+ net7 net7 VSS VSS 
+ nmos
+ w='0.5u' l='90n' nf='1' m='20' 

iibias
+ VDD net7 
+ 0.00003
* No parameters


cCc
+ net5 out 
+ 3E-12
* No parameters


.ENDS

.SUBCKT Tb
+ VSS 
* No parameters

vvdc
+ vdc_p VSS 
+ dc '1.2' 
+ ac '0' 
* No parameters


vsig_p
+ dcin_p VSS 
+ dc '0.6' 
+ ac '0.5' 
* No parameters


vsig_n
+ dcin_n VSS 
+ dc '0.6' 
+ ac '-0.5' 
* No parameters


xinst
+ vdc_p VSS sig_out dcin_p dcin_n 
+ 2_CL_1e_11_Cc_3e_12_ibias_3e_05_
* No parameters


.ENDS

xtop 0 Tb // Top-Level DUT 


.include "../examples/45nm_bulk.txt"
.op

.ac dec 10 10.0 10000000000.0





