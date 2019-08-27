  google.charts.load('current', {'packages':['gauge']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {

    var data = google.visualization.arrayToDataTable([
      ['Label', 'Value'],
      ['Access', access_health ],
      ['Distribution', distribution_health ],
      ['Core', core_health ],
      ['WLC', wlc_health ],
      ['AP', ap_health ],
    ]);

    var options = {
      width: 400, height: 120,
      redFrom: 0, redTo: 50,
      yellowFrom:50, yellowTo: 90,
      greenFrom:90, greenTo: 100,
      minorTicks: 5
    };

    var chart = new google.visualization.Gauge(document.getElementById('gauges'));

    chart.draw(data, options);

  }