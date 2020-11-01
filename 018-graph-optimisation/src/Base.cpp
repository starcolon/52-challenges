#include "Base.hpp"

Graph::Graph(){

}

Graph::~Graph(){

}

bool Graph::addNode(string value, double cost){
  if (this->nodes.find(value) == this->nodes.end()){
    Node n {.value = value, .cost = cost };
    this->nodes.insert_or_assign(value, n);
    return true;
  }
  else return false;
}

bool Graph::delNode(string value){
  auto it = this->nodes.find(value);
  if (it == this->nodes.end()){
    return false;
  }
  else {
    // Delete the node from map registry
    this->nodes.erase(it);
    return true;
  }
}

bool Graph::addEdge(string from, string to, double cost){
  // NOTE: Will update if already exists
  auto itFrom = this->nodes.find(from);
  auto itTo = this->nodes.find(to);

  if ((itFrom == this->nodes.end()) || (itTo == this->nodes.end())){
    // Either end of the edge does not exist
    return false;
  }
  else {
    (*itFrom).second.edges.insert_or_assign(to, cost);
    return true;
  }
}

bool Graph::setNodeCost(string node, double cost){
  auto n = this->nodes.find(node);
  if (n != this->nodes.end()){
    n->second.cost = cost;
  }
  else return false;
}

int Graph::numNodes() const{
  return this->nodes.size();
}

int Graph::numEdges() const{
  int num = 0;
  for (auto& n : this->nodes){
    for (auto& e : n.second.edges){
      // Only count valid edges
      auto to = e.first;
      if (this->nodes.find(to) != this->nodes.end()){
        num++;
      }
    }
  }
  return num;
}

vector<string> Graph::getNodes() const{
  vector<string> v;
  for (auto& n : this->nodes){
    v.push_back(n.first);
  }
  return v;
}

map<string, double> Graph::getEdges(string from) const {
  map<string, double> edges;
  auto node = this->nodes.find(from);
  if (node != this->nodes.end()){
    for (auto& e : node->second.edges){
      // Only take valid edges
      auto to = e.first;
      if (this->nodes.find(to) != this->nodes.end()){
        edges.insert_or_assign(to, e.second);
      }
    }
  }
  return edges;
}

optional<Node> Graph::getNode(string node) const {
  auto n = this->nodes.find(node);
  if (n != this->nodes.end()){
    return { n->second };
  }
  else return nullopt;
}

priority_queue<
  NodeInt,
  vector<NodeInt>, 
  NodeIntDesc> 
Graph::mostOutbounds() const {
  priority_queue<
    NodeInt,
    vector<NodeInt>,
    NodeIntDesc> q;
  for (auto& n : this->nodes){
    int numOutflow = this->getEdges(n.first).size();
    q.push(make_tuple(n.first, numOutflow));
  }
  return q;
}

priority_queue<
  NodeInt,
  vector<NodeInt>, 
  NodeIntDesc> 
Graph::mostInbounds() const {
  priority_queue<
    NodeInt,
    vector<NodeInt>,
    NodeIntDesc> q;

  map<string, int> bounds;

  for (auto& n : this->nodes){
    for (auto& e : this->getEdges(n.first)){
      auto dest = e.first;
      auto b = bounds.find(dest);
      if (b != bounds.end()){
        bounds.insert_or_assign(dest, b->second+1);
      }
      else bounds.insert_or_assign(dest, 1);
    }
  }

  for (auto& b : bounds){
    q.push(make_tuple(b.first, b.second));
  }

  return q;
}

bool Graph::hasCycle(vector<string> nodes) const {
  // Detect if the selected nodes conform a cycle

}
