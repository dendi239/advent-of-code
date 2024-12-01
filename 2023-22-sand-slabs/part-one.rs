use std::cmp::{max, min};
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq)]
struct Coords {
    x: i32,
    y: i32,
    z: i32,
}

#[derive(Debug, Clone, PartialEq)]
struct Brick {
    start: Coords,
    end: Coords,
}

impl FromStr for Coords {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s
            .split(',')
            .map(|x| x.parse::<i32>().unwrap());

        Ok(Coords {
            x: parts.next().ok_or(())?,
            y: parts.next().ok_or(())?,
            z: parts.next().ok_or(())?,
        })
    }
}

impl FromStr for Brick {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s
            .split('~')
            .map(|x| x.parse::<Coords>().unwrap());

        Ok(Brick {
            start: parts.next().unwrap(),
            end: parts.next().unwrap(),
        })
    }
}

impl Brick {
    fn low_z(&self) -> i32 {
        min(self.start.z, self.end.z)
    }

    fn up_z(&self) -> i32 {
        max(self.start.z, self.end.z)
    }

    fn lower(&mut self, dz: i32) {
        self.start.z -= dz;
        self.end.z -= dz;
    }
}

fn main() {}
