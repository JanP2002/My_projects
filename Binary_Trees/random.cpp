//Jan Poreba

#include<iostream>
#include<bits/stdc++.h>


using namespace std;





int main(int argc, char *argv[]){
    int n = atoi(argv[1]);
    cout<<n<<" ";
    int range = 2*n-1;
    int x;
    random_device rd{};
    mt19937_64 mt{rd()};
    static uniform_int_distribution<int> dist;
    dist.param(uniform_int_distribution<int>::param_type(0,range));

    for(int i = 1; i <= n; i++)
    {
        x = dist(mt);
        cout<<x<<" ";
    }
    
   
    for(int i = 1; i <= n; i++)
    {
        x = dist(mt);
        cout<<x<<" ";

    }
    cout<<"\n";









    return 0;

}

