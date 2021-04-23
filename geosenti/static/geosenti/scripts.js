$(function() {
    $("#formy").submit(function(e){
        e.preventDefault();
        var s = this.elements.search.value;
        $.ajax({
            type: "POST",
            url: "/geosenti/search/",
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
            },
            data: {
                "searched":s,
            },
            success: function (response) {
                
                const leftData = response['left']
                const rightData = response['right']
                var ctx = $('#leftChart');
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
            }
        });
    });
});