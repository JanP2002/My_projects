//Jan Poreba
#include<stdio.h>
#include<stdlib.h>
#include<limits.h>
#include<bits/stdc++.h>
#include<assert.h>
#include<iostream>
#include<ostream>
#include<stdbool.h>
#include <random>
#include<cmath>
#define GOLDEN_RATIO_ROUND_DOWN 1.618


using namespace std;

long long compare_counter = 0;

void reset_compare_counter()
{
    compare_counter = 0;
}


bool compare(int a, int b)
{
    compare_counter++;
    return a > b;
}


bool equals(int a, int b)
{
    compare_counter++;
    return a == b;
}


void print_array(int t[], int n)
{
    for(int i = 0; i < n; i++)
    {
        printf("%d ", t[i]);
    }
    printf("\n");
}

bool is_correctly_sorted(int t[], int n)
{
    for(int i = 0; i < n-1; i++)
    {
        if(t[i] > t[i+1])
        {
            return false;
        }
    }
    return true;
}


typedef struct node
{
    int key;
    struct node* parent;
    struct node* child;
    int degree;
    struct node* left;
    struct node* right;
    bool mark;
} node;


node* new_node(int element)
{
    node* node_ptr = (node*) malloc( sizeof(struct node));
    node_ptr->key = element;
    node_ptr->child = NULL;
    node_ptr->parent = NULL;
    node_ptr->degree = 0;
    node_ptr->left = NULL;
    node_ptr->right = NULL;
    node_ptr->mark = false;
    return node_ptr;
}


node* new_node(int element, node* old_child, int old_degree)
{
    node* node_ptr = (node*) malloc( sizeof(struct node));
    node_ptr->key = element;
    node_ptr->child = old_child;
    node_ptr->parent = NULL;
    node_ptr->degree = old_degree;
    node_ptr->left = NULL;
    node_ptr->right = NULL;
    node_ptr->mark = false;
    return node_ptr;
}


typedef struct Heap
{
    node* min_node;
    int n;
} Heap;


Heap* make_fib_heap()
{
    Heap* heap_ptr = (Heap*) malloc( sizeof(struct Heap)); 
    heap_ptr->min_node = NULL;
    heap_ptr->n = 0;
    return heap_ptr;
}


Heap* heap_insert(Heap* heap, node* x)
{
    x->degree = 0;
    x->parent = NULL;
    x->child = NULL;
    x->left = NULL;
    x->right = NULL;
    x->mark = false;
    //polacz x z lista korzeni heap:
    if(heap->min_node != NULL)
    {
        //wstawiamy na lewo od min_node
        (heap->min_node->left)->right = x;
        x->right = heap->min_node;
        x->left = (heap->min_node)->left;
        (heap->min_node)->left = x;
        if(compare(heap->min_node->key, x->key))
        {
            heap->min_node = x;
        }
    }
    else
    {
        heap->min_node = x;
        heap->min_node->left = heap->min_node;
        heap->min_node->right = heap->min_node;
    }
    heap->n = heap->n + 1;
    return heap;
}


int heap_min(Heap* heap)
{
    return heap->min_node->key;
}


Heap* heap_union(Heap* heap1, Heap* heap2)
{
    Heap* new_heap = make_fib_heap();
    if(heap1->min_node != NULL && heap2->min_node != NULL)
    {
        new_heap->min_node = heap1->min_node;
        new_heap->min_node->right->left = heap2->min_node->left;
        heap2->min_node->left->right = new_heap->min_node->right;
        new_heap->min_node->right = heap2->min_node;
        heap2->min_node->left = new_heap->min_node;
        if(compare(heap1->min_node->key, heap2->min_node->key))
        {
            new_heap->min_node = heap2->min_node;
        }
    }
    else if(heap1->min_node == NULL && heap2->min_node != NULL)
    {
        new_heap = heap2;
    }
    else if(heap1->min_node != NULL && heap2->min_node == NULL)
    {
        new_heap = heap1;
    }
    else
    {
        return new_heap;
    }
    new_heap->n = heap1->n + heap2->n;
    return new_heap;
}


void heap_link(node* y, node* x)
{
    //usun y z listy korzeni heap
    y->left->right = y->right;
    y->right->left = y->left;

    if(x->child == NULL)
    {
        x->child = y;
        y->right = y;
        y->left = y;
    }
    else
    {
        node* child = x->child;
        y->right = child;
        y->left = child->left;
        child->left->right = y;
        child->left = y;
    }
    //uczyn y synem x
    y->parent = x;
    x->degree = x->degree + 1;
    y->mark = false;
}


    void fillListWithElements(node *x, list<node*> &A) {
        node *last = x;
        node *w = last;
        do {
            w = w->right;
            A.push_back(w);
        } while (w != last);
    }


    node* unite(node *x, node *y) {
        if (x == NULL) {
            return y;
        } else if (y == NULL) {
            return x;
        } else if (compare(x->key, y->key)) {
            return unite(y, x);
        } else {
            node *xRight = x->left;
            node *yRight = y->left;

            x->left = yRight;
            xRight->right = y;

            y->left = xRight;
            yRight->right = x;

            return x;
        }
    }

void consolidate(Heap* heap)
{
    int Dn = (int)(log(heap->n)/log(GOLDEN_RATIO_ROUND_DOWN));
    node** A = new node*[Dn + 1];
    for(int i = 0; i <= Dn; i++)
    {
        A[i] = NULL;
    }
    // node* w = heap->min_node;//wskaznik na liste korzeni
    // node* start_node = heap->min_node;
    // node* x = NULL;//zawsze wskazuje na max(w, A[w->degree]) na liscie korzeni
    int d = 0;
    //dla kazdego wezla w na liscie korzeni heap
    list<node*> elements;
    fillListWithElements(heap->min_node, elements);
    for (auto x : elements) 
    {
        d = x->degree;
        while(A[d] != NULL)
        {
            node* y = A[d];
            if(compare(x->key, y->key))
            {
                node* temp = x;
                x = y;
                y = temp;
            }
            heap_link(y, x);
            A[d] = NULL;
            d++;
        }
        A[d] = x;
    }
    heap->min_node = NULL;
    for(int i = 0; i < Dn; i++)
    {
        if(A[i] != NULL)
        {   
            A[i]->right = A[i];
            A[i]->left = A[i];
            heap->min_node = unite(heap->min_node, A[i]);
        }
    }
}



Heap* extract_min(Heap* heap, int* min_variable_ptr)
{
    if(heap == NULL || heap->min_node == NULL)
    {
        printf("Kopiec jest pusty\n");
        *min_variable_ptr = INT_MAX;
        return heap;
    }
    node* z = heap->min_node;
    if(z->child != NULL)
    {
        //kazdy syn x wezla z do:
        //dodaj x do listy korzeni
        //aktualnie zamiast heap->min_node
        node* x = z->child;
        do
        {
            x->parent = NULL;
            x = x->right;
        } while (x != z->child);
        heap->min_node = unite(heap->min_node, x);
    }
    z->left->right = z->right;
    z->right->left = z->left;
    if(z == z->right)
    {
        //z byl jedynym korzeniem (i nie mial synow)
        heap->min_node = NULL;
    }
    else
    {
        heap->min_node = z->right;
        consolidate(heap);
    }
    heap->n = heap->n - 1;
    *min_variable_ptr = z->key;
    return heap;
}



bool is_Empty(Heap* heap)
{
    return heap->min_node == NULL;
}


void simulation(int N_MIN, int N_MAX, int delta)
{
    ofstream fout_comp;
    fout_comp.open("fibonacci_heap_all.txt");
    fout_comp<<"n "<<"liczba porownan\n";
    for(int i = N_MIN; i <= N_MAX; i += delta)
    {
        int* t = new int[2*i];
        int range = 2*i-1;
        random_device rd{};
        mt19937_64 mt{rd()};
        static uniform_int_distribution<int> dist;
        dist.param(uniform_int_distribution<int>::param_type(0,range));

        Heap* heap1 = make_fib_heap();
        Heap* heap2 = make_fib_heap();
        for(int j = 1; j <= i; j++)
        {
            int element = dist(mt);
            node* x = new_node(element);
            heap1 = heap_insert(heap1, x);
        }
        for(int j = 1; j <= i; j++)
        {
            int element = dist(mt);
            node* x = new_node(element);
            heap2 = heap_insert(heap2, x);
        }
        Heap* heap = heap_union(heap1, heap2);
        for(int j = 1; j <= 2*i; j++)
        {
            int curr_min = INT_MAX;
            heap = extract_min(heap, &curr_min);
            t[j-1] = curr_min;
        }
        assert(is_correctly_sorted(t, 2*i));
        assert(is_Empty(heap));
        fout_comp<<i<<" "<<compare_counter<<"\n";
        reset_compare_counter();
        delete[] t;
    }
    fout_comp.close();

}


int main()
{
    int N_MIN = 100;
    int N_MAX = 10000;
    int delta = 100;
    simulation(N_MIN, N_MAX, delta);
    
    return 0;
}