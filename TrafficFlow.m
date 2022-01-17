clc;clear all;close all;
Table1 = readtable("CSV_DATA\VD-N5-N-20.412-M-LOOP.csv");
Table2 = readtable("CSV_DATA\VD-N5-N-21.055-M-PS-LOOP.csv");

[v1,q1,p1,v1f,p1j]=datatrans(Table1);
[v2,q2,p2,v2f,p2j]=datatrans(Table2);


p1c=p1j/2;%critial density
q1m=v1f*(p1c-p1c^2/p1j);

% 3th row is 00:00
X=643;
nx =1000;           
T = 60;             
nt =6000;           
dx=X/nx;           
dt=T/nt; 
xScale = 0:dx:X;   
tScale = 0:dt:T; 
tes_index=3333;

for i = 1:nt+1
    for j = 1:nx+1
        i_t=floor(dt*i);
        K(j,i)=(p1(tes_index+i_t)*(nx-j+1)+p2(tes_index+i_t)*(j-1))/nx;
    end
end




K=fliplr(fliplr(K'))';
contourf(tScale, xScale, K,60,'LineColor', 'none')
colorbar;
xlabel({'time (m)'});
ylabel({'x (m)'});








function [v,q,p,vf,pj]=datatrans(Table)
    v=Table(:,7).Variables;%outside speed
    q=Table(:,10).Variables;%flow
    num=length(v);
    cnt=0;
    for i = 1:num
        if v(i,1) == 0 || v(i,1)== -99 || q(i,1)==0
            p(i,1)=0;
        else
            cnt=cnt+1;
            p(i,1)=q(i)/v(i);
            p_fit(cnt,1)= p(i,1);
            q_fit(cnt,1)= q(i);
            v_fit(cnt,1)= v(i);
        end    
    end
    A=[ones(cnt,1),p_fit];
    b=lsqr(A,v_fit);
    vf=b(1,1);
    pj=-b(1,1)/b(2,1);
    pc=pj/2;%critial density
    qm=vf*(pc-pc^2/pj);

end