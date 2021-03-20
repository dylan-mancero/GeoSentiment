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
                console.log("something amazing")
            }
        });
    });
});