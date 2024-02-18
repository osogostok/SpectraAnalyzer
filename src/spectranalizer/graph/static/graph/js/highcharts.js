console.log("Function started."); // Перемещаем вывод в консоль сюда

Highcharts.chart('container', {

    chart: {
        zoomType: 'x'
    },

    title: {
        text: 'Highcharts drawing ' + n + ' points',
        align: 'left'
    },

    subtitle: {
        text: 'Using the Boost module',
        align: 'left'
    },

    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<{headingTagName}>{chartTitle}</{headingTagName}><div>{chartSubtitle}</div><div>{chartLongdesc}</div><div>{xAxisDescription}</div><div>{yAxisDescription}</div>'
        }
    },

    tooltip: {
        valueDecimals: 2
    },

    xAxis: {
        type: 'datetime'
    },

    series: [{
        data: data,
        lineWidth: 0.5,
        name: 'Hourly data points'
    }]

});
