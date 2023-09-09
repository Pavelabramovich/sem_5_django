function drawPieDiagram(name, parameter, title, pieResidueSliceLabel, containerId, values) {
    values = [[name, parameter]].concat(values)

    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable(values);

        var options = {
             title: title,
             is3D: true,
             pieResidueSliceLabel: pieResidueSliceLabel
        };

        var chart = new google.visualization.PieChart(document.getElementById(containerId));
        chart.draw(data, options);
    }
}

function drawDateTrendLineDiagram(hAxis, vAxis, title, legend, containerId, dates) {
    vAxis = vAxis || 'Date'

    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('date', hAxis);
        data.addColumn('number', vAxis);

        dates.forEach(date => {
            data.addRow([new Date(date[0]), date[1]])
        });

        var options = {
            title: title,
            hAxis: {title: hAxis},
            vAxis: {title: vAxis},
            legend: legend || 'none',
            trendlines: { 0: {type: 'polynomial'} }
        };

        var chart = new google.visualization.ScatterChart(document.getElementById(containerId));
        chart.draw(data, options);
    }
}