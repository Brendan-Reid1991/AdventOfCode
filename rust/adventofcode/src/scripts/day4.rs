use std::{ fs, fs::File, io::{ prelude::*, BufReader }, path::Path, str };

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

// struct Pair {
//     assignment1: Vec<u16>,
//     assignment2: Vec<u16>,
// }

fn parse_line(assignments: &String) -> (Vec<u16>, Vec<u16>) {
    let individual_assignments: Vec<&str> = assignments.split(",").collect();
    assert_eq!(individual_assignments.len(), 2);

    let bounds1: Vec<u16> = individual_assignments[0]
        .to_string()
        .split("-")
        .map(|x| x.parse::<u16>().unwrap())
        .collect();

    let bounds2: Vec<u16> = individual_assignments[1]
        .split("-")
        .map(|x| x.parse::<u16>().unwrap())
        .collect();
    assert_eq!(bounds1.len(), 2);
    assert_eq!(bounds2.len(), 2);

    (bounds1, bounds2)
}

fn fully_contained(assignments: &String) -> bool {
    let (bounds1, bounds2) = parse_line(assignments);
    if
        ((bounds1[0] >= bounds2[0]) & (bounds1[1] <= bounds2[1])) |
        ((bounds2[0] >= bounds1[0]) & (bounds2[1] <= bounds1[1]))
    {
        true
    } else {
        false
    }
}

fn overlap(assignments: &String) -> bool {
    let (bounds1, bounds2) = parse_line(assignments);
    if
        (bounds1[0]..bounds1[1] + 1).contains(&bounds2[0]) |
        (bounds1[0]..bounds1[1] + 1).contains(&bounds2[1]) |
        (bounds2[0]..bounds2[1] + 1).contains(&bounds1[0]) |
        (bounds2[0]..bounds2[1] + 1).contains(&bounds1[1])
    {
        true
    } else {
        false
    }
}

fn part1(pairings: Vec<String>) -> usize {
    pairings
        .iter()
        .filter(|x| fully_contained(x))
        .collect::<Vec<&String>>()
        .len()
}

fn part2(pairings: Vec<String>) -> usize {
    pairings
        .iter()
        .filter(|x| overlap(x))
        .collect::<Vec<&String>>()
        .len()
}

fn main() {
    let file_path = fs::canonicalize("../../problem_specs/day4.txt");
    let pairings: Vec<String> = lines_from_file(file_path.unwrap());
    let pairings_copy = pairings.clone();
    let p1_score = part1(pairings);
    println!("{}", p1_score);
    let p2_score = part2(pairings_copy);
    println!("{}", p2_score)
}
