use std::{ fs, fs::File, io::{ prelude::*, BufReader }, path::Path, collections::HashSet, str };

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

fn check_rucksack_for_duplicates(rucksack: &String) -> Vec<String> {
    let size = rucksack.len();
    assert_eq!(size % 2, 0);
    let compartment1: String = String::from(&rucksack[0..size / 2]);
    let compartment2: String = String::from(&rucksack[size / 2..]);

    let mut commonalities: Vec<String> = Vec::new();
    for item in compartment1.chars() {
        if compartment2.contains(item) {
            commonalities.push(item.to_string());
        }
    }
    commonalities
}

fn part1(rucksacks: Vec<String>) -> usize {
    let alphabet = Alphabet { ..Default::default() };
    let mut priority_score: Vec<usize> = Vec::new();
    for rucksack in rucksacks.iter() {
        let common = check_rucksack_for_duplicates(rucksack);
        if common.len() > 0 {
            priority_score.push(alphabet.get_priority(&common.first().unwrap()));
        }
    }
    priority_score.iter().sum()
}

fn compare_rucksacks(rcksck1: String, rcksck2: String) -> String {
    let rucksack1_as_vec: Vec<u8> = Vec::from(rcksck1);
    let rucksack2_as_vec: Vec<u8> = Vec::from(rcksck2);

    let rcksck_set1: HashSet<&u8> = HashSet::from_iter(rucksack1_as_vec.iter());
    let rcksck_set2: HashSet<&u8> = HashSet::from_iter(rucksack2_as_vec.iter());
    let intersection = rcksck_set1.intersection(&rcksck_set2);
    str::from_utf8(&intersection.map(|&x| *x as u8).collect::<Vec<u8>>())
        .unwrap()
        .to_string()
}

fn part2(rucksacks: Vec<String>) -> usize {
    let alphabet = Alphabet { ..Default::default() };
    let mut priority_score: Vec<usize> = Vec::new();

    for (idx, rcksck) in rucksacks.iter().enumerate().step_by(3) {
        let overlap_on_first_2: String = compare_rucksacks(
            rcksck.to_string(),
            rucksacks
                .iter()
                .nth(idx + 1)
                .unwrap()
                .to_string()
        );
        let group_badge: String = compare_rucksacks(
            overlap_on_first_2,
            rucksacks
                .iter()
                .nth(idx + 2)
                .unwrap()
                .to_string()
        );
        priority_score.push(alphabet.get_priority(&group_badge));
    }
    priority_score.iter().sum()
}

fn main() {
    let file_path = fs::canonicalize("../../problem_specs/day3.txt");
    let _rucksacks: Vec<String> = lines_from_file(file_path.unwrap());
    let rucksacks_copy = _rucksacks.clone();
    let p1_score: usize = part1(_rucksacks);
    println!("{}", p1_score);
    let p2_score = part2(rucksacks_copy);
    println!("{}", p2_score);
}
