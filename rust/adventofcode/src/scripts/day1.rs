use std::fs;
use std::path::Path;

fn main() {
    let file_path = Path::new("/../../problem_specs/day1.txt");

    let file_contents = fs::read_to_string(file_path).expect("Error reading file");

    let mut all_calories_held: Vec<i32> = Vec::new();
    let mut calories_held = 0;
    for line in file_contents.lines() {
        if line.is_empty() {
            all_calories_held.push(calories_held);
            calories_held = 0;
        } else {
            let calories: i32 = line.parse().unwrap();
            calories_held += calories;
        }
    }

    all_calories_held.sort_by(|a, b| b.cmp(a));

    let max_calories_held: i32 = all_calories_held[0];
    println!("{:?}", max_calories_held);

    let top_3_calories_held: i32 = all_calories_held[0..3].iter().sum();
    println!("{:?}", top_3_calories_held);
}
