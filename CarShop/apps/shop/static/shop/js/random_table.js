
var div = document.getElementById("cont")

var randomTable = document.createElement("table")
randomTable.setAttribute('id', "random_table")

div.appendChild(randomTable)

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
        isLmbDown && !cell.classList.contains("selected")   // paint
        || isRmbDown && cell.classList.contains("selected")      // erase
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
    const cellIndex = Array.prototype.indexOf.call(row.cells, cell);

    const selectedInRow = Array.prototype.filter.call(row.cells, c => c.classList.contains("selected"));

    const selectedInColumn = Array.prototype
        .map.call(randomTable.rows, r => r.cells[cellIndex])
        .filter(c => c.classList.contains("selected"));

    if (cell.classList.contains("selected")) {
        cell.classList.remove("selected");
    } else if (
        selectedInRow.length < maxSelection
        && selectedInColumn.length < maxSelection
        && !hasNeighborSelected(row.cells, cellIndex)
    ) {
        cell.classList.add("selected");
    }
}

function hasNeighborSelected(cells, i) {
    return i > 0 && cells.item(i - 1).classList.contains("selected")
           || i < cells.length - 1 && cells.item(i + 1).classList.contains("selected");
}


var isLmbDown = false;
var isRmbDown = false;

document.addEventListener('mousedown', function(event) {
    if (event.button === 0) {
        isLmbDown = true;
    }

    if ("which" in event && event.which === 3) {
        isRmbDown = true;
    } else if ("button" && event.button === 2) {
        isRmbDown = true;
    }
});

document.addEventListener('mouseup', function(event) {
    if (event.button === 0) {
        isLmbDown = false;
    }

    if ("which" in event && event.which === 3) {
        isRmbDown = false;
    } else if ("button" && event.button === 2) {
        isRmbDown = false;
    }
});

// disable default menu on rmb
randomTable.addEventListener("contextmenu", e => e.preventDefault());