use std::cmp::Eq;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::fmt::Display;
use std::hash::Hash;

#[derive(Debug, PartialEq, Clone)]
pub enum Pulse {
    Low,
    High,
}

impl Display for Pulse {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if *self == Pulse::Low {
            write!(f, "low")
        } else {
            write!(f, "high")
        }
    }
}

#[derive(Debug, PartialEq, Clone)]
pub struct Command<Tag> {
    pub source: Tag,
    pub destination: Tag,
    pub pulse: Pulse,
}

impl<Tag: Display> Display for Command<Tag> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} -{}-> {}", self.source, self.pulse, self.destination)
    }
}

pub trait Broadcaster<Tag> {
    fn receive<'a>(&'a mut self, command: Command<Tag>) -> Vec<Command<Tag>>;

    fn get_state(&self) -> bool {
        false
    }
    fn set_state(&mut self, state: bool) {}

    fn add_inbound(&mut self, _other: Tag) {}
    fn add_outbound(&mut self, _other: Tag) {}
}

struct SimpleBroadcaster<Tag> {
    outbounds: Vec<Tag>,
}

impl<Tag> SimpleBroadcaster<Tag> {
    fn new() -> Self {
        Self {
            outbounds: Vec::new(),
        }
    }
}

impl<Tag: Clone> Broadcaster<Tag> for SimpleBroadcaster<Tag> {
    fn receive(&mut self, command: Command<Tag>) -> Vec<Command<Tag>> {
        self.outbounds
            .iter()
            .map(|x| Command {
                source: command.destination.clone(),
                destination: x.clone(),
                pulse: command.pulse.clone(),
            })
            .collect()
    }

    fn add_outbound(&mut self, other: Tag) {
        self.outbounds.push(other)
    }
}

struct FlipFlopBroadcaster<Tag> {
    outbounds: Vec<Tag>,
    state: bool,
}

impl<Tag> FlipFlopBroadcaster<Tag> {
    fn new() -> Self {
        Self {
            outbounds: Vec::new(),
            state: false,
        }
    }
}

impl<Tag: Clone> Broadcaster<Tag> for FlipFlopBroadcaster<Tag> {
    fn get_state(&self) -> bool {
        self.state
    }

    fn set_state(&mut self, state: bool) {
        self.state = state;
    }

    fn receive(&mut self, command: Command<Tag>) -> Vec<Command<Tag>> {
        if command.pulse == Pulse::High {
            Vec::new()
        } else {
            self.state = !self.state;
            self.outbounds
                .iter()
                .map(|x| Command {
                    source: command.destination.clone(),
                    destination: x.clone(),
                    pulse: {
                        if self.state {
                            Pulse::High
                        } else {
                            Pulse::Low
                        }
                    },
                })
                .collect()
        }
    }

    fn add_outbound(&mut self, other: Tag) {
        self.outbounds.push(other)
    }
}

struct ConjunctionBroadcaster<Tag: Eq + Hash> {
    inbounds: HashMap<Tag, Pulse>,
    outbounds: Vec<Tag>,
}

impl<Tag: Eq + Hash> ConjunctionBroadcaster<Tag> {
    fn new() -> Self {
        Self {
            inbounds: HashMap::new(),
            outbounds: Vec::new(),
        }
    }
}

impl<Tag: Eq + Hash + Clone> Broadcaster<Tag> for ConjunctionBroadcaster<Tag> {
    fn add_inbound(&mut self, other: Tag) {
        self.inbounds.insert(other, Pulse::Low);
    }
    fn add_outbound(&mut self, other: Tag) {
        self.outbounds.push(other);
    }

    fn receive(&mut self, command: Command<Tag>) -> Vec<Command<Tag>> {
        if let Some(x) = self.inbounds.get_mut(&command.source) {
            *x = command.pulse;
        }
        let result = {
            if self.inbounds.iter().any(|(_, f)| *f == Pulse::Low) {
                Pulse::High
            } else {
                Pulse::Low
            }
        };
        self.outbounds
            .iter()
            .map(|x| Command {
                source: command.destination.clone(),
                destination: x.clone(),
                pulse: result.clone(),
            })
            .collect()
    }
}

pub struct Graph {
    broadcaster: SimpleBroadcaster<String>,
    flip_flops: HashMap<String, FlipFlopBroadcaster<String>>,
    conjunctions: HashMap<String, ConjunctionBroadcaster<String>>,
    adjacency_list: HashMap<String, Vec<String>>,
}

impl Graph {
    fn new() -> Self {
        Self {
            broadcaster: SimpleBroadcaster::new(),
            flip_flops: HashMap::new(),
            conjunctions: HashMap::new(),
            adjacency_list: HashMap::new(),
        }
    }

    fn create_flip_flop(&mut self, name: &str) {
        self.flip_flops
            .insert(name.to_string(), FlipFlopBroadcaster::new());
    }

    fn create_conjunction(&mut self, name: &str) {
        self.conjunctions
            .insert(name.to_string(), ConjunctionBroadcaster::new());
    }

    pub fn get_names(&self) -> Vec<String> {
        let mut res = vec!["broadcaster".to_string()];
        res.extend(self.flip_flops.keys().map(|x| x.clone()));
        res.extend(self.conjunctions.keys().map(|x| x.clone()));
        res
    }

    pub fn get<'a>(&'a self, name: &str) -> Option<&'a dyn Broadcaster<String>> {
        if name == "broadcaster" {
            Some(&self.broadcaster)
        } else if let Some(x) = self.flip_flops.get(name) {
            Some(x)
        } else if let Some(x) = self.conjunctions.get(name) {
            Some(x)
        } else {
            None
        }
    }

    pub fn get_mut<'a>(&'a mut self, name: &str) -> Option<&'a mut dyn Broadcaster<String>> {
        if name == "broadcaster" {
            Some(&mut self.broadcaster)
        } else if let Some(x) = self.flip_flops.get_mut(name) {
            Some(x)
        } else if let Some(x) = self.conjunctions.get_mut(name) {
            Some(x)
        } else {
            None
        }
    }

    fn connect<'a>(&'a mut self, lhs: &str, rhs: &str) -> Option<()> {
        let x = self.get_mut(lhs)?;
        x.add_outbound(rhs.to_string());

        let y = self.get_mut(rhs)?;
        y.add_inbound(lhs.to_string());

        if !self.adjacency_list.contains_key(lhs) {
            self.adjacency_list.insert(lhs.to_string(), Vec::new());
        }

        self.adjacency_list
            .get_mut(lhs)
            .map(|links| links.push(rhs.to_string()));

        Some(())
    }
}

impl graph::Graph<String, String> for Graph {
    fn outgoing_edges(&self, node: String) -> Vec<String> {
        self.adjacency_list
            .get(&node)
            .map_or(Vec::new(), |x| x.clone())
    }

    fn get_target(&self, edge: String) -> String {
        edge
    }
}

#[derive(PartialEq, Debug)]
pub struct Stats {
    lows: usize,
    highs: usize,
}

impl Stats {
    pub fn new() -> Self {
        Self { lows: 0, highs: 0 }
    }
    pub fn value(&self) -> u64 {
        (self.lows as u64) * (self.highs as u64)
    }
}

impl std::ops::AddAssign for Stats {
    fn add_assign(&mut self, other: Self) {
        *self = Self {
            lows: self.lows + other.lows,
            highs: self.highs + other.highs,
        }
    }
}

pub fn run_epoch(graph: &mut Graph) -> Stats {
    let mut stats = Stats { lows: 0, highs: 0 };
    let mut queue = VecDeque::new();
    queue.push_back(Command::<String> {
        source: "button".to_string(),
        destination: "broadcaster".to_string(),
        pulse: Pulse::Low,
    });

    while let Some(cmd) = queue.pop_front() {
        if cmd.pulse == Pulse::Low {
            stats.lows += 1;
        } else {
            stats.highs += 1;
        }
        if let Some(x) = graph.get_mut(&cmd.destination) {
            x.receive(cmd)
                .iter()
                .for_each(|x| queue.push_back(x.clone()));
        }
    }

    stats
}

pub fn parse_graph(text: &str) -> Graph {
    let nodes = text
        .split('\n')
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
        .filter_map(|line| line.split(' ').next())
        .collect::<Vec<_>>();

    let mut graph = Graph::new();
    for node in nodes {
        match &node[..1] {
            "b" => {}
            "%" => graph.create_flip_flop(&node[1..]),
            "&" => graph.create_conjunction(&node[1..]),
            _ => println!("something weird happened with node: {}", node),
        }
    }

    for line in text
        .split('\n')
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
    {
        let mut node_links = line.split("->");

        let node = {
            let node = node_links.next().unwrap().trim();
            if &node[..1] == "%" || &node[..1] == "&" {
                &node[1..]
            } else {
                node
            }
        };

        for link in node_links.next().unwrap().split(',').map(|x| x.trim()) {
            graph.connect(node, link);
        }
    }

    graph
}
