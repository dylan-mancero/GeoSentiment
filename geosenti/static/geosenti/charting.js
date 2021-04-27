function createChart(ctx, leftData) {
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data :{
            labels: [
                'Negative',
                'Positive',
                'Neutral'
              ],
              datasets: [{
                label: 'left Data',
                data: [leftData['neg'], leftData['pos'], leftData['neutral']],
                backgroundColor: [
                  'rgb(255, 99, 132)',
                  'rgb(54, 162, 235)',
                  'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
              }]
        }
    });
    return myChart
}