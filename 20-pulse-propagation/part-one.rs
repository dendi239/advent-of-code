fn main() -> std::io::Result<()> {
    let graph_str = std::fs::read_to_string("20-pulse-propagation/input.txt")?;
    let mut graph = broadcaster::parse_graph(&graph_str);
    let mut stats = broadcaster::Stats::default();
    for _ in 0..1_000 {
        stats += broadcaster::run_epoch(&mut graph);
    }
    println!("{}", stats.value());
    Ok(())
}
