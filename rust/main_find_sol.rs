
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::env;

//##############################
//#          results           # 
//##############################

// const R1V1: [u64; 3] = [18161482951001600, 224115895571578983, 2063565630690589080];
// const R2V1: [u64; 3] = [18161620316521472, 224115758273966144, 2063565630623205823];
// const R3V1: [u64; 3] = [354333485532702, 1750978556347809792, 518481322361387489];
// const R4V1: [u64; 3] = [604864404442056704, 14523930431, 1696474990620336320];
// const R5V1: [u64; 3] = [591815496861680128, 106587951509568, 1713920924400503231];


// const R1V2: [u64; 6] = [18155963859108352, 5519091893248, 6790721788969063, 217325173782609920, 2063565630623186944, 67402136];
// const R2V2: [u64; 6] = [18156101224628224, 5519091893248, 6808244719464512, 217307513554501632, 2063565630623186944, 18879];
// const R3V2: [u64; 6] = [8606811678, 354324878721024, 1747591475270516736, 3387081077293056, 517913957147883552, 567365213503937];
// const R4V2: [u64; 6] = [19290693339971584, 585573711102085120, 14515508224, 8422207, 506672550269444288, 1189802440350892032];
// const R5V2: [u64; 6] = [591248118746447872, 567378115232256, 813445184, 106587138064384, 1713920924400484352, 18879];

// const R1V3: [u64; 12] = [18155962779041792, 1080066560, 6790721788968960, 103, 2026690201060900864, 36875429562286080, 4415276843008, 1103815050240, 17661309222912, 217307512473387008, 16792, 67385344];
// const R2V3: [u64; 12] = [18155962779041792, 138445586432, 798784, 6808244718665728, 2026690201060900864, 36875429562286080, 4415276843008, 1103815050240, 1081114624, 217307512473387008, 16792, 2087];
// const R3V3: [u64; 12] = [8606811136, 542, 1747538492419735552, 52982850781184, 276512, 517913957147607040, 283680450805760, 70644427915264, 550836895744, 3386530240397312, 16833, 567365213487104];
// const R4V3: [u64; 12] = [18155962779041792, 1134730560929792, 12901745664, 1613762560, 506672550265225216, 4219072, 68988700672, 585573642113384448, 8422160, 47, 1189235075137404928, 567365213487104];
// const R5V3: [u64; 12] = [590113388185518080, 1134730560929792, 798784, 812646400, 506672550265225216, 1207248374135259136, 567360901611520, 17213620736, 35666482167808, 70920655896576, 16792, 2087];

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
    Ok(all_results)
}


//##############################
//#      detect results        # 
//##############################

// get bit positions
fn get_bit_positions(ns: Vec<u64>) {
    let result: Vec<Vec<u32>> = ns
        .iter()
        .map(|&n| (0..64).filter(|&i| n & (1 << i) != 0).collect())
        .collect();
    for (_index, positions) in result.iter().enumerate() {
        println!("{:?}", positions);
    }
}


fn binary_addition_for_detection(data: Vec<Vec<u64>>, given: Vec<u64>) -> Result<Vec<u64>, Box<dyn std::error::Error>> {
    let mut found: Vec<u64> = Vec::new();
    let in_len_half = data.len() / 2;
    for i in 0..=in_len_half - 1{
        for l1 in 0..= data[i].len() - 1{
            for l2 in 0..= data[i + in_len_half].len() - 1{
                let value = data[i][l1] + data[i + in_len_half][l2];
                if given.contains(&value)   {  
                    found.push(data[i][l1]);
                    found.push(data[i + in_len_half][l2]); 
                }             
            }
        }
    }
    Ok(found)
}

//##############################
//#           main             # 
//##############################

// start
fn main() {
    // get arguments
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        println!("Verwendung: {} <zahl1> <zahl2> <zahl3>", args[0]);
        return;
    }
    let mut given_u64: Vec<u64> = Vec::new();
    for arg in args.iter().skip(1) {
        match arg.parse::<u64>() {
            Ok(num) => given_u64.push(num),
            Err(_) => {
                println!("Fehler: '{}' ist keine gültige positive ganze Zahl.", arg);
                return;
            }
        }
    }

    // get data from files
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
    let mut all_u64_v2 = Vec::with_capacity(6);
    match binary_addition(all_u64_v1.clone()){
        Ok(vecs) => all_u64_v2 = vecs,
        Err(e) => eprintln!("{}", e),
    };  

    // find relations
    let mut found_u64_v2 = Vec::new();
    match binary_addition_for_detection(all_u64_v2, given_u64) {
        Ok(found) => found_u64_v2 = found,
        Err(e) => eprintln!("{}", e),
    };

    let mut found_u64_v1 = Vec::new();
    match binary_addition_for_detection(all_u64_v1, found_u64_v2) {
        Ok(found) => found_u64_v1 = found,
        Err(e) => eprintln!("{}", e),
    };

    get_bit_positions(found_u64_v1);
}