// use std::fs;
use std::env;
use std::io::Result;
use std::path::PathBuf;

fn get_current_working_dir() -> std::io::Result<PathBuf> {
    return env::current_dir();
}

fn main() {
    let cwd = get_current_working_dir();
    println!("{}", cwd);
}
