use std::{ fs, fs::File, io::{ prelude::*, BufReader }, path::Path };

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

struct Alphabet {
    uppercase: String,
    lowercase: String,
}

impl Default for Alphabet {
    fn default() -> Alphabet {
        let uppercase = String::from_utf8((b'A'..=b'Z').collect());
        let lowercase = String::from_utf8((b'a'..=b'z').collect());
        Alphabet {
            uppercase: uppercase.unwrap(),
            lowercase: lowercase.unwrap(),
        }
    }
}

impl Alphabet {
    pub fn get_priority(&self, character: &str) -> usize {
        if self.lowercase.contains(character) {
            let char_idx = self.lowercase.find(character).unwrap();
            char_idx + 1
        } else if self.uppercase.contains(character) {
            let char_idx = self.uppercase.find(character).unwrap();
            char_idx + 27
        } else {
            panic!("String value {} is not in the alphabet!", character);
        }
    }
}

fn common_item(rucksack: &String) -> (bool, String) {
    let size = rucksack.len();
    assert_eq!(size % 2, 0);
    assert!(size > 0);
    let compartment1: String = String::from(&rucksack[0..size / 2]);
    let compartment2: String = String::from(&rucksack[size / 2..]);

    for item in compartment1.chars() {
        if compartment2.contains(item) {
            return (true, item.to_string());
        }
    }
    return (false, String::from(""));
}

fn part1(rucksacks: Vec<String>) -> usize {
    let alphabet = Alphabet { ..Default::default() };
    let mut priority_score: Vec<usize> = Vec::new();
    for rucksack in rucksacks.iter() {
        let (success, item) = common_item(rucksack);
        if success {
            priority_score.push(alphabet.get_priority(&item));
        }
    }
    priority_score.iter().sum()
}

fn main() {
    let file_path = fs::canonicalize("../../problem_specs/day3.txt");
    let _rucksacks: Vec<String> = lines_from_file(file_path.unwrap());
    let p1_score: usize = part1(_rucksacks);
    println!("{}", p1_score)
}
