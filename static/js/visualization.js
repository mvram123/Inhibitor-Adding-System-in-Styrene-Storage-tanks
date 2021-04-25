google.charts.load("current", {'packages':["corechart"]});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
              ['DAYS', 'TEMPERATURE'],
              [1,  64],
              [2,  70],
              [3,  61],
              [4,  68],
              [5,  69],
              [6,  67],
              [7,  68],
              [8,  68],
              [9,  61],
              [10,  62],
              [11,  68],
              [12,  63],
              [13,  67],
              [14,  62],
              [15,  68],
              [16,  61],
              [17,  69],
              [18,  61],
              [19,  64],
              [20,  65],
              [21,  66],
              [22,  69],
              [23,  65],
              [24,  68],
              [25,  67],
              [26,  67],
              [27,  61],
              [28,  63],
              [29,  70],
              [30,  64],
        ]);

        var options = {
          title: 'TEMPERATURE (FOR LAST 30 DAYS)',
            legend: { position: 'bottom'},
          series: {
            0: { color: '#ff1414' }
          }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
        chart.draw(data, options);
      }