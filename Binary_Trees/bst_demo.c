//Jan Poreba
#include <stdio.h>
#include <stdlib.h>



struct node{
  struct node *parent;
  struct node *left;
  struct node *right;
  int element;
};


struct node* root = NULL;



void insert( struct node** root, struct node* z )
{
  if( z==NULL) return;
  struct node* y = NULL;
  struct node* x = *root;
  while(x != NULL)
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
  if(y==NULL)
  {
    *root = z;
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
  }
  return x;
}


struct node* stree_successor(struct node* x)
{
  if(x->right != NULL)
  {
    return tree_minimum(x->right);
  }
  struct node* y = x->parent;
  while(y != NULL && x==y->right)
  {
    x = y;
    y = y->parent;
  }
  return y;
}


void transplant(struct node** root, struct node* u, struct node* v)
{
  if(u->parent == NULL)
  {
    *root = v;
  }
  else if(u == u->parent->left)
  {
    u->parent->left = v;
  }
  else 
  {
    u->parent->right = v;
  }
  if(v != NULL)
  {
    v->parent = u->parent;
  }
}



void tree_delete(struct node** root, struct node* z)
{
  if(z->left == NULL)
  {
    transplant(root, z, z->right);
  }
  else if(z->right == NULL)
  {
    transplant(root, z, z->left);
  }
  else 
  {
    struct node* y = tree_minimum(z->right);
    if(y->parent != z)
    {
      transplant(root, y, y->right);
      y->right = z->right;
      y->right->parent = y;
    }
    transplant(root, z, y);
    y->left = z->left;
    y->left->parent = y;
  }
  free(z);
}


struct node* tree_search(struct node* x, int key)
{
  while(x != NULL && key != x->element)
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


void delete_key(struct node** root, int key)
{
  struct node* node = tree_search(*root, key);
  if(node != NULL)
  {
    tree_delete(root, node);
  }
  
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


// global variables used in `print_BST`
char* left_trace; // needs to be allocaded with size
char* right_trace; // needs to be allocaded with size



void print_BST( struct node * root, int depth,char prefix){
  if( root == NULL ) return;
  if( root->left != NULL ){
    print_BST(root->left, depth+1, '/');
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
  printf("[%d]\n", root->element);
  left_trace[depth]=' ';
  if( root->right != NULL ){
    right_trace[depth]='|';
    print_BST(root->right, depth+1, '\\');
  }
}



int main(){

  int size=20;
  printf("input size: ");
  scanf("%d", &size);
  printf("size = %d\n", size);

  left_trace=(char*) malloc( size*sizeof(char) );
  right_trace=(char*) malloc( size*sizeof(char) );
  for(int i=0; i<=size; i++){
    left_trace[i]=' ';
    left_trace[i]=' ';
  }
  
  printf("\n");
  
  for(int i=0; i<size; i++){
    struct node * node_ptr = malloc( sizeof(struct node));
    printf("height: %d\n", height(&root));
    int element;
    scanf("%d", &element);
    node_ptr->element = element;
    node_ptr->left=NULL;
    node_ptr->right=NULL;
    node_ptr->parent=NULL;
    printf("INSERT: [%d]\n\n", node_ptr->element);
    insert(&root, node_ptr );
    printf("TREE:\n");
    print_BST(root, 0, '-');
    printf("height: %d\n", height(&root));
    printf("\n\n");
  }


   for(int i=0; i<size; i++){
    printf("height: %d\n", height(&root));
    int key;
    scanf("%d", &key);
    printf("DELETE: [%d]\n\n", key);
    delete_key(&root, key);
    printf("TREE:\n");
    print_BST(root, 0, '-');
    printf("height: %d\n", height(&root));
    printf("\n\n");
  }

  free(left_trace);
  free(right_trace);
  delete_tree(&root);
}




