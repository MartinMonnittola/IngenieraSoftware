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

function timeStamp() {
    // Create a date object with the current time
    var now = new Date();
    // Create an array with the current month, day and time
    var date = [ now.getMonth() + 1, now.getDate(), now.getFullYear() ];
    // Create an array with the current hour, minute and second
    var time = [ now.getHours(), now.getMinutes(), now.getSeconds() ];
    // Determine AM or PM suffix based on the hour
    var suffix = ( time[0] < 12 ) ? "AM" : "PM";
    // Convert hour from military time
    time[0] = ( time[0] < 12 ) ? time[0] : time[0] - 12;
    // If hour is 0, set it to 12
    time[0] = time[0] || 12;

    // If seconds and minutes are less than 10, add a zero
    for ( var i = 1; i < 3; i++ ) {
        if ( time[i] < 10 ) {
          time[i] = "0" + time[i];
        }
    }
    // Return the formatted string
    //return date.join("/") + " " + time.join(":") + " " + suffix;
    return time.join(":") + " " + suffix;
}

function listPlanets(){
	var csrftoken = getCookie('csrftoken');
    var num = $('#gamenum').text();
    var timest = timeStamp();
	$.ajax({
	    type : 'POST',
	    data : { csrfmiddlewaretoken : csrftoken, num: num},
	    url : "get_planets/",
		success : function(json) {
			var plist = json.planets;
            var user = json.user;
			$('#playerList').empty();
			for (var i = 0; i < plist.length; i++) {
                if ((plist[i].owner)==(user)){
                    $('#mypopAvailable').empty();
                    $('#mypopAvailable').append(plist[i].pop);
                    $('#mymissilesAvailable').empty();
                    $('#mymissilesAvailable').append(plist[i].missiles);
                }
                $('#planet-'+plist[i].id+' .tb_planet_pop').empty();
				$('#planet-'+plist[i].id+' .tb_planet_pop').append(plist[i].pop);
                $('#planet-'+plist[i].id+' .tb_planet_shield').empty();
                $('#planet-'+plist[i].id+' .tb_planet_shield').append(plist[i].shield);
			}
        setTimeout(listPlanets, 2000);
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

function battleLog(linelog){
    var consoleLine = "<p class=\"console-line\"></p>";
    console = {
        log: function (text) {
            $("#console-log").append($(consoleLine).html(text));
        }
    };
    console.log(linelog);
}

function changeDistribution(){
    var csrftoken = getCookie('csrftoken');
    var num = $('#gamenum').text();
    var population = $("#population_range").text();
    var shield = $("#shield_range").text();
    var missiles = $("#missiles_range").text();
    var timest = timeStamp();
    $.ajax({
        type: "POST",
        url: "change_distribution/",
        data: {
                csrfmiddlewaretoken: csrftoken,
                population: population,
                shield: shield,
                missiles: missiles,
                game_num: num,
              },
        dataType: 'json',
    });
    battleLog('['+ timest +']'+' '+'|'+' '+'NRD'+' '+'P:'+population +' '+'S:'+shield+' '+'M:'+missiles);
}

function attackPlanet(){
    $('.attack-planet').on("click", function(event) {
        event.preventDefault();
        var planet_id = $(this).closest('tr').find('td:nth-child(1)').text();
        //battleLog(planet_id); //Uncomment to check attack is working OK
        var num = $('#gamenum').text();
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: "send_attack/",
            data: {
                    csrfmiddlewaretoken: csrftoken,
                    planet_id: planet_id,
                    game_num: num,
                  },
            dataType: 'json',
        });
    });
}

$(document).ready(function(){
    planetDistribution();
    listPlanets();
    attackPlanet();
});
