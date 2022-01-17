clc;clear;close all;
Table = readtable("CSV_DATA\VD-N5-N-20.412-M-LOOP.csv");

[v,q,p,vf,pj]=datatrans(Table);
pc=pj/2;%critial density
qm=vf*(pc-pc^2/pj);

X=643;
nx =10;           
T = 60;             
nt =6;           
dx=X/nx;           
dt=T/nt; 
xScale = 0:dx:X;   
tScale = 0:dt:T; 
dt/dx*6/100
tes_index=2449;

i=1;
total_dis=643;
count=1;
 for j= 1:nx+1
    dis=v(tes_index+i-j)*100/6*dt;
    total_dis=total_dis-dis;
    unit=floor(dis/dx)+1;
    if count+unit >= nx+1
        K(count:nx+1,i)=p(tes_index+i-j);
        break;
    else    
        K(count:count+unit,i)=p(tes_index+i-j);
        count=count+unit+1;
    end
    if total_dis <=0
        break;
    end
 end

 for i = 2: nt+1
     i_t=floor(i*dt);
     K(1,i)=p(tes_index-1+i_t);
     for k=2:nx+1
         if K(k,i-1) <pc 
            K(k,i)=K(k,i-1)-(dt/dx)*(6/100)*(Q(vf,K(k-1,i-1),pj)-Q(vf,K(k,i-1),pj));
         else
            K(k,i)=K(k,i-1)-(dt/dx)*(6/100)*(Q(vf,K(k+1,i-1),pj)-Q(vf,K(k,i-1),pj));
         end    
     end
     
 end
K=fliplr(fliplr(K'))';
contourf(tScale, xScale, K,12,'LineColor', 'none')
colorbar;
xlabel({'time (s)'});
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

function q= Q(vf,p,pj)
    if p <=pj/2
        q=vf*p;
    else
        q=pj*vf*(1-p/pj);
    end
end