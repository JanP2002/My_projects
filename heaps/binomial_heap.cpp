//Jan Poreba
#include<stdio.h>
#include<stdlib.h>
#include<limits.h>
#include<bits/stdc++.h>
#include<assert.h>
#include<iostream>
#include<ostream>
#include<stdbool.h>


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
    struct node* sibling;
} node;


node* new_node(int element)
{
    node* node_ptr = (node*) malloc( sizeof(struct node));
    node_ptr->key = element;
    node_ptr->child = NULL;
    node_ptr->parent = NULL;
    node_ptr->degree = 0;
    node_ptr->sibling = NULL;
    return node_ptr;
}



typedef struct node* heap_head;


typedef struct Heap
{
    heap_head head;
} Heap;


Heap* make_binomial_heap()
{
    Heap* heap_ptr = (Heap*) malloc( sizeof(struct Heap));
    heap_ptr->head = NULL;
    return heap_ptr;
}


node* heap_minimum(Heap* heap)
{
    node* y = NULL;
    node* x = heap->head;
    int mini = INT_MAX;
    while(x != NULL)
    {
        if(compare(mini, x->key))
        {
            mini = x->key;
            y = x;
        }
        x = x->sibling;
    }
    return y;
}


void heap_link(node* y, node* z)
{
    y->parent = z;
    y->sibling = z->child;
    z->child = y;
    z->degree = z->degree + 1;
}


heap_head heap_merge(Heap* h1, Heap* h2)
{
   if(h1->head == NULL)
   {
        return h2->head;
   }
   if(h2->head == NULL)
   {
        return h1->head;
   }
   heap_head curr1 = h1->head;
   heap_head curr2 = h2->head;
   heap_head curr = NULL;
   heap_head new_heap = NULL;
   if(curr1->degree <= curr2->degree)
   {
        curr = curr1;
        curr1 = curr1->sibling;
   }
   else
   {
        curr = curr2;
        curr2 = curr2->sibling;
   }
   new_heap = curr;
   while(curr1 != NULL && curr2 != NULL)
   {
        if(curr1->degree <= curr2->degree)
        {
            curr->sibling = curr1;
            curr1 = curr1->sibling;
        }
        else
        {
            curr->sibling = curr2;
            curr2 = curr2->sibling;
        }
        curr = curr->sibling;
   }
   if(curr1 != NULL)
   {
        while(curr1 != NULL)
        {
            curr->sibling = curr1;
            curr1 = curr1->sibling;
            curr = curr->sibling;
        }
   }
    if(curr2 != NULL)
   {
        while(curr2 != NULL)
        {
            curr->sibling = curr2;
            curr2 = curr2->sibling;
            curr = curr->sibling;
        }
   }
   return new_heap;
}



Heap* heap_union(Heap* h1, Heap* h2)
{
    Heap* h = make_binomial_heap();
    h->head = heap_merge(h1, h2);
    if(h->head == NULL)
    {
        return h;
    }
    node* prev_x = NULL;
    node* x = h->head;
    node* next_x = x->sibling;
    while(next_x != NULL)
    {
        if(x->degree != next_x->degree || (next_x->sibling != NULL && next_x->sibling->degree == x->degree))
        {
            prev_x = x;//1 i 2
            x = next_x;
        }
        
        else if(!compare(x->key, next_x->key))
        {
            x->sibling = next_x->sibling;//3
            heap_link(next_x, x);
        }
        else
        {
            if(prev_x == NULL)
            {
                h->head = next_x;//4
            }
            else
            {
                prev_x->sibling = next_x;//4
            }
            heap_link(x, next_x);//4
            x = next_x;//4
        }
        next_x = x->sibling;//koniec while
    }
    return h;
}



Heap* heap_insert(Heap* heap, node* x)
{
    Heap* new_heap = make_binomial_heap();
    x->parent = NULL;
    x->child = NULL;
    x->sibling = NULL;
    x->degree = 0;
    new_heap->head = x;
    heap = heap_union(heap, new_heap);
    return heap;
}



Heap* extract_min(Heap* heap, int* min_variable_ptr)
{
    if(heap == NULL || heap->head == NULL)
    {
        printf("Kopiec jest pusty\n");
        *min_variable_ptr = INT_MAX;
        return heap;
    }
    node* prev = NULL;
    node* curr = heap->head;
    node* next = curr->sibling;
    node* min_node = heap->head;
    while(next != NULL)
    {
        
        if(compare(min_node->key, next->key))
        {
            min_node = next;
            prev = curr;
        }
        curr = next;
        next = curr->sibling;
    }
    if(prev == NULL)
    {
        heap->head = min_node->sibling;
    }
    else if(prev != NULL && min_node->sibling == NULL)
    {
        prev->sibling = NULL;
    }
    else
    {
        prev->sibling = min_node->sibling;
    }
    Heap* new_heap = make_binomial_heap();
    node* new_list = min_node->child;
    prev = NULL;
    curr = new_list;
    while(curr != NULL)
    {
        node* tail = curr->sibling;
        curr->sibling = prev;
        curr->parent = NULL;
        prev = curr;
        curr = tail;
    }
    new_list = prev;
    new_heap->head = new_list;
    heap = heap_union(heap, new_heap);
    *min_variable_ptr = min_node->key;
    free(min_node);
    return heap;
}


bool is_Empty(Heap* heap)
{
    return heap->head == NULL;
}





int main()
{
    int n;
    printf("Podaj liczbe elementow wstawianych do kazdego kopca:\n");
    scanf("%d", &n);
    printf("Liczba elementow: %d\n", n);
    ofstream fout_comp;
    fout_comp.open("binomial_heap_historic.txt");
    fout_comp<<"i "<<"liczba porownan\n";
    Heap* heap1 = make_binomial_heap();
    Heap* heap2 = make_binomial_heap();

    for(int i = 1; i <= n; i++)
    {
        int element;
        scanf("%d", &element);
        node* x = new_node(element);
        heap1 = heap_insert(heap1, x);
        fout_comp<<i<<" "<<compare_counter<<"\n";
        reset_compare_counter();
    }

    for(int i = 1; i <= n; i++)
    {
        int element;
        scanf("%d", &element);
        node* x = new_node(element);
        heap2 = heap_insert(heap2, x);
        fout_comp<<i+n<<" "<<compare_counter<<"\n";
        reset_compare_counter();

    }

    Heap* heap = heap_union(heap1, heap2);
    fout_comp<<2*n+1<<" "<<compare_counter<<"\n";
    reset_compare_counter();

    int* t = (int*)malloc(2*n* sizeof(int));
    for(int i = 1; i <= 2*n; i++)
    {
        int curr_min = INT_MAX;
        heap = extract_min(heap, &curr_min);
        t[i-1] = curr_min;
        fout_comp<<2*n+1+i<<" "<<compare_counter<<"\n";
        reset_compare_counter();
    }
    assert(is_correctly_sorted(t, n));
    assert(is_Empty(heap));
    fout_comp.close();



    
    
    return 0;
}