interface Teacher {
  readonly firstName: string;
  readonly lastName: string;
  fullTimeEmployee: boolean;
  yearsOfExperience?: number;
  location: string;
  [propName: string]: any;
}

const teacher1: Teacher = {
  firstName: "John",
  lastName: "Smith",
  fullTimeEmployee: true,
  yearsOfExperience: 10,
  location: "Nairobi",
};

const teacher2: Teacher = {
  firstName: "Jane",
  lastName: "Doe",
  fullTimeEmployee: false,
  location: "Eldoret",
  contract: true,
};

console.log(teacher1);
console.log(teacher2);
