use graph::Graph;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::iter::DoubleEndedIterator;

trait StateFullGraph<N, E>: Graph<N, E> {
    fn get_state(&self, node: &N) -> bool;
    fn set_state(&mut self, node: &N, state: bool);

    fn get_component_state<'a, C>(&self, component: C) -> u32
    where
        C: Iterator<Item = &'a N>,
        N: 'a,
    {
        let mut result = 0;
        for node in component {
            result <<= 1;
            result |= self.get_state(node) as u32;
        }
        result
    }

    fn set_component_state<'a, C>(&mut self, component: C, state: u32)
    where
        C: Iterator<Item = &'a N> + DoubleEndedIterator,
        N: 'a,
    {
        let mut state = state;
        for node in component.rev() {
            self.set_state(node, (state & 1) != 0);
            state >>= 1;
        }
    }
}

impl StateFullGraph<String, String> for broadcaster::Graph {
    fn get_state(&self, node: &String) -> bool {
        self.get(node).map_or(false, |x| x.get_state())
    }

    fn set_state(&mut self, node: &String, state: bool) {
        self.get_mut(node).map(|x| x.set_state(state));
    }
}

fn main() -> std::io::Result<()> {
    let graph_str = std::fs::read_to_string("20-pulse-propagation/input.txt")?;
    let mut graph = broadcaster::parse_graph(&graph_str);

    let condensation = graph::build_condensation(graph.get_names().into_iter(), &graph);

    for (i, component) in condensation.components.iter().enumerate() {
        print!("Component #{} of size {}:", i, component.len());
        for node in component {
            print!(" {}", node);
        }
        println!();
    }

    for node in graph.get_names() {
        print!("{}:", node);
        for e in graph.outgoing_edges(node) {
            print!(" {}", graph.get_target(e));
        }
        println!();
    }

    let mut component_states = condensation
        .components
        .iter()
        .map(|_| HashMap::new())
        .collect::<Vec<_>>();

    let mut cycle_indices = condensation
        .components
        .iter()
        .map(|_| crt::CycleIndex::with_two_points(0, 0))
        .collect::<Vec<_>>();

    for epoch in 0..1_000_000 {
        if epoch != 0 {
            for (i, component) in condensation.components.iter().enumerate() {
                let state = graph.get_component_state(component.iter());
                if !component_states[i].contains_key(&state) {
                    component_states[i].insert(state, epoch);
                } else if cycle_indices[i].cycle_len == 0 {
                    cycle_indices[i] = crt::CycleIndex::with_two_points(
                        component_states[i].get(&state).map_or(0, |x| *x),
                        epoch,
                    );
                    cycle_indices[i].index = 0;
                }
            }
        }

        if cycle_indices
            .iter()
            .zip(condensation.components.iter())
            .all(|(ci, cmp)| cmp.len() <= 1 || (ci.cycle_len > 0 && ci.index > 0))
        {
            break;
        }

        run_epoch(
            condensation
                .components
                .iter()
                .map(|x| {
                    x.iter()
                        .rev()
                        .skip(1)
                        .chain(x.iter())
                        .next()
                        .map_or("".to_string(), |x| x.clone())
                })
                .collect(),
            &mut graph,
        )
        .iter()
        .zip(cycle_indices.iter_mut())
        .for_each(|(f, idx)| {
            if *f && idx.index == 0 && idx.cycle_len != 0 {
                (*idx).index = epoch + 1;
            }
        })
    }

    let big_indices = cycle_indices
        .iter()
        .zip(condensation.components.iter())
        .filter(|(_, c)| c.len() > 1)
        .map(|(i, _)| i.clone())
        .collect();

    println!("{:?}", crt::solve_chineese_remainder_theorem(big_indices));

    Ok(())
}

fn run_epoch(nodes: Vec<String>, graph: &mut broadcaster::Graph) -> Vec<bool> {
    let mut queue = VecDeque::new();
    queue.push_back(broadcaster::Command::<String> {
        source: "button".to_string(),
        destination: "broadcaster".to_string(),
        pulse: broadcaster::Pulse::Low,
    });

    let mut states = nodes.iter().map(|_| false).collect::<Vec<_>>();

    while let Some(cmd) = queue.pop_front() {
        if cmd.pulse == broadcaster::Pulse::Low {
            nodes
                .iter()
                .enumerate()
                .filter(|(i, n)| **n == cmd.source)
                .for_each(|(i, f)| states[i] = true)
        }
        if let Some(x) = graph.get_mut(&cmd.destination) {
            x.receive(cmd)
                .iter()
                .for_each(|x| queue.push_back(x.clone()));
        }
    }

    states
}
