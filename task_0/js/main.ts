interface Student {
  firstName: string;
  lastName: string;
  age: number;
  location: string;
}

const student1: Student = {
  firstName: "Winnie",
  lastName: "Kathomi",
  age: 22,
  location: "Nairobi"
};

const student2: Student = {
  firstName: "Alex",
  lastName: "Kiptoo",
  age: 25,
  location: "Eldoret"
};

const studentsList: Student[] = [student1, student2];

const table = document.createElement("table");
table.border = "1";
table.style.borderCollapse = "collapse";
table.style.marginTop = "20px";

studentsList.forEach((student) => {
  const row = document.createElement("tr");

  const firstNameCell = document.createElement("td");
  firstNameCell.textContent = student.firstName;
  firstNameCell.style.padding = "8px";

  const locationCell = document.createElement("td");
  locationCell.textContent = student.location;
  locationCell.style.padding = "8px";

  row.appendChild(firstNameCell);
  row.appendChild(locationCell);
  table.appendChild(row);
});

document.body.appendChild(table);
