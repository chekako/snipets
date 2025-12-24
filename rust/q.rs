
use std::ops::Add;

fn sum<T: Add<Output = T>>(num1: T, num2: T) -> T {
	num1 + num2
}

fn f1(i: u64) -> u64 {
	match i {
		0 => 1,
		n => n * f1(n - 1),
	}
}

fn f2(i: u64) -> u64 {
	(2..=i).product()
}

fn main() {
	let result1 = sum(10, 20);
	println!("Sum is: {}", result1);

	let result2 = sum(10.23, 20.45);
	println!("Sum is: {}", result2);

	println!("f1: {}", f1(7));
	println!("f2: {}", f2(7));

	let name: Option<String> = None;
//	name = None;
	if let Some(name) = name {
		println!("{}", name);
	}
	else {
		println!("testing");
	}
}
