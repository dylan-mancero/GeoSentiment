$(function() {
    var leftChart;
    var rightChart;
    $("#formy").submit(function(e){
        e.preventDefault();
        const searchQuery = this.elements.search.value;
        const country1 = this.elements.Country1.value;
        const country2 = this.elements.Country2.value;
        if (country1===country2) {
            alert("Must be different locations")
            return
        }
        if (leftChart) {
            leftChart.destroy();
            rightChart.destroy();
        }
        $.ajax({
            type: "POST",
            url: "/geosenti/search/",
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
            },
            data: {
                "searched":searchQuery,
                "country1":country1,
                "country2":country2
            },
            success: function (response) {
                
                const leftData = response['left']
                const rightData = response['right']
                const ctxl = $('#leftChart');
                const ctxr = $('#rightChart');
                leftChart = createChart(ctxl, leftData)
                rightChart = createChart(ctxr, rightData)
            }
        });
    });
});