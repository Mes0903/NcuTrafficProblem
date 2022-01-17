clc;clear all;close all;
Table1 = readtable("CSV_DATA\VD-N5-N-20.412-M-LOOP.csv");
Table2 = readtable("CSV_DATA\VD-N5-N-21.055-M-PS-LOOP.csv");

[v1,q1,p1,v1f,p1j]=datatrans(Table1);
[v2,q2,p2,v2f,p2j]=datatrans(Table2);


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
        K(j,i)=p1(tes_index+i_t)*(nx-j+1)/nx+p2(tes_index+i_t)*(j-1)/nx;
    end
end
 

[t,p]=ode45(@(t,p) ODE_RHS(t,p,p1(tes_index:tes_index+T),p2(tes_index:tes_index+T),dx,nx),[0:dt:T],K(2:nx,1));
K(2:nx,:)=fliplr(fliplr(p)');
K=fliplr(fliplr(K'))';
contourf(tScale, xScale, K,12,'LineColor', 'none')
colorbar;
xlabel({'time (m)'});
ylabel({'x (m)'});



function dpxdt=ODE_RHS(t,p,p1,p2,dx,nx)
   
    i_t=floor(t);
    dpxdt(1)=-(p(2)-p1(i_t+1))/(2*dx);
    for i = 2:nx-2    
        dpxdt(i)=-(p(i+1)-p(i-1))/(2*dx);
    end
    dpxdt(nx-1)=-(p2(i_t+1)-p(nx-2))/(2*dx);
    dpxdt=dpxdt';
end


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

function q= Q(vf,p,pj)
    if p <=pj/2
        q=vf*p;
    else
        q=pj*vf*(1-p/pj);
    end
end