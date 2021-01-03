google.charts.load('current', {'packages':['gantt']});
google.charts.setOnLoadCallback(drawChart);

function daysToMilliseconds(days) {
      return days * 24 * 60 * 60 * 1000;
}

function drawChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Task ID');
    data.addColumn('string', 'Task Name');
    data.addColumn('date', 'Start Date');
    data.addColumn('date', 'End Date');
    data.addColumn('number', 'Duration');
    data.addColumn('number', 'Percent Complete');
    data.addColumn('string', 'Dependencies');

    data.addRows([
        ['Research', 'Find sources',
         new Date(2017, 0, 2), new Date(2017, 0, 6), null,  110,  null],
        ['Write', 'Write paper',
         null, new Date(2017, 0, 10), daysToMilliseconds(3), 35, 'Research,Outline'],
        ['Cite', 'Create bibliography',
         null, new Date(2017, 0, 8), daysToMilliseconds(1), 30, 'Research'],
        ['Complete', 'Hand in paper',
         null, new Date(2017, 0, 11), daysToMilliseconds(1), 10, 'Cite,Write'],
        ['Outline', 'Outline paper',
         null, new Date(2017, 0, 7), daysToMilliseconds(1), 110, 'Research']
      ]);

    var options = {
        height: 175
    };

    var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

    chart.draw(data, options);
}