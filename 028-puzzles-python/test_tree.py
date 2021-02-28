# BST 
class TreeNode: 
  def __init__(self,key): 
    self.left = None
    self.right = None
    self.val = key 


# For Facebook's query
class Node: 
  def __init__(self, data): 
    self.val = data 
    self.children = []


def test_count_visible__left_nodes():
  def visible_nodes(root):
    # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=495004218121393
    # 
    # hint: leftmost node on each level may be right node

    num_visible_left = 0
    num_visible_right = 0
    if root.left is not None:
      num_visible_left = visible_nodes(root.left)
    if root.right is not None:
      num_visible_right = visible_nodes(root.right)
    return 1+max(num_visible_left, num_visible_right)


  # Test
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  assert visible_nodes(root_1) == 4

  root_2 = TreeNode(10)
  root_2.left = TreeNode(8)
  root_2.right = TreeNode(15)
  root_2.left.left = TreeNode(4)
  root_2.left.left.right = TreeNode(5)
  root_2.left.left.right.right = TreeNode(6)
  root_2.right.left =TreeNode(14)
  root_2.right.right = TreeNode(16)
  assert visible_nodes(root_2) == 5


def test_flatten_tree_to_list():
  # REF: https://leetcode.com/problems/flatten-binary-tree-to-linked-list/
  def flatten(tree):
    vec = [tree.val]
    if tree.left is not None:
      vec = flatten(tree.left) + vec
    if tree.right is not None:
      vec = vec + flatten(tree.right)
    return vec



  # Test
  #             8
  #           /   \
  #          3     10
  #         / \      \    
  #        1   6     14
  #           / \    /
  #          4   7  13
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  assert flatten(root_1) == [1,3,4,6,7,8,10,13,14]


def test_right_side_view():
  # REF: https://leetcode.com/problems/binary-tree-right-side-view/
  def right_view(tree):
    vec = []
    proj = project_right(tree, weight=1, current_depth=0, proj={})
    for level, node in proj.items():
      w,val = node
      vec.append(val)
    return vec

  def project_right(tree, weight, current_depth, proj):
    if current_depth not in proj:
      proj[current_depth] = (weight, tree.val)
    else:
      w,a = proj[current_depth]
      if weight>w:
        proj[current_depth] = (weight, tree.val)

    # DFS to right first
    if tree.right is not None:
      proj = project_right(tree.right, weight<<1, current_depth+1, proj) 

    # DFS to left afterwards
    if tree.left is not None:
      proj = project_right(tree.left, weight, current_depth+1, proj)

    return proj

  # Test
  #             8
  #           /   \
  #          3     10
  #         / \      \    
  #        1   6     14
  #           / \    /
  #          4   7  13
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  assert right_view(root_1) == [8,10,14,13]

  # Test
  #             10
  #            /  \
  #           8    15
  #          /    /  \
  #         4    14   16
  #          \
  #           5
  #            \
  #             6
  root_2 = TreeNode(10)
  root_2.left = TreeNode(8)
  root_2.right = TreeNode(15)
  root_2.left.left = TreeNode(4)
  root_2.left.left.right = TreeNode(5)
  root_2.left.left.right.right = TreeNode(6)
  root_2.right.left =TreeNode(14)
  root_2.right.right = TreeNode(16)
  assert right_view(root_2) == [10,15,16,5,6]


def test_count_char_nodes():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=3068294883205371

  #           1(a)
  #         /   \
  #       2(b)  3(a)

  # s = "aba"
  # RootNode = 1
  # query = [[1, 'a']]  ==> output = [2]

  # Note: 
  # Node 1 corresponds to first letter 'a', 
  # Node 2 corresponds to second letter of the string 'b', 
  # Node 3 corresponds to third letter of the string 'a'.

  # Both Node 1 and Node 3 contain 'a', 
  # so the number of nodes within the subtree of Node 1 containing 'a' 
  # is 2.

  
  def count_of_nodes(root, queries, s):
    ans = []
    for q in queries:
      ans.append(query(root, q, s))
    return ans

  def query(root, query, s):
    u,c = query
    # Find all possible 'val' of [c] in [s]
    vals = [i+1 for k,i in zip(s,range(len(s))) if k==c]
    print(vals)
    return find_in_tree(root, u, vals)

  def find_in_tree(root, u, vals):
    # Locate children of value=u and start finding from its subtrees
    if root.val==u:
      return find_in_subtree(root, vals)
    else:
      ans = 0
      for child in root.children:
        ans += find_in_tree(child, u, vals)
      return ans

  def find_in_subtree(root, vals):
    # Also count root itself if it's the right value we're looking for
    ans = 1 if root.val in vals else 0
    for child in root.children:
      if child.val in vals:
        ans += 1
      # Dig deeper too
      for grandchild in child.children:
        ans += find_in_subtree(grandchild, vals)
    return ans

  # Testcase 1
  n_1 ,q_1 = 3, 1 
  s_1 = "aba"
  root_1 = Node(1) 
  root_1.children.append(Node(2)) 
  root_1.children.append(Node(3)) 
  queries_1 = [(1, 'a')]

  output_1 = count_of_nodes(root_1, queries_1, s_1)
  expected_1 = [2]
  assert expected_1 == output_1

  # Testcase 2
  n_2 ,q_2 = 7, 3 
  s_2 = "abaacab"
  root_2 = Node(1)
  root_2.children.append(Node(2))
  root_2.children.append(Node(3))
  root_2.children.append(Node(7))
  root_2.children[0].children.append(Node(4))
  root_2.children[0].children.append(Node(5))
  root_2.children[1].children.append(Node(6))
  queries_2 = [(1, 'a'),(2, 'b'),(3, 'a')]
  output_2 = count_of_nodes(root_2, queries_2, s_2)
  expected_2 = [4, 1, 2]
  assert expected_2 == output_2


