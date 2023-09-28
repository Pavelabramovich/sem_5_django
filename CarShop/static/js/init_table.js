function initTable(maxColumnCount, tableId, title, vHeader, columns) {
    var table = document.getElementById(tableId)

    var caption = document.createElement("caption")
    var head = document.createElement("h4")
    title = document.createTextNode(title)

    head.appendChild(title)
    caption.appendChild(head)
    table.appendChild(caption)

    var origLen = columns.length
    var totalLen = maxColumnCount ? Math.ceil(columns.length / maxColumnCount) * maxColumnCount : columns.length

    if (columns.length > 0 && columns[0].length > vHeader.length) {
        vHeader = ['\u00A0'].concat(vHeader)
    }

    const height = vHeader.length

    for (var i = columns.length; i < totalLen; i++) {
        const placeholder = '\u00A0'.repeat(i - maxColumnCount >= 0 ? columns[i - maxColumnCount].length : 6)
        columns.push(Array(height).fill(placeholder))
    }

    var rows = new Array(height).fill().map(r => (document.createElement("tr")));

    for (var i = 0; i < totalLen; i++) {
        // Add vertical header.
        if (i % maxColumnCount == 0) {
            for (var j = 0; j < height; j++) {
                const cell = document.createElement(j == 0 ? "th" : "td");
                const cellText = document.createTextNode(vHeader[j]);
                cell.appendChild(cellText);

                rows[j].appendChild(cell);
            }
        }

        for (var j = 0; j < height; j++) {
            const cell = document.createElement(j == 0 ? "th" : "td");
            const cellText = document.createTextNode(columns[i][j]);
            cell.appendChild(cellText);

            if (i === origLen - 1) {
                cell.setAttribute("colspan", totalLen - origLen + 1);

                if (j === height - 1) {
                    i = totalLen - 1
                }
            }

            rows[j].appendChild(cell);
        }

        if ((i + 1) % maxColumnCount == 0) {
            var old = rows[0]
            rows[0] = document.createElement("thead")
            rows[0].appendChild(old)

            rows.forEach(row => {
                table.appendChild(row)
            });

            rows = new Array(height).fill().map(r => (document.createElement("tr")));
        }

    }
}