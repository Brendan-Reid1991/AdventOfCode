use std::{ fs, fs::File, io::{ prelude::*, BufReader }, path::Path, str };

use itertools::Itertools;

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

struct Containers {
    stack_config: Vec<String>,
}

impl Containers {
    fn get_stacks(&self) -> (Vec<u32>, Vec<usize>) {
        let stack_labels: Vec<u32> = self.stack_config[self.stack_config.len() - 1]
            .chars()
            .filter_map(|x| x.to_digit(10))
            .collect();

        let stack_indices: Vec<usize> = stack_labels
            .iter()
            .map(|x|
                self.stack_config[self.stack_config.len() - 1]
                    .chars()
                    .position(|y| char::from_digit(*x, 10).unwrap() == y)
                    .unwrap()
            )
            .collect();

        (stack_labels, stack_indices)
    }

    fn initial_stack_contents(&self, stack_num: u32) -> Vec<String> {
        let (stack_labels, stack_indices) = self.get_stacks();
        if !stack_labels.contains(&stack_num) {
            panic!("Stack number given is not present in the manifest.");
        }
        let index: usize =
            stack_indices
                [
                    stack_labels
                        .iter()
                        .position(|&x| x == stack_num)
                        .unwrap()
                ];
        let relevant_lines: Vec<&String> = self.stack_config
            .iter()
            .filter(|line| line.len() >= index && line.chars().nth(index).unwrap() != ' ')
            .collect();

        relevant_lines
            .iter()
            .map(|line| line.chars().nth(index).unwrap().to_string())
            .collect()
    }

    pub fn initial_configuration(&self) -> Vec<Vec<String>> {
        let (stack_labels, _) = self.get_stacks();
        let mut config: Vec<Vec<String>> = Vec::new();
        for label in stack_labels.iter() {
            let stack_contents: Vec<String> = self.initial_stack_contents(*label);
            config.push(stack_contents);
        }
        config
    }
}

fn parse_instruction(instr: &String) -> Vec<u32> {
    let relevant_instructions: Vec<u32> = instr
        .split(' ')
        .filter(|x| x.chars().all(char::is_numeric))
        .map(|x| x.parse::<u32>().unwrap())
        .collect();
    relevant_instructions
}

fn update_crate_configuration(configuration: Vec<Vec<String>>, instr: &String) -> () {
    let (_move, _from, _to) = parse_instruction(instr).iter().next_tuple().unwrap();
    println!("{}, {}, {}", _move, _from, _to)
}

fn main() {
    let file_path = fs::canonicalize("../../problem_specs/day5.txt");
    let stacks_and_instructions: Vec<String> = lines_from_file(file_path.unwrap());
    let dividing_line: usize = stacks_and_instructions
        .iter()
        .position(|x| x.is_empty())
        .unwrap();
    let _stacks: Vec<String> = stacks_and_instructions[0..dividing_line].to_vec();
    let _instructions: Vec<String> = stacks_and_instructions[dividing_line + 1..].to_vec();

    let manifest: Containers = Containers {
        stack_config: _stacks,
    };
    let mut config = manifest.initial_configuration();
    for instr in _instructions.iter() {
        update_crate_configuration(config, instr);
    }
}
