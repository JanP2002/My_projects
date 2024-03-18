//Jan Poreba
#include<iostream>
#include<iomanip>
#include<assert.h>
#include<bits/stdc++.h>
#include<ostream>
#include<time.h>
#include<sys/time.h>
#include<limits.h>
#include<stdio.h>
#include <stdlib.h>
#include<queue>


using namespace std;


typedef struct node{
  struct node *parent;
  struct node *left;
  struct node *right;
  int element;
} node;

typedef struct node* nodeptr;

struct node* root = NULL;


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


int ptr_operations = 0;

void reset_ptr_operations()
{
  ptr_operations = 0;
}

void insert( struct node** root, struct node* z )
{
  ptr_operations++;
  if( z==NULL) return;
  struct node* y = NULL;
  struct node* x = *root;
  while(x != NULL)
  {
    ptr_operations++;
    y = x;
    ptr_operations++;
    if(compare(x->element, z->element))
    {
      x=x->left;
    }
    else
    {
      x=x->right;
    }
    ptr_operations++;
  }
  z->parent=y;
  ptr_operations++;
  if(y==NULL)
  {
    *root = z;
    ptr_operations++;
  }
  else if(compare(y->element, z->element))
  {
    y->left = z;
    ptr_operations++;
  }
  else
  {
    y->right = z;
    ptr_operations++;
  }
  ptr_operations++;

}




int height(struct node** root) {
  if(root == NULL || *root == NULL)
  {
    return -1;
  }
  int left_height = height(&(*root)->left);
  int right_height = height(&(*root)->right);
  if(left_height > right_height)
  {
    return left_height+1;
  }
  else 
  {
    return right_height+1;
  }


}

struct node* tree_minimum(struct node* x)
{
  while(x->left != NULL)
  {
    x = x->left;
    ptr_operations += 2;
  }
  return x;
}


struct node* stree_successor(struct node* x)
{
  if(x->right != NULL)
  {
    return tree_minimum(x->right);
  }
  ptr_operations++;
  struct node* y = x->parent;
  ptr_operations++;
  while(y != NULL && x==y->right)
  {
    x = y;
    y = y->parent;
    ptr_operations += 4;
  }
  return y;
}


void transplant(struct node** root, struct node* u, struct node* v)
{
  if(u->parent == NULL)
  {
    *root = v;
    ptr_operations += 2;
  }
  else if(u == u->parent->left)
  {
    u->parent->left = v;
    ptr_operations += 3;
  }
  else 
  {
    u->parent->right = v;
    ptr_operations += 3;
  }
  if(v != NULL)
  {
    v->parent = u->parent;
    ptr_operations++;
  }
  ptr_operations++;
}



void tree_delete(struct node** root, struct node* z)
{
  if(z->left == NULL)
  {
    transplant(root, z, z->right);
    ptr_operations++;
  }
  else if(z->right == NULL)
  {
    transplant(root, z, z->left);
    ptr_operations++;
  }
  else 
  {
    struct node* y = tree_minimum(z->right);
    ptr_operations++;
    if(y->parent != z)
    {
      transplant(root, y, y->right);
      y->right = z->right;
      y->right->parent = y;
      ptr_operations += 2;
    }
    ptr_operations++;
    transplant(root, z, y);
    y->left = z->left;
    y->left->parent = y;
    ptr_operations += 2;
  }
  delete z;
}


struct node* tree_search(struct node* x, int key)
{
  while(x != NULL && !equals(key, x->element))
  {
    ptr_operations += 2;
    if(compare(x->element, key))
    {
      x = x->left;
    }
    else
    {
      x = x->right;
    }
    ptr_operations++;
  }
  return x;
}


void delete_key(struct node** root, int key)
{
  struct node* node = tree_search(*root, key);
  ptr_operations++;
  if(node != NULL)
  {
    tree_delete(root, node);
  }
  ptr_operations++;
  
}




void delete_tree(struct node** root)
{
  struct node* current = *root;
  struct node* tmp;
  while(*root != NULL)
  {
    //assert(current != NULL)
    if(current->left != NULL)
    {
      current = current->left;
    }
    else
    {
      current->left = (*root)->right;
      tmp = (*root)->left;
      if(current == *root)
      {
        current = current->left;
      }
      free(*root);
      *root = tmp;
    }
  }
}



void simulation1(int N_MIN, int N_MAX, int delta, int m)
{
    ofstream fout_bst_height;
    fout_bst_height.open("bst_height_inc.txt");
    fout_bst_height<<"n"<<" ";
    ofstream fout_bst_height_m;
    fout_bst_height_m.open("bst_height_max_inc.txt");
    fout_bst_height_m<<"n"<<" ";
    ofstream fout_bst_comp;
    fout_bst_comp.open("bst_compares_inc.txt");
    fout_bst_comp<<"n"<<" ";
    ofstream fout_bst_comp_m;
    fout_bst_comp_m.open("bst_compares_max_inc.txt");
    fout_bst_comp_m<<"n"<<" ";
    ofstream fout_bst_subs;
    fout_bst_subs.open("bst_subs_inc.txt");
    fout_bst_subs<<"n"<<" ";
    ofstream fout_bst_subs_m;
    fout_bst_subs_m.open("bst_subs_max_inc.txt");
    fout_bst_subs_m<<"n"<<" ";
    
    for(int i = 0; i < m; i++){
        fout_bst_height<<"m"<<i+1<<" ";
        fout_bst_height_m<<"m"<<i+1<<" ";
        fout_bst_comp<<"m"<<i+1<<" ";
        fout_bst_comp_m<<"m"<<i+1<<" ";
        fout_bst_subs<<"m"<<i+1<<" ";
        fout_bst_subs_m<<"m"<<i+1<<" ";
    }
    fout_bst_height<<endl;
    fout_bst_height_m<<endl;
    fout_bst_comp<<endl;
    fout_bst_comp_m<<endl;
    fout_bst_subs<<endl;
    fout_bst_subs_m<<endl;
    root = NULL;
    for(int i = N_MIN; i<= N_MAX; i+= delta)
    {
        fout_bst_height<<i<<" ";
        fout_bst_height_m<<i<<" ";
        fout_bst_comp<<i<<" ";
        fout_bst_comp_m<<i<<" ";
        fout_bst_subs<<i<<" ";
        fout_bst_subs_m<<i<<" ";
        int size = i;
        for(int j = 0; j < m; j++){

            long double avg_height = 0;
            long long sum_height = 0;
            long long sum_comp = 0;
            long double avg_comp = 0;
            long long sum_subs = 0;
            long double avg_subs = 0;
            int max_comp = 0;
            int max_subs = 0;
            int max_height = 0;
            for(int k = 1; k <= size; k++)
            {
                struct node* node_ptr = new node;
                node_ptr->element = k;
                node_ptr->left=NULL;
                node_ptr->right=NULL;
                node_ptr->parent=NULL;
                insert(&root, node_ptr );
                int h = height(&root);
                sum_height += h;
                if(h > max_height)
                {
                  max_height = h;
                }
                sum_comp += compare_counter;
                sum_subs += ptr_operations;
                if(compare_counter > max_comp)
                {
                  max_comp = compare_counter;
                }
                if(ptr_operations > max_subs)
                {
                  max_subs = ptr_operations;
                }
                reset_compare_counter();
                reset_ptr_operations();
            }

            int range = 2*size-1;
            int x;
            random_device rd{};
            mt19937_64 mt{rd()};
            static uniform_int_distribution<int> dist;
            dist.param(uniform_int_distribution<int>::param_type(0,range));

            for(int k = 1; k <= size; k++)
            {
                x = dist(mt);
                delete_key(&root, x);
                int h = height(&root);
                sum_height += h;
                if(h > max_height)
                {
                  max_height = h;
                }
                sum_comp += compare_counter;
                sum_subs += ptr_operations;
                if(compare_counter > max_comp)
                {
                  max_comp = compare_counter;
                }
                if(ptr_operations > max_subs)
                {
                  max_subs = ptr_operations;
                }
                reset_compare_counter();
                reset_ptr_operations();
            }
            avg_height = sum_height*1.0/(2*size);
            fout_bst_height<<avg_height<<" ";
            fout_bst_height_m<<max_height<<" ";
            avg_comp = sum_comp*1.0/(2.0*size);
            fout_bst_comp<<avg_comp<<" ";
            fout_bst_comp_m<<max_comp<<" ";
            avg_subs = sum_subs*1.0/(2*size);
            fout_bst_subs<<avg_subs<<" ";
            fout_bst_subs_m<<max_subs<<" ";
            delete_tree(&root);
        }
        fout_bst_height<<endl;
        fout_bst_height_m<<endl;
        fout_bst_comp<<endl;
        fout_bst_comp_m<<endl;
        fout_bst_subs<<endl;
        fout_bst_subs_m<<endl;
    }
    fout_bst_height.close();
    fout_bst_height_m.close();
    fout_bst_comp.close();
    fout_bst_comp_m.close();
    fout_bst_subs.close();
    fout_bst_subs_m.close();

}


void simulation2(int N_MIN, int N_MAX, int delta, int m)
{
    ofstream fout_bst_height;
    fout_bst_height.open("bst_height_rand.txt");
    fout_bst_height<<"n"<<" ";
    ofstream fout_bst_height_m;
    fout_bst_height_m.open("bst_height_max_rand.txt");
    fout_bst_height_m<<"n"<<" ";
    ofstream fout_bst_comp;
    fout_bst_comp.open("bst_compares_rand.txt");
    fout_bst_comp<<"n"<<" ";
    ofstream fout_bst_comp_m;
    fout_bst_comp_m.open("bst_compares_max_rand.txt");
    fout_bst_comp_m<<"n"<<" ";
    ofstream fout_bst_subs;
    fout_bst_subs.open("bst_subs_rand.txt");
    fout_bst_subs<<"n"<<" ";
    ofstream fout_bst_subs_m;
    fout_bst_subs_m.open("bst_subs_max_rand.txt");
    fout_bst_subs_m<<"n"<<" ";
    
    for(int i = 0; i < m; i++){
        fout_bst_height<<"m"<<i+1<<" ";
        fout_bst_height_m<<"m"<<i+1<<" ";
        fout_bst_comp<<"m"<<i+1<<" ";
        fout_bst_comp_m<<"m"<<i+1<<" ";
        fout_bst_subs<<"m"<<i+1<<" ";
        fout_bst_subs_m<<"m"<<i+1<<" ";
    }
    fout_bst_height<<endl;
    fout_bst_height_m<<endl;
    fout_bst_comp<<endl;
    fout_bst_comp_m<<endl;
    fout_bst_subs<<endl;
    fout_bst_subs_m<<endl;
    root = NULL;
    for(int i = N_MIN; i<= N_MAX; i+= delta)
    {
        fout_bst_height<<i<<" ";
        fout_bst_height_m<<i<<" ";
        fout_bst_comp<<i<<" ";
        fout_bst_comp_m<<i<<" ";
        fout_bst_subs<<i<<" ";
        fout_bst_subs_m<<i<<" ";
        int size = i;
        for(int j = 0; j < m; j++){

            long double avg_height = 0;
            long long sum_height = 0;
            long long sum_comp = 0;
            long double avg_comp = 0;
            long long sum_subs = 0;
            long double avg_subs = 0;
            int max_comp = 0;
            int max_subs = 0;
            int max_height = 0;

            int range = 2*size-1;
            int x;
            random_device rd{};
            mt19937_64 mt{rd()};
            static uniform_int_distribution<int> dist;
            dist.param(uniform_int_distribution<int>::param_type(0,range));
            for(int k = 1; k <= size; k++)
            {
                struct node* node_ptr = new node;
                x = dist(mt);
                node_ptr->element = x;
                node_ptr->left=NULL;
                node_ptr->right=NULL;
                node_ptr->parent=NULL;
                insert(&root, node_ptr);
                int h = height(&root);
                sum_height += h;
                if(h > max_height)
                {
                  max_height = h;
                }
                sum_comp += compare_counter;
                sum_subs += ptr_operations;
                if(compare_counter > max_comp)
                {
                  max_comp = compare_counter;
                }
                if(ptr_operations > max_subs)
                {
                  max_subs = ptr_operations;
                }
                reset_compare_counter();
                reset_ptr_operations();
            }


            for(int k = 1; k <= size; k++)
            {
                x = dist(mt);
                delete_key(&root, x);
                int h = height(&root);
                sum_height += h;
                if(h > max_height)
                {
                  max_height = h;
                }
                sum_comp += compare_counter;
                sum_subs += ptr_operations;
                if(compare_counter > max_comp)
                {
                  max_comp = compare_counter;
                }
                if(ptr_operations > max_subs)
                {
                  max_subs = ptr_operations;
                }
                reset_compare_counter();
                reset_ptr_operations();
            }
            avg_height = sum_height*1.0/(2*size);
            fout_bst_height<<avg_height<<" ";
            fout_bst_height_m<<max_height<<" ";
            avg_comp = sum_comp*1.0/(2.0*size);
            fout_bst_comp<<avg_comp<<" ";
            fout_bst_comp_m<<max_comp<<" ";
            avg_subs = sum_subs*1.0/(2*size);
            fout_bst_subs<<avg_subs<<" ";
            fout_bst_subs_m<<max_subs<<" ";
            delete_tree(&root);
        }
        fout_bst_height<<endl;
        fout_bst_height_m<<endl;
        fout_bst_comp<<endl;
        fout_bst_comp_m<<endl;
        fout_bst_subs<<endl;
        fout_bst_subs_m<<endl;
    }
    fout_bst_height.close();
    fout_bst_height_m.close();
    fout_bst_comp.close();
    fout_bst_comp_m.close();
    fout_bst_subs.close();
    fout_bst_subs_m.close();

}



int main()
{
    int N_MIN = 1000;
    int N_MAX = 10000;
    int delta = 1000;
    int m = 20;
    cout<<"simulation1\n";
    simulation1(N_MIN, N_MAX, delta, m);
    cout<<"simulation2\n";
    simulation2(N_MIN, N_MAX, delta, m);
    return 0;
}