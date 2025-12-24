
function greeter1(person:string) {
  return "Hello, " + person;
}
let u = "Jane User";
//let user = [0, 1, 2];
document.body.textContent = greeter1(u);

class Student {
  fullName: string;
  constructor(
    public firstName: string,
    public middleInitial: string,
    public lastName: string
  ) {
    this.fullName = firstName + " " + middleInitial + " " + lastName;
  }
}

interface Person {
  firstName: string;
  lastName: string;
}

interface I1{}
interface I2{}
interface I0 extends I1, I2 {}

function greeter(person: Person) {
  return "Hello, " + person.firstName + " " + person.lastName;
}

let user = new Student("Jane", "M.", "User");

document.body.textContent = greeter(user);

let i : number = 5
let s : string = 'fdsfdsa'
let a : number[] = [1,2,3]
let t : [number, boolean] = [2.34, true]
let un : string | number = 123
un = 'twtrew'
enum E{a,b,c}
let e : E = E.a
const c = { k: 3, v: 't' }
