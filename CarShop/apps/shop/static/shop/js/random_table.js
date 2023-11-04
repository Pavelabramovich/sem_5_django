const randomTable = document.getElementById("random_table")

function addRow() {
    const row = document.createElement("tr")

    const rowSize = randomTable.rows.length
        ? randomTable.rows.item(0).cells.length
        : 1

    for (var i = 0; i < rowSize; i++) {
        const cell = createCell(null);
        row.appendChild(cell);
    }

    randomTable.appendChild(row);
}

function addColumn() {
    const rows = randomTable.rows;

    if (rows.length) {
        Array.prototype.forEach.call(rows, row => {
            const cell = createCell(null);
            row.appendChild(cell);
        });
    } else {
        addRow();
    }
}

function transpose() {
    const rows = randomTable.rows;

    if (!rows) {
        return;
    }

    const rowCount = rows.length;
    const colCount = rows.item(0).cells.length;

    const newRows = {}

    for (var i = 0; i < rowCount; i++) {
        for (var j = 0; j < colCount; j++) {
            const cell = rows.item(i).cells.item(j);
            newRows[[j,i]] = [cell.innerText, cell.classList.contains("selected")]
        }
    }

    randomTable.innerText = "";

    for (var i = 0; i < colCount; i++) {
        const row = document.createElement("tr")

        for (var j = 0; j < rowCount; j++) {
            const cell = createCell(newRows[[i, j]][0])

            if (newRows[[i, j]][1]) {
                cell.classList.add("selected")
            }

            row.appendChild(cell);
        }

        randomTable.appendChild(row);
    }
}

function createTable(height, width) {
    randomTable.innerText = "";

    while (height--) {
        addRow()
    }

    while (width --> 1) {
        addColumn()
    }
}

function createCell(content) {
    const cell = document.createElement("td");
    cell.textContent = content ?? Math.floor(Math.random() * 10);
    cell.addEventListener('mouseover', onCellMouseOver);
    cell.addEventListener("click", onCellMouseClick);

    return cell
}


function onCellMouseOver(e) {
    const cell = e.target;

    if (
        isLmbDown && !cell.classList.contains("selected") ||  // paint
        isRmbDown && cell.classList.contains("selected")      // erase
    ) {
        selectCell(cell)
    }
}

function onCellMouseClick(e) {
    const cell = e.target;
    selectCell(cell)
}




function selectCell(cell) {
    const maxSelection = document.getElementById("maxSelect").value;

    const row = cell.parentElement;
    const rowCells = Array.from(row.cells);
    const cellIndex = rowCells.indexOf(cell);

    const selectedInRow = rowCells.filter(c => c.classList.contains("selected"));
    const columnCells = Array.from(cell.parentElement.parentElement.rows);

    const selectedInColumn = Array.prototype
        .map.call(randomTable.rows, r => r.cells[cellIndex])
        .filter(c => c.classList.contains("selected"));

    if (cell.classList.contains("selected")) {
        cell.classList.remove("selected");
    } else if (
        selectedInRow.length < maxSelection &&
        selectedInColumn.length < maxSelection &&
        !hasNeighborSelected(rowCells, cellIndex)
    ) {
        cell.classList.add("selected");
    }
}

function hasNeighborSelected(cells, i) {
    if (i > 0 && cells[i - 1].classList.contains("selected")) {
        return true;
    }
    if (i < cells.length - 1 && cells[i + 1].classList.contains("selected")) {
        return true;
    }
    return false;
}


var isLmbDown = false;

document.addEventListener('mousedown', function(event) {
    if (event.button === 0) {
        isLmbDown = true;
    }
});

document.addEventListener('mouseup', function(event) {
    if (event.button === 0) {
        isLmbDown = false;
    }
});


var isRmbDown = false;

document.addEventListener('mousedown', function(event) {
    var isRmb;

    if ("which" in event)
        isRmb = event.which == 3;
    else if ("button" in event)
        isRmb = event.button == 2;

    if (isRmb) {
        isRmbDown = true;
    }


});

document.addEventListener('mouseup', function(event) {
    var isRmb;

    if ("which" in event)  // Gecko (Firefox), WebKit (Safari/Chrome) & Opera
        isRmb = event.which == 3;
    else if ("button" in event)  // IE, Opera
        isRmb = event.button == 2;

    if (isRmb) {
        isRmbDown = false;
    }
});

randomTable.addEventListener("contextmenu", e => e.preventDefault());