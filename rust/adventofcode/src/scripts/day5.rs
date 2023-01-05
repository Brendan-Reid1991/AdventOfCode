use std::{ fs, fs::File, io::{ prelude::*, BufReader }, path::Path, str };

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

fn main() {
    let file_path = fs::canonicalize("../../problem_specs/day5.txt");
    let stacks_and_instructions: Vec<String> = lines_from_file(file_path.unwrap());
    let dividing_line: usize = stacks_and_instructions
        .iter()
        .position(|x| x.is_empty())
        .unwrap();
    let stacks: Vec<String> = stacks_and_instructions[0..dividing_line].to_vec();
    let instructions: Vec<String> = stacks_and_instructions[dividing_line + 1..].to_vec();
}
