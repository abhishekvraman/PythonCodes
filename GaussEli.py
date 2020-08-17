# To solve linear equations of with same number of variables
# For example to solve system of following equations
# 4x1+2x2+x3=11
# -x1+2x2=3
# 2x1+x2+4x3=16
#Answer=[1.0, 2.0, 3.0]

def gaussElim(a):
    n=len(a)
    if(n!=len(a[0])-1):
        print("Number of equations should be equal to number of variables")
        return        
    for i in range(n-1):
         for k in range(1,n-i):
            quot=a[i+k][i]/a[i][i]
            for j in range(i,n+1):
                a[i+k][j]=a[i+k][j]-quot*a[i][j]
    x=[a[n-1][n]/a[n-1][n-1]]
    for i in range(n-1,0,-1):
        su=0
        for j in range(n-i):
            su=su+x[j]*a[i-1][n-1-j]
        x=x+[(a[i-1][n]-su)/a[i-1][i-1]]
    x.reverse()
    return x
grid_len=int(input("Enter number of variables:"))
a = [list(map(int,input("Input coefficients of equation "+str(i+1)+" separated by space (Eg. ax+by=c enter as=> a b c) :").split())) for i in range(grid_len)]
print (gaussElim (a))
