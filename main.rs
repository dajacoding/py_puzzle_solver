use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use rayon::prelude::*;
use std::sync::mpsc;
use std::thread;

//##############################
//# get information from files # 
//##############################

// convert string with 5 numbers in array with 5 integers
fn string_to_int_array(input: &str) -> Result<[i32; 5], Box<dyn std::error::Error>> {
	let parts: Vec<&str> = input.split_whitespace().collect();	
	if parts.len() != 5 {
		return Err("Error 5 elements".into());}	
	let mut array = [0; 5];
	for (i, part) in parts.iter().enumerate() {
		array[i] = part.parse::<i32>()?;}	
	Ok(array)
}

// open files and return vector with array[5] 
fn read_text_files(input: i32) -> Result<Vec<[i32; 5]>, Box<dyn std::error::Error>> {
    let filename = format!("Teil{:02}.txt", input);
    let file = File::open(Path::new(&filename))?;
    let mut list: Vec<[i32; 5]> = Vec::new();
    for line in BufReader::new(file).lines() {
        let line = line?; 
        match string_to_int_array(&line) {
            Ok(array) => {
                list.push(array);},
            Err(e) => {
                eprintln!("Error parsing line: {}", e);}
        }
    }    
    Ok(list)
}

// iterate all 12 files and return a vector<vec<array[5]>>
fn collect_all_files() -> Result<Vec<Vec<[i32; 5]>>, Box<dyn std::error::Error>> {
    let mut all_results = Vec::with_capacity(12);    
    for i in 1..=12 {
        match read_text_files(i) {
            Ok(vec) => all_results.push(vec),
            Err(e) => return Err(Box::new(std::io::Error::new(
                std::io::ErrorKind::Other, 
                format!("Error reading file {}: {}", i, e)
            ))),
        }
    }
    Ok(all_results)
}

//##############################
//#     convert to binary      # 
//##############################

// set bit on nth position to 1
fn set_bit(value: &mut u64, n: i32) {
    *value |= 1u64 << n;
}

// for each 5-element array create 1 u64 and collect in vecs again
fn collect_all_binarys(input: Vec<Vec<[i32; 5]>>) -> Result<Vec<Vec<u64>>, Box<dyn std::error::Error>> {
    let mut all_results = Vec::with_capacity(12);
    for i in 0..=11 {  
        let mut list: Vec<u64> = Vec::new(); 
        for j in 0..=input[i].len() - 1{
            let mut value: u64 = 0;
            for k in 0..=4{
                set_bit(&mut value, input[i][j][k]);  
            }
            list.push(value);    
        }
        all_results.push(list);
    }
    Ok(all_results)
}

//##############################
//#      binary addition       # 
//##############################

// takes vectors of vectors of u64 and
// combines the u64 with the condition that the combination has now double the 1s on bit-level
// returns vectors of vectors of u64 
fn binary_addition(input: Vec<Vec<u64>>) -> Result<Vec<Vec<u64>>, Box<dyn std::error::Error>> {
    let in_len_half = input.len() / 2;
    let mut all_results = Vec::with_capacity(in_len_half);
    let bitcount_goal = input[0][0].count_ones() * 2;
    for i in 0..=in_len_half - 1{
        let mut list: Vec<u64> = Vec::new(); 
        for l1 in 0..= input[i].len() - 1{
            for l2 in 0..= input[i + in_len_half].len() - 1{
                let value = input[i][l1] + input[i + in_len_half][l2];
                if value.count_ones() == bitcount_goal {
                    list.push(value);
                }                
            }
        }
        all_results.push(list);
    }
    for i in 0..=in_len_half - 1{
        println!("{}", all_results[i].len())
    }
    Ok(all_results)
}

// takes vectors of vectors of u64 
// multithreat iteration to combine vom 3 different vectors of u64
// to find a combination that has 60 bits being a 1
// excluded results are written in a file
// found results are written in a file
fn iter_3(input: &Vec<Vec<u64>>){    
    input[0].par_iter().for_each(|a| {
        input[1].iter().for_each(|b| {
            let e = a + b; 
            if e.count_ones() == 40 { 
                input[2].iter().for_each(|c| {
                    let d = e + c;
                    if d.count_ones() == 60 {       
                        let result = format!("{}, {}, {}\n", a, b, c);                   
                        let out = OpenOptions::new()
                            .append(true)
                            .create(true)
                            .open("results.txt");
                        let _ = out.expect("error").write_all(result.as_bytes());
                        println!("{:?}, {:?}, {:?}", a, b, c); 
                    }
                });
            }
        });
        let _ = append_u64("not_in_results.txt", *a);
    });
}

//##############################
//#      not_in_results        # 
//##############################

// in case of restart the program
// read the file, that contains the excluded u64 
// returns a vector of u64
fn read_not_in_results() -> std::io::Result<Vec<u64>> {
    let file = File::open("not_in_results.txt")?;
    let reader = BufReader::new(file);    
    let mut numbers = Vec::new();
    for line in reader.lines() {
        let line = line?;
        if let Ok(number) = line.trim().parse::<u64>() {
            numbers.push(number);println!("{}", number.count_ones());
        }
    }
    Ok(numbers)
}

// takes a filename and a u64
// writes the u64 at the end of that filename-file
fn append_u64(filename: &str, value: u64) -> std::io::Result<()> {
    let mut file = OpenOptions::new()
        .append(true)
        .create(true)
        .open(filename)?;
    writeln!(file, "{}", value)?;
    Ok(())
}

//##############################
//#           main             # 
//##############################

// start
fn main() {
    // get datas from files
    let mut all_int_arr = Vec::with_capacity(12);
    match collect_all_files() {
        Ok(vecs) => all_int_arr = vecs,
        Err(e) => eprintln!("{}", e),
    };

    // transform data to usable u64
    let mut all_u64_v1 = Vec::with_capacity(12);
    match collect_all_binarys(all_int_arr){
        Ok(vecs) => all_u64_v1 = vecs,
        Err(e) => eprintln!("{}", e),
    };

    // combine vectors and reduce possibilities
    let mut all_u64_v2 = Vec::with_capacity(6);
    match binary_addition(all_u64_v1){
        Ok(vecs) => all_u64_v2 = vecs,
        Err(e) => eprintln!("{}", e),
    };    
    let mut all_hash = Vec::with_capacity(3);
    match binary_addition(all_u64_v2){
        Ok(vecs) => all_hash = vecs,
        Err(e) => eprintln!("{}", e),
    }

    // reduce u64-entries
    let mut not_in_results_u64 = Vec::new();
    match read_not_in_results() {
        Ok(numbers) => not_in_results_u64 = numbers,        
        Err(e) => eprintln!("Error reading file: {}", e),
    }
    all_hash[0].retain(|x| !not_in_results_u64.contains(x));

    // start search
    iter_3(&all_hash);
}
