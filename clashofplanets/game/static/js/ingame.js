function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
          	// Does this cookie string begin with the name we want?
          	if (cookie.substring(0, name.length + 1) == (name + '=')) {
            	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              	break;
            }
        }
    }
    return cookieValue;
}

function listPlanets(){
	var csrftoken = getCookie('csrftoken');
    var num = $('#gamenum').text();
	$.ajax({
	    type : 'POST',
	    data : { csrfmiddlewaretoken : csrftoken, num: num},
	    url : "get_planets/",
		success : function(json) {
				var plist = json.planets;
                var user = json.user;
				$('#playerList').empty();
				for (var i = 0; i < plist.length; i++) {
					$('#playerList').append(
                        '<tr>'
                        +'<td>' + plist[i].id +'</td>'
                        +'<td>' + plist[i].name+'</td>'
                        +'<td>' + plist[i].owner +'</td>'
                        +'<td>' + plist[i].seed +'</td>'
                        +'<td>' + plist[i].pop +'</td>'
                        +'<td>' + plist[i].shield +'</td>'
                        +'</tr>');
                    if ((plist[i].owner)==(user)){
                        $('#mypopavailable').empty();
                        $('#mypopavailable').append(plist[i].pop);
                    }
				}
			setTimeout(listPlanets, 3000);
		},
		error : function(xhr,errmsg,err) {
			console.log(xhr.status + ": " + xhr.responseText);
		},
	});
}

function planetDistribution(){
    var $range = $(".js-range-slider"),
    $from = $(".js-from"),
    $middle = $(".js-middle"),
    $to = $(".js-to"),
    range,
    min = 0,
    max = 100,
    from,
    to;
    var updateValues = function () {
        $from.prop("value", from);
        $middle.prop("value", to - from);
        $to.prop("value", max - to);
    };
    $range.ionRangeSlider({
        type: "double",
        min: min,
        max: max,
        prettify_enabled: false,
        grid: true,
        grid_num: 10,
        onChange: function (data) {
            from = data.from;
            to = data.to;
            updateValues();
        }
    });
    range = $range.data("ionRangeSlider");
    var updateRange = function () {
        range.update({
            from: from,
            to: to
        });
    };
    $from.on("change", function () {
        from = +$(this).prop("value");
        if (from < min) {
            from = min;
        }
        if (from > to) {
            from = to;
        }
        updateValues();
        updateRange();
    });
    $to.on("change", function () {
        to = +$(this).prop("value");
        if (to > max) {
            to = max;
        }
        if (to < from) {
            to = from;
        }
        updateValues();
        updateRange();
    });
}

$(document).ready(function(){
    planetDistribution();
	listPlanets();
    //canvas = document.getElementById("canvas");
    //context = canvas.getContext("2d");
});
