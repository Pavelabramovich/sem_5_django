var id;

var students = JSON.parse(sessionStorage.getItem('students'))

if (students) {
    var arr = Array.from(Object.keys(students))
    id = Math.max(...arr) + 1;
} else {
    id = 0;
}

var table = document.querySelector("#students");

students = Object.values(students)


students.forEach(s => {
    var row = document.createElement("tr");

    [s.name, s.surname, s.form].forEach(field => {
        const cell = document.createElement("td");
        const cellText = document.createTextNode(field);
        cell.appendChild(cellText);

        row.appendChild(cell);
    });

    table.appendChild(row);
})


function addStudents() {
    var name = document.querySelector("#name").value;
    var surname = document.querySelector("#surname").value;
    var form = document.querySelector("#form").value;

    if (name && surname && form) {

        var row = document.createElement("tr");

        [name, surname, form].forEach(field => {
            const cell = document.createElement("td");
            const cellText = document.createTextNode(field);
            cell.appendChild(cellText);

            row.appendChild(cell);
        });

        if (sessionStorage.getItem('students')) {
            var students = JSON.parse(sessionStorage.getItem('students'));
            students[id++] = {name, surname, form}

            var repetitionsMarker = document.querySelector("#repetitions");

            var surnames = Object.values(students).map(s => s.surname);

            if ((new Set(surnames)).size === surnames.length) {
                repetitionsMarker.innerText = "No repetitions";
                repetitionsMarker.style.color = "blue";
            } else {
                repetitionsMarker.innerText = "Repetitions!!!";
                repetitionsMarker.style.color = "red";
            }

            sessionStorage.setItem('students', JSON.stringify(students))
        } else {
            sessionStorage.setItem('students', JSON.stringify({[id++]: {name, surname, form}}))
        }

        table.appendChild(row);
    }
}
