use std::cmp::max;

#[derive(Debug, Clone)]
pub struct CycleIndex {
    pub index: i64,
    pub cycle_start: i64,
    pub cycle_len: i64,
}

fn lrp_gcd(x: i64, y: i64) -> (i64, i64) {
    if y == 0 {
        (1, 0)
    } else {
        let (a, b) = lrp_gcd(y, x % y);
        (b, a - (x / y) * b)
    }
}

pub fn solve_chineese_remainder_theorem(remainders: Vec<CycleIndex>) -> CycleIndex {
    let mut prefs = Vec::with_capacity(remainders.len());
    prefs.push(1);

    for r in remainders.iter().rev().skip(1).rev() {
        prefs.push(prefs.last().copied().map_or(1, |x| x) * r.cycle_len);
    }

    let mut mult = 1;
    for (i, r) in remainders.iter().enumerate().skip(1).rev() {
        mult *= r.cycle_len;
        prefs[i - 1] *= mult;
    }

    let mut res = CycleIndex {
        index: 0,
        cycle_start: remainders
            .iter()
            .max_by_key(|x| x.cycle_start)
            .map_or(0, |x| x.cycle_start),
        cycle_len: prefs[0] * remainders[0].cycle_len,
    };

    for (p, r) in prefs.iter().zip(remainders.iter()) {
        let (inv, _) = lrp_gcd(*p, r.cycle_len);
        let mut inv = inv as i64;
        inv *= r.index % r.cycle_len;
        res.index += p * inv;
    }

    res.index += max(
        0,
        (res.cycle_start - res.index + res.cycle_len - 1) / res.cycle_len,
    ) * res.cycle_len;

    res
}

impl CycleIndex {
    pub fn with_two_points(prev: i64, curr: i64) -> Self {
        Self {
            index: curr,
            cycle_start: prev,
            cycle_len: curr - prev,
        }
    }
}
