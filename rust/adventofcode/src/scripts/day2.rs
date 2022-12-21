// use std::collections::HashMap;
use std::{
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

fn convert(play: &str) {
    if ["X", "Y", "Z"].contains(&&play) {
        return 1;
    } else {
        return 2;
    }
}

fn main() {
    let _strategy_guide = lines_from_file("../problem_specs/day2.txt");
}
