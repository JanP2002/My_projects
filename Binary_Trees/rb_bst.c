//Jan Poreba
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


const bool RED = true;
const bool BLACK = false;
const char* ANSI_RED = "\033[0;31m";
const char *ANSI_RESET = "\033[0m";


struct node{
  struct node *parent;
  struct node *left;
  struct node *right;
  int element;
  bool color;
};


typedef struct tree{
  struct node* root;
  struct node* NILL;
} tree;



tree* create_tree()
{
  tree* t = malloc(sizeof(tree));
  t->NILL = malloc(sizeof(struct node));
  t->NILL->color = BLACK;
  t->NILL->left = NULL;
  t->NILL->right = NULL;
  t->root = t->NILL;
  return t;
}







void insert(tree* t, struct node* z)
{
  if( z==NULL || z== t->NILL) return;
  struct node* y = t->NILL;
  struct node* x = t->root;
  while(x != t->NILL)
  {
    y = x;
    if(z->element < x->element)
    {
      x=x->left;
    }
    else
    {
      x=x->right;
    }
  }
  z->parent=y;
  if(y==t->NILL)
  {
    t->root = z;
  }
  else if(z->element < y->element)
  {
    y->left = z;
  }
  else
  {
    y->right = z;
  }

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
  }
  return x;
}


struct node* tree_successor(tree* t, struct node* x)
{
  if(x->right != t->NILL)
  {
    return tree_minimum(t, x->right);
  }
  struct node* y = x->parent;
  while(y != t->NILL && x==y->right)
  {
    x = y;
    y = y->parent;
  }
  return y;
}



struct node* tree_search(tree* t, struct node* x, int key)
{
  while(x != t->NILL && key != x->element)
  {
    if(key < x->element)
    {
      x = x->left;
    }
    else
    {
      x = x->right;
    }
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


// global variables used in `print_BST`
char* left_trace; // needs to be allocaded with size
char* right_trace; // needs to be allocaded with size



void print_RB_TREE(tree* t, struct node* subtree, int depth, char prefix){
  if( t == NULL || subtree == t->NILL || subtree == NULL) return;
  if( subtree->left != t->NILL ){
    print_RB_TREE(t, subtree->left, depth+1, '/');
  }
  if(prefix == '/') left_trace[depth-1]='|';
  if(prefix == '\\') right_trace[depth-1]=' ';
  if( depth==0) printf("-");
  if( depth>0) printf(" ");
  for(int i=0; i<depth-1; i++)
    if( left_trace[i]== '|' || right_trace[i]=='|' ) {
      printf("| ");
    } else {
      printf("  ");
    }
  if( depth>0 ) printf("%c-", prefix);
  if(subtree->color == RED)
  {
    printf("%s[%d]%s\n", ANSI_RED, subtree->element, ANSI_RESET);
  }
  else
  {
     printf("[%d]\n", subtree->element);
  }
  left_trace[depth]=' ';
  if( subtree->right != t->NILL ){
    right_trace[depth]='|';
    print_RB_TREE(t, subtree->right, depth+1, '\\');
  }
}


void left_rotate(tree* t, struct node* x)
{
  struct node* y= x->right;//y bedzie podnoszony
  x->right = y->left;//poddrzewo beta - pod x
  if(y->left != t->NILL)
  {
    y->left->parent = x;//popraw parent[korzen beta]
  }
  y->parent = x->parent;//byly ojciec x bedzie ojcem y
  if(x->parent == t->NILL)
  {
    t->root = y;//y - nowy korzen t
  }
  //y pod x->parent
  else if(x == x->parent->left)
  {
    x->parent->left = y;
  }
  else 
  {
    x->parent->right = y;
  }
  y->left = x;//x - pod y
  x->parent = y;
}


void right_rotate(tree* t, struct node* y)
{
  struct node* x = y->left;
  y->left = x->right;
  if(x->right != t->NILL)
  {
    x->right->parent = y;
  }
  x->parent = y->parent;
  if(y->parent == t->NILL)
  {
    t->root = x;
  }
  else if(y == y->parent->left)
  {
    y->parent->left = x;
  }
  else{
    y->parent->right = x;
  }
  x->right = y;
  y->parent = x;

}



void rb_insert(tree* t, struct node* z)
{
  insert(t, z);
  z->color = RED;//moze naruszyc wlasnosc 3
  //fixup:
  while(z->parent->color == RED)
  {
    struct node* y;
    if(z->parent == z->parent->parent->left)
    {
      y = z->parent->parent->right;
      if(y->color == RED)
      {
        z->parent->color = BLACK;//przypadek 1
        y->color = BLACK;
        z->parent->parent->color = RED;
        z = z->parent->parent;
      }
      else
      {
        if(z == z->parent->right)
        {
          z = z->parent;//przypadek 2
          left_rotate(t, z);
        }
        z->parent->color = BLACK;
        z->parent->parent->color = RED;
        right_rotate(t, z->parent->parent);
      }
    }
    else//to samo co po then z zamienionymi wskaznikami right i left
    {
      y = z->parent->parent->left;
      if(y->color == RED)
      {
        z->parent->color = BLACK;//przypadek 1
        y->color = BLACK;
        z->parent->parent->color = RED;
        z = z->parent->parent;
      }
      else
      {
        if(z == z->parent->left)
        {
          z = z->parent;//przypadek 2
          right_rotate(t, z);
        }
        z->parent->color = BLACK;//przypadek 3
        z->parent->parent->color = RED;
        left_rotate(t, z->parent->parent);
      }
    }
  }
  t->root->color = BLACK;
}



void rb_transplant(tree* t, struct node* u, struct node* v)
{
  if(u->parent == t->NILL)
  {
    t->root = v;
  }
  else if(u == u->parent->left)
  {
    u->parent->left = v;
  }
  else
  {
    u->parent->right = v;
  }
  v->parent = u->parent;
}


void rb_delete_fixup(tree* t, struct node* x)
{
  while(x != t->root && x->color == BLACK)
  {
    struct node* w;
    if(x == x->parent->left)
    {
      w = x->parent->right;
      if(w->color == RED)
      {
        w->color = BLACK;//przypadek 1
        x->parent->color = RED;
        left_rotate(t, x->parent);
        w = x->parent->right;
      }
      if(w->left->color == BLACK && w->right->color == BLACK)
      {
        w->color = RED;//przypadek 2
        x = x->parent;
      }
      else 
      {
        if(w->right->color == BLACK) 
        {
          w->left->color = BLACK;//przypadek 3
          w->color = RED;
          right_rotate(t, w);
          w = x->parent->right;
        }
        w->color = x->parent->color;//przypadek 4
        x->parent->color = BLACK;
        w->right->color = BLACK;
        left_rotate(t, x->parent);
        x = t->root;
      }
    }
    else//to samo co po then, ale z zamienionymi wskaznikami "right" i "left"
    {
      w = x->parent->left;
      if(w->color == RED)
      {
        w->color = BLACK;//przypadek 1
        x->parent->color = RED;
        right_rotate(t, x->parent);
        w = x->parent->left;
      }
      if(w->left->color == BLACK && w->right->color == BLACK)
      {
        w->color = RED;//przypadek 2
        x = x->parent;
      }
      else 
      {
        if(w->left->color == BLACK) 
        {
          w->right->color = BLACK;//przypadek 3
          w->color = RED;
          left_rotate(t, w);
          w = x->parent->left;
        }
        w->color = x->parent->color;//przypadek 4
        x->parent->color = BLACK;
        w->left->color = BLACK;
        right_rotate(t, x->parent);
        x = t->root;
      }
    }
  }
  x->color = BLACK;
}


void rb_delete(tree* t, struct node* z)
{
  struct node* y = z;
  struct node* x;
  bool y_original_color = y->color;
  if(z->left == t->NILL)
  {
    x = z->right;
    rb_transplant(t, z, z->right);
  }
  else if(z->right == t->NILL)
  {
    x = z->left;
    rb_transplant(t, z, z->left);
  }
  else
  {
    y = tree_minimum(t, z->right);
    y_original_color = y->color;
    x = y->right;
    if(y->parent == z)
    {
      x->parent = y;
    }
    else 
    {
      rb_transplant(t, y, y->right);
      y->right = z->right;
      y->right->parent = y;
    }
    rb_transplant(t, z, y);
    y->left = z->left;
    y->left->parent = y;
    y->color = z->color;
  }
  if(y_original_color == BLACK)
  {
    rb_delete_fixup(t, x);
  }
  free(z);
}

void rb_delete_key(tree* t, int key)
{
  struct node* node = tree_search(t, t->root, key);
  if(node != t->NILL)
  {
    rb_delete(t, node);
  }
}

int main(){

  tree* my_tree = create_tree();
  int size;
  printf("input size: ");
  scanf("%d", &size);
  printf("size = %d\n", size);

  // init traces
  left_trace=(char*) malloc( size*sizeof(char) );
  right_trace=(char*) malloc( size*sizeof(char) );
  for(int i=0; i<=size; i++){
    left_trace[i]=' ';
    left_trace[i]=' ';
  }
  
  printf("\n");
  
  for(int i=0; i<size; i++){
    struct node * node_ptr = malloc( sizeof(struct node));
    printf("height: %d\n", height(my_tree, my_tree->root));
    int element;
    scanf("%d", &element);
    node_ptr->element = element;
    node_ptr->left=my_tree->NILL;
    node_ptr->right=my_tree->NILL;
    node_ptr->parent=my_tree->NILL;
    printf("INSERT: [%d]\n\n", node_ptr->element);
    rb_insert(my_tree, node_ptr );
    printf("TREE:\n");
    print_RB_TREE(my_tree, my_tree->root, 0, '-');
    printf("height: %d\n", height(my_tree, my_tree->root));
    printf("\n\n");
  }


   for(int i=0; i<size; i++){
    printf("height: %d\n", height(my_tree, my_tree->root));
    int key;
    scanf("%d", &key);
    printf("DELETE: [%d]\n\n", key);
    rb_delete_key(my_tree, key);
    printf("TREE:\n");
    print_RB_TREE(my_tree, my_tree->root, 0, '-');
    printf("height: %d\n", height(my_tree, my_tree->root));
    printf("\n\n");
  }

  free(left_trace);
  free(right_trace);
  free_tree(my_tree);

}




