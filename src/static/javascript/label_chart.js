/* Declare bar chart data and options as dictionaries */
 
var barData = {
    labels: chartLabels,
    datasets: [
        {
            backgroundColor: "rgba(26, 126, 126, 0.4)",
            borderColor: "rgba(26, 126, 126, 1)",
            borderSkipped: "bottom",
            borderWidth: 1,
            label: "Not labeled",
            data: unlabeled 
        }, 
        {
            backgroundColor: "rgba(172, 96, 21, 0.4)",
            borderColor: "rgba(172, 96, 21, 1)",
            borderSkipped: "bottom",
            borderWidth: 1,
            label: "Labeled",
            data: labeled
        }
    ]
};

var barOptions = {
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
    type: 'bar',
    data: barData,
    options: barOptions
});
