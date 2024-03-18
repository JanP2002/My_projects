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
#include<stdlib.h>


using namespace std;


const bool RED = true;
const bool BLACK = false;



typedef struct node{
  struct node *parent;
  struct node *left;
  struct node *right;
  int element;
  bool color;
} node;


typedef struct tree{
  struct node* root;
  struct node* NILL;
} tree;



tree* create_tree()
{
  tree* t = new tree;
  t->NILL = new node;
  t->NILL->color = BLACK;
  t->NILL->left = NULL;
  t->NILL->right = NULL;
  t->root = t->NILL;
  return t;
}



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



void insert(tree* t, struct node* z)
{
  ptr_operations++;
  if( z==NULL || z== t->NILL) return;
  struct node* y = t->NILL;
  struct node* x = t->root;
  while(x != t->NILL)
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
    ptr_operations ++;
  }
  z->parent=y;
  ptr_operations++;
  if(y==t->NILL)
  {
    t->root = z;
  }
  else if(compare(y->element, z->element))
  {
    y->left = z;
  }
  else
  {
    y->right = z;
  }
  ptr_operations += 2;

}



int height(tree* t, struct node* subtree) {
  if(t == NULL || subtree == t->NILL || subtree == NULL)
  {
    return -1;
  }
  int left_height = height(t, subtree->left);
  int right_height = height(t, subtree->right);
  if(left_height > right_height)
  {
    return left_height+1;
  }
  else 
  {
    return right_height+1;
  }


}


struct node* tree_minimum(tree* t, struct node* x)
{
  while(x->left != t->NILL)
  {
    x = x->left;
    ptr_operations += 2;
  }
  return x;
}


struct node* tree_successor(tree* t, struct node* x)
{
  if(x->right != t->NILL)
  {
    return tree_minimum(t, x->right);
  }
  ptr_operations++;
  struct node* y = x->parent;
  ptr_operations++;
  while(y != t->NILL && x==y->right)
  {
    x = y;
    y = y->parent;
    ptr_operations += 4;
  }
  ptr_operations += 2;
  return y;
}



struct node* tree_search(tree* t, struct node* x, int key)
{
  while(x != t->NILL && !equals(key, x->element))
  {
    ptr_operations++;
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


void delete_tree(tree* t)
{
  struct node* current = t->root;
  struct node* tmp;
  while(t->root != t->NILL)
  {
    //assert(current != t->NILL)
    if(current->left != t->NILL)
    {
      current = current->left;
    }
    else
    {
      current->left = (t->root)->right;
      tmp = (t->root)->left;
      if(current == t->root)
      {
        current = current->left;
      }
      free(t->root);
      t->root = tmp;
    }
  }
}

void free_tree(tree* t)
{
  delete_tree(t);
  free(t->NILL);
}



void left_rotate(tree* t, struct node* x)
{
  struct node* y= x->right;//y bedzie podnoszony
  x->right = y->left;//poddrzewo beta - pod x
  ptr_operations++;
  if(y->left != t->NILL)
  {
    y->left->parent = x;//popraw parent[korzen beta]
    ptr_operations++;
  }
  ptr_operations++;
  y->parent = x->parent;//byly ojciec x bedzie ojcem y
  ptr_operations++;
  if(x->parent == t->NILL)
  {
    t->root = y;//y - nowy korzen t
    ptr_operations+=2;
  }
  //y pod x->parent
  else if(x == x->parent->left)
  {
    x->parent->left = y;
    ptr_operations += 3;
  }
  else 
  {
    x->parent->right = y;
    ptr_operations += 3;
  }
  y->left = x;//x - pod y
  x->parent = y;
  ptr_operations += 2;
}


void right_rotate(tree* t, struct node* y)
{
  struct node* x = y->left;
  y->left = x->right;
  ptr_operations++;
  if(x->right != t->NILL)
  {
    x->right->parent = y;
    ptr_operations++;
  }
  ptr_operations++;
  x->parent = y->parent;
  ptr_operations++;
  if(y->parent == t->NILL)
  {
    t->root = x;
     ptr_operations+=2;
  }
  else if(y == y->parent->left)
  {
    y->parent->left = x;
     ptr_operations+=3;
  }
  else{
    y->parent->right = x;
     ptr_operations+=3;
  }
  x->right = y;
  y->parent = x;
  ptr_operations += 2;

}



void rb_insert(tree* t, struct node* z)
{
  insert(t, z);
  z->color = RED;//moze naruszyc wlasnosc 3
  ptr_operations++;
  //fixup:
  while(z->parent->color == RED)
  {
    ptr_operations++;
    struct node* y;
    if(z->parent == z->parent->parent->left)
    {
      ptr_operations++;
      y = z->parent->parent->right;
      ptr_operations++;
      if(y->color == RED)
      {
        z->parent->color = BLACK;//przypadek 1
        y->color = BLACK;
        z->parent->parent->color = RED;
        z = z->parent->parent;
        ptr_operations += 5;
      }
      else
      {
        ptr_operations++;
        if(z == z->parent->right)
        {
          z = z->parent;//przypadek 2
          ptr_operations +=2;
          left_rotate(t, z);
        }
        z->parent->color = BLACK;
        z->parent->parent->color = RED;
        ptr_operations +=2;
        right_rotate(t, z->parent->parent);
      }
    }
    else//to samo co po then z zamienionymi wskaznikami right i left
    {
        ptr_operations++;
      y = z->parent->parent->left;
      ptr_operations++;
      if(y->color == RED)
      {
        z->parent->color = BLACK;//przypadek 1
        y->color = BLACK;
        z->parent->parent->color = RED;
        z = z->parent->parent;
        ptr_operations += 5;
      }
      else
      {
        ptr_operations++;
        if(z == z->parent->left)
        {
          z = z->parent;//przypadek 2
          ptr_operations +=2;
          right_rotate(t, z);
        }
        z->parent->color = BLACK;//przypadek 3
        z->parent->parent->color = RED;
         ptr_operations +=2;
        left_rotate(t, z->parent->parent);
      }
    }
  }
  t->root->color = BLACK;
  ptr_operations++;
}



void rb_transplant(tree* t, struct node* u, struct node* v)
{
  if(u->parent == t->NILL)
  {
    t->root = v;
    ptr_operations += 2;
  }
  else if(u == u->parent->left)
  {
    u->parent->left = v;
    ptr_operations +=3;
  }
  else
  {
    u->parent->right = v;
    ptr_operations +=3;
  }
  v->parent = u->parent;
  ptr_operations++;
}


void rb_delete_fixup(tree* t, struct node* x)
{
  while(x != t->root && x->color == BLACK)
  {
    ptr_operations +=2;
    struct node* w;
    if(x == x->parent->left)
    {
      ptr_operations++;
      w = x->parent->right;
      ptr_operations++;
      if(w->color == RED)
      {
        w->color = BLACK;//przypadek 1
        x->parent->color = RED;
        left_rotate(t, x->parent);
        w = x->parent->right;
        ptr_operations += 3;
      }
      ptr_operations++;
      if(w->left->color == BLACK && w->right->color == BLACK)
      {
        w->color = RED;//przypadek 2
        x = x->parent;
        ptr_operations += 4;
      }
      else 
      {
        ptr_operations+=2;
        if(w->right->color == BLACK) 
        {
          w->left->color = BLACK;//przypadek 3
          w->color = RED;
          right_rotate(t, w);
          w = x->parent->right;
          ptr_operations += 3;
        }
        ptr_operations++;
        w->color = x->parent->color;//przypadek 4
        x->parent->color = BLACK;
        w->right->color = BLACK;
        left_rotate(t, x->parent);
        x = t->root;
        ptr_operations += 4;
      }
    }
    else//to samo co po then, ale z zamienionymi wskaznikami "right" i "left"
    {
      ptr_operations++;
      w = x->parent->left;
      ptr_operations++;
      if(w->color == RED)
      {
        w->color = BLACK;//przypadek 1
        x->parent->color = RED;
        right_rotate(t, x->parent);
        w = x->parent->left;
        ptr_operations += 3;
      }
      ptr_operations++;
      if(w->left->color == BLACK && w->right->color == BLACK)
      {
        w->color = RED;//przypadek 2
        x = x->parent;
        ptr_operations += 4;
      }
      else 
      {
        ptr_operations += 2;
        if(w->left->color == BLACK) 
        {
          w->right->color = BLACK;//przypadek 3
          w->color = RED;
          left_rotate(t, w);
          w = x->parent->left;
          ptr_operations += 3;
        }
        ptr_operations++;
        w->color = x->parent->color;//przypadek 4
        x->parent->color = BLACK;
        w->left->color = BLACK;
        right_rotate(t, x->parent);
        x = t->root;
        ptr_operations += 4;
      }
    }
  }
  x->color = BLACK;
  ptr_operations += 3;
}


void rb_delete(tree* t, struct node* z)
{
  struct node* y = z;
  struct node* x;
  bool y_original_color = y->color;
  ptr_operations++;
  if(z->left == t->NILL)
  {
    x = z->right;
    ptr_operations += 2;
    rb_transplant(t, z, z->right);
  }
  else if(z->right == t->NILL)
  {
    x = z->left;
    ptr_operations += 3;
    rb_transplant(t, z, z->left);
  }
  else
  {
    ptr_operations += 2;
    y = tree_minimum(t, z->right);
    y_original_color = y->color;
    x = y->right;
    ptr_operations += 2;
    if(y->parent == z)
    {
      x->parent = y;
      ptr_operations++;
    }
    else 
    {
      ptr_operations++;
      rb_transplant(t, y, y->right);
      y->right = z->right;
      y->right->parent = y;
      ptr_operations += 2;
    }
    rb_transplant(t, z, y);
    y->left = z->left;
    y->left->parent = y;
    y->color = z->color;
    ptr_operations += 3;
  }
  if(y_original_color == BLACK)
  {
    rb_delete_fixup(t, x);
  }
  ptr_operations++;
  free(z);
}

void rb_delete_key(tree* t, int key)
{
  struct node* node = tree_search(t, t->root, key);
  if(node != t->NILL)
  {
    rb_delete(t, node);
  }
  ptr_operations++;
}


void simulation1(int N_MIN, int N_MAX, int delta, int m)
{
    ofstream fout_bst_height;
    fout_bst_height.open("rb_height_inc.txt");
    fout_bst_height<<"n"<<" ";
    ofstream fout_bst_height_m;
    fout_bst_height_m.open("rb_height_max_inc.txt");
    fout_bst_height_m<<"n"<<" ";
    ofstream fout_bst_comp;
    fout_bst_comp.open("rb_compares_inc.txt");
    fout_bst_comp<<"n"<<" ";
    ofstream fout_bst_comp_m;
    fout_bst_comp_m.open("rb_compares_max_inc.txt");
    fout_bst_comp_m<<"n"<<" ";
    ofstream fout_bst_subs;
    fout_bst_subs.open("rb_subs_inc.txt");
    fout_bst_subs<<"n"<<" ";
    ofstream fout_bst_subs_m;
    fout_bst_subs_m.open("rb_subs_max_inc.txt");
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
            tree* my_tree = create_tree();
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
                node_ptr->left=my_tree->NILL;
                node_ptr->right=my_tree->NILL;
                node_ptr->parent=my_tree->NILL;
                rb_insert(my_tree, node_ptr);
                int h = height(my_tree, my_tree->root);
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
                rb_delete_key(my_tree, x);
                int h = height(my_tree, my_tree->root);
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
            free_tree(my_tree);
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
    fout_bst_height.open("rb_height_rand.txt");
    fout_bst_height<<"n"<<" ";
    ofstream fout_bst_height_m;
    fout_bst_height_m.open("rb_height_max_rand.txt");
    fout_bst_height_m<<"n"<<" ";
    ofstream fout_bst_comp;
    fout_bst_comp.open("rb_compares_rand.txt");
    fout_bst_comp<<"n"<<" ";
    ofstream fout_bst_comp_m;
    fout_bst_comp_m.open("rb_compares_max_rand.txt");
    fout_bst_comp_m<<"n"<<" ";
    ofstream fout_bst_subs;
    fout_bst_subs.open("rb_subs_rand.txt");
    fout_bst_subs<<"n"<<" ";
    ofstream fout_bst_subs_m;
    fout_bst_subs_m.open("rb_subs_max_rand.txt");
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
            tree* my_tree = create_tree();
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
                node_ptr->left=my_tree->NILL;
                node_ptr->right=my_tree->NILL;
                node_ptr->parent=my_tree->NILL;
                rb_insert(my_tree, node_ptr);
                int h = height(my_tree, my_tree->root);
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
                rb_delete_key(my_tree, x);
                int h = height(my_tree, my_tree->root);
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
            free_tree(my_tree);
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
