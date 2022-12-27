use std::{fs,
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
};

use phf::phf_map;

static SCORE: phf::Map<&'static str, i8> = phf_map! {
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

fn convert(play: String)->String {
    let xyz: Vec<String> = ["X", "Y", "Z"].map(String::from).to_vec();
    let abc: Vec<String> = ["A", "B", "C"].map(String::from).to_vec();

    let rps: Vec<String> = ["Rock", "Paper", "Scissors"].map(String::from).to_vec();

    if xyz.contains(&play) {
        let idx = xyz.iter().position(|r| r == &play).unwrap();
        let equiv_play: String = rps.get(idx).unwrap().to_string();
        equiv_play
    } else {
        let idx = abc.iter().position(|r| r == &play).unwrap();
        let equiv_play: String = rps.get(idx).unwrap().to_string();
        equiv_play
    }


}

fn outcome(player1: String, player2: String) -> i8 {
    let score: i8 = SCORE[&player2] - SCORE[&player1];
    if score == 0 {
       return 3 + SCORE[&player2]
    } else if vec![1, -2].contains(&score) {
        return 6 + SCORE[&player2]
    } else if vec![-1, 2].contains(&score) {
        return SCORE[&player2]
    };
    panic!("Invalid game outcomes.")
}

fn tactics(opponent: String, instructions: String) -> String {
    if instructions.eq(&"X".to_string()) {
        LOSING_STRAT[&opponent].to_string()
    } else if instructions.eq(&"Z".to_string()) {
        WINNING_STRAT[&opponent].to_string()
    } else {
        opponent
    }
}

fn part1() {

    let file_path = fs::canonicalize("../../problem_specs/day2.txt");
    let strategy_guide = lines_from_file(file_path.unwrap());
    let mut score = Vec::new();
    for line in strategy_guide.iter() {
        let first_col = convert(line.chars().next().unwrap().to_string());
        let second_col = convert(line.chars().last().unwrap().to_string());
        score.push(outcome(first_col, second_col));
    };
    println!("{}", score.iter().map(|i| (*i) as u32).sum::<u32>())
}

fn part2() {

    let file_path = fs::canonicalize("../../problem_specs/day2.txt");
    let strategy_guide = lines_from_file(file_path.unwrap());
    let mut score = Vec::new();
    for line in strategy_guide.iter() {
        let first_col = convert(line.chars().nth(0).unwrap().to_string());
        let copy = first_col.clone();
        let second_col = line.chars().last().unwrap().to_string();
        let my_play = tactics(first_col, second_col);
        score.push(outcome(copy, my_play));
    };
    println!("{}", score.iter().map(|i| (*i) as u32).sum::<u32>())
}


fn main() {
    part1();
    part2();
}
