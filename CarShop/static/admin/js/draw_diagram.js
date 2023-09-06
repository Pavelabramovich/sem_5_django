function drawDiagram(name, parameter, title, pieResidueSliceLabel, containerId, values) {
    var values = Object.entries(values)
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