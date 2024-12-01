#[derive(Debug, Clone, Copy, PartialEq)]
enum Tile {
    Garden,
    Rock,
    Start,
}

impl std::fmt::Display for Tile {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Tile::Garden => ".",
                Tile::Rock => "#",
                Tile::Start => "O",
            }
        )
    }
}

struct Grid {
    data: Vec<Tile>,
    rows: usize,
    columns: usize,
}

impl std::fmt::Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        for (i, c) in self.data.iter().enumerate() {
            if i % self.columns == 0 && i != 0 {
                writeln!(f)?;
            }
            write!(f, "{}", c)?;
        }
        Ok(())
    }
}

impl Grid {
    fn from_data<I>(data: I, rows: usize, columns: usize) -> Self
    where
        I: Iterator<Item = Tile>,
    {
        Self {
            data: data.collect(),
            rows,
            columns,
        }
    }

    fn from_string(data: &str) -> Self {
        let columns = data.split('\n').next().map_or(0, |x| x.len());
        let rows = data.split('\n').filter(|x| !x.trim().is_empty()).count();
        Self {
            data: data
                .chars()
                .filter_map(|x| match x {
                    '.' => Some(Tile::Garden),
                    '#' => Some(Tile::Rock),
                    'S' => Some(Tile::Start),
                    _ => None,
                })
                .collect(),
            rows,
            columns,
        }
    }

    fn get(&self, i: isize, j: isize) -> Option<&Tile> {
        if 0 <= i && i < self.rows as isize && 0 <= j && j < self.columns as isize {
            Some(&self.data[(i * (self.columns as isize) + j) as usize])
        } else {
            None
        }
    }

    fn get_mut(&mut self, i: isize, j: isize) -> Option<&mut Tile> {
        if 0 <= i && i < self.rows as isize && 0 <= j && j < self.columns as isize {
            Some(&mut self.data[(i * (self.columns as isize) + j) as usize])
        } else {
            None
        }
    }
}

fn next_grid(grid: &Grid) -> Grid {
    let mut other = Grid::from_data(
        grid.data.iter().map(|x| match x {
            Tile::Rock => Tile::Rock,
            _ => Tile::Garden,
        }),
        grid.rows,
        grid.columns,
    );

    for i in 0..grid.rows {
        for j in 0..grid.columns {
            let (i, j) = (i as isize, j as isize);
            if grid.get(i, j).copied() != Some(Tile::Start) {
                continue;
            }

            for (di, dj) in [(1, 0), (-1, 0), (0, -1), (0, 1)] {
                if let Some(cell) = other.get_mut(i + di, j + dj) {
                    if *cell != Tile::Rock {
                        *cell = Tile::Start;
                    }
                }
            }
        }
    }

    other
}

fn main() -> std::io::Result<()> {
    let field = std::fs::read_to_string("2023-21-step-counter/input.txt")?;
    let mut grid = Grid::from_string(&field);

    for _ in 0..64 {
        grid = next_grid(&grid);
    }

    println!(
        "{}\n{}",
        grid,
        grid.data.iter().filter(|x| **x == Tile::Start).count()
    );

    Ok(())
}
