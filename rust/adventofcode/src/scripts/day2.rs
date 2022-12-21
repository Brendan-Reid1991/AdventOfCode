use std::{fs,
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
};

use phf::phf_map;

static SCORE: phf::Map<&'static str, u32> = phf_map! {
    "Rock" => 1,
    "Paper" => 2,
    "Scissors" => 3,
};

static WINNING_STRAT: phf::Map<&'static str, &'static str> = phf_map! {
    "Rock" => "Paper",
    "Paper" => "Scissors",
    "Scissors" => "Rock",
};

static LOSING_STRAT: phf::Map<&'static str, &'static str> = phf_map! {
    "Rock" => "Scissors",
    "Paper" => "Rock",
    "Scissors" => "Paper",
};

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}


fn convert(play: &str)->&str {
    let xyz: Vec<&str> = vec!["X", "Y", "Z"];
    let abc: Vec<&str> = vec!["A", "B", "C"];

    if xyz.contains(&&play) {
        return play
    } else {
        let idx = abc.iter().position(|&r| r == play).unwrap();
        return xyz.iter().nth(idx).unwrap();
    }
}

fn outcome(player1: &str, player2: &str) -> u32 {

}

fn main() {

    let file_path = fs::canonicalize("../../problem_specs/day2.txt");
    let strategy_guide = lines_from_file(file_path.unwrap());
    for line in strategy_guide.iter() {
        let first_col = line.chars().nth(0).unwrap();
        let second_col = line.chars().last().unwrap();
    }
}
