function addStudents() {
    var name = document.querySelector("#name").value;
    var surname = document.querySelector("#surname").value;
    var form = document.querySelector("#form").value;

    if (name && surname && form) {
        var table = document.querySelector("#students");

        var row = document.createElement("tr");

        [name, surname, form].forEach(field => {
            const cell = document.createElement("td");
            const cellText = document.createTextNode(field);
            cell.appendChild(cellText);

            row.appendChild(cell);
        });

        if (table.dataset.surnames) {
            var surnames = JSON.parse(table.dataset.surnames);
            surnames.push(surname);

            var repetitionsMarker = document.querySelector("#repetitions");

            if ((new Set(surnames)).size === surnames.length) {
                repetitionsMarker.innerText = "No repetitions";
                repetitionsMarker.style.color = "blue";
            } else {
                repetitionsMarker.innerText = "Repetitions!!!";
                repetitionsMarker.style.color = "red";
            }

            table.dataset.surnames = JSON.stringify(surnames);
        } else {
            table.dataset.surnames = JSON.stringify([surname]);
        }

        table.appendChild(row);
    }
}
