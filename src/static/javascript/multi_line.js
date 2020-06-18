/* Declare bar chart data and options as dictionaries */

var colors = ["#000000", "#003d66", "#006bb3", "#0099ff", "#66c2ff", "#b3e0ff", "#6600cc", "#8c1aff"]
var index = 0
var dataSet = []
for (let key in dataObj) {
    dataSet.push({
        label: key,
        data: dataObj[key],
        borderColor: colors[index],
        fill: false
    })
    index = index + 1
}

var lineData = {
    labels: chartLabels,
    datasets: dataSet 
};

console.log(lineData)

var lineOptions = {
    title: {
        display: true,
        text: chartTitle,
        fontSize: 18
    },
    legend: {
        display: true,
        labels: {
            fontSize: 13
        }
    },
    scales: {
        yAxes: [{
            scaleLabel: {
                display: true,
                labelString: yLabel,
                fontSize: 15
            },
            ticks: {
                fontSize: 13,
                beginAtZero: true
            }
        }],
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: xLabel,
                fontSize: 15
            },
            ticks: {
                fontSize: 13
            },
            autoskip: true
        }]
    }     
};

/* Get chart canvas and draw the chart */
var ctx = document.getElementById(canvasID).getContext("2d");
var chart = new Chart(ctx, {
    type: 'line',
    data: lineData,
    options: lineOptions
});
