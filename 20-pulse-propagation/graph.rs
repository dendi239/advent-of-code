use std::clone::Clone;
use std::cmp::Eq;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fmt::Debug;
use std::hash::Hash;
use std::marker::PhantomData;
use std::vec::Vec;

pub trait Graph<Node, Edge> {
    fn get_target(&self, edge: Edge) -> Node;
    fn outgoing_edges(&self, node: Node) -> Vec<Edge>;
}

pub struct Condensation<Node> {
    pub components: Vec<Vec<Node>>,
    pub node_to_component: HashMap<Node, usize>,
}

struct RevGraph<Node>
where
    Node: Eq + Hash + Clone,
{
    adj_list: HashMap<Node, Vec<Node>>,
}

impl<N> RevGraph<N>
where
    N: Eq + Hash + Clone,
{
    fn new<E, G, C>(nodes: C, g: &G) -> Self
    where
        G: Graph<N, E>,
        C: Iterator<Item = N>,
    {
        let mut adj_list = HashMap::new();
        for node in nodes {
            for e in g.outgoing_edges(node.clone()) {
                let n = g.get_target(e);
                if !adj_list.contains_key(&n) {
                    adj_list.insert(n.clone(), Vec::new());
                }
                if let Some(xs) = adj_list.get_mut(&n) {
                    xs.push(node.clone());
                }
            }
        }
        RevGraph { adj_list }
    }
}

impl<N> Graph<N, N> for RevGraph<N>
where
    N: Eq + Hash + Clone,
{
    fn get_target(&self, edge: N) -> N {
        edge
    }

    fn outgoing_edges(&self, node: N) -> Vec<N> {
        self.adj_list.get(&node).map_or(Vec::new(), |x| x.clone())
    }
}

impl<N> Condensation<N>
where
    N: Eq + Hash + Clone,
{
    fn new() -> Condensation<N> {
        Self {
            components: Vec::new(),
            node_to_component: HashMap::new(),
        }
    }

    fn add_component(&mut self, component: Vec<N>) {
        for node in component.iter() {
            self.node_to_component
                .insert(node.clone(), self.components.len());
        }
        self.components.push(component);
    }
}

trait DFSVisitor<Node> {
    fn on_enter(&mut self, _node: &Node) {}
    fn on_edge(&mut self, _from: &Node, _to: &Node) {}
    fn on_exit(&mut self, _node: &Node) {}
}

enum Action<Node> {
    Enter(Node),
    Exit(Node),
}

struct DepthFirstSearcher<'a, N, E, G>
where
    N: Hash + Eq,
    G: Graph<N, E>,
{
    queue: Vec<Action<N>>,
    graph: &'a G,
    used: HashSet<N>,
    phantom: PhantomData<E>,
}

impl<'a, N, E, G> DepthFirstSearcher<'a, N, E, G>
where
    N: Hash + Eq + Clone,
    G: Graph<N, E>,
{
    fn new(graph: &'a G) -> Self {
        Self {
            queue: Vec::new(),
            graph,
            used: HashSet::new(),
            phantom: PhantomData::default(),
        }
    }

    fn enter<V>(&mut self, node: &N, visitor: &mut V)
    where
        V: DFSVisitor<N>,
    {
        if self.used.contains(node) {
            return;
        }

        self.used.insert(node.clone());
        visitor.on_enter(node);
        self.queue.push(Action::Exit(node.clone()));

        for e in self.graph.outgoing_edges(node.clone()) {
            let n = self.graph.get_target(e);
            visitor.on_edge(node, &n);
            self.queue.push(Action::Enter(n));
        }
    }

    fn exit<V>(&mut self, node: &N, visitor: &mut V)
    where
        V: DFSVisitor<N>,
    {
        visitor.on_exit(node);
    }

    fn seen(&self, node: &N) -> bool {
        self.used.contains(node)
    }

    fn visit<V>(&mut self, node: &N, visitor: &mut V)
    where
        V: DFSVisitor<N>,
    {
        self.queue.push(Action::Enter(node.clone()));
        while let Some(action) = self.queue.pop() {
            match action {
                Action::Enter(node) => self.enter(&node, visitor),
                Action::Exit(node) => self.exit(&node, visitor),
            }
        }
    }
}

fn depth_first_search<N, E, G, C, V>(nodes: C, graph: &G, visitor: &mut V)
where
    N: Hash + Eq + Clone,
    G: Graph<N, E>,
    C: Iterator<Item = N>,
    V: DFSVisitor<N>,
{
    let mut dfs = DepthFirstSearcher::new(graph);
    for node in nodes {
        dfs.visit(&node, visitor);
    }
}

struct ExitOrderBuilder<'a, Node> {
    order: &'a mut Vec<Node>,
}

impl<Node> DFSVisitor<Node> for ExitOrderBuilder<'_, Node>
where
    Node: Clone,
{
    fn on_exit(&mut self, node: &Node) {
        self.order.push(node.clone())
    }
}

pub fn build_condensation<N, E, G, C>(nodes: C, graph: &G) -> Condensation<N>
where
    N: Hash + Eq + Clone + Debug,
    G: Graph<N, E>,
    C: Iterator<Item = N>,
{
    let mut exit_order = Vec::new();
    depth_first_search(
        nodes,
        graph,
        &mut ExitOrderBuilder {
            order: &mut exit_order,
        },
    );
    exit_order.reverse();
    println!("exit order: {:?}", exit_order);

    let rev_graph = RevGraph::new(exit_order.clone().into_iter(), graph);
    let mut condensation = Condensation::new();
    let mut current_component = Vec::new();
    let mut dfs = DepthFirstSearcher::<N, N, RevGraph<N>>::new(&rev_graph);

    for node in exit_order {
        if !dfs.seen(&node) {
            current_component.clear();
            dfs.visit(
                &node,
                &mut ExitOrderBuilder {
                    order: &mut current_component,
                },
            );
            condensation.add_component(current_component.clone());
        }
    }

    condensation
}
