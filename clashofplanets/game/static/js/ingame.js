function timeStamp() {
    // Create a date object with the current time
    var now = new Date();
    // Create an array with the current month, day and time
    var date = [now.getMonth() + 1, now.getDate(), now.getFullYear()];
    // Create an array with the current hour, minute and second
    var time = [now.getHours(), now.getMinutes(), now.getSeconds()];
    // Determine AM or PM suffix based on the hour
    var suffix = ( time[0] < 12 ) ? "AM" : "PM";
    // Convert hour from military time
    time[0] = ( time[0] < 12 ) ? time[0] : time[0] - 12;
    // If hour is 0, set it to 12
    time[0] = time[0] || 12;
    // If seconds and minutes are less than 10, add a zero
    for (var i = 1; i < 3; i++) {
        if (time[i] < 10) {
            time[i] = "0" + time[i];
        }
    }
    // Return the formatted string
    //return date.join("/") + " " + time.join(":") + " " + suffix;
    return time.join(":") + " " + suffix;
}

var alert_show = true;
function listPlanets() {
    var timest = timeStamp();
    var msg = "";
    $.ajax({
        type: 'GET',
        url: "get_planets/",
        success: function (json) {
            var plist = json.planets;
            var user = json.user;
            var rst = json.game_status;
            $('#playerList').empty();
            for (var i = 0; i < plist.length; i++) {
                if (plist[i].owner == user) {
                    $('#mypopAvailable').empty();
                    $('#mymissilesAvailable').empty();
                    $('#pop_per_second').empty();
                    $('#shield_per_second').empty();
                    $('#missiles_per_second').empty();
                    $('#mypopAvailable').append(plist[i].pop);
                    $('#mymissilesAvailable').append(plist[i].missiles);
                    $('#pop_per_second').append(plist[i].pop_per_second+'/seg');
                    $('#shield_per_second').append(plist[i].shield_per_second+'/seg');
                    $('#missiles_per_second').append(plist[i].missiles_per_second+'/seg');

                    if (plist[i].is_alive == 0) {
                        // Writes message, disable attack
                        $('#attackError').empty();
                        $('#attackError').append("Your planet is dead!!!");
                        $('.attack-planet').prop("disabled",true);
                        $('.send-pop-planet').prop("disabled",true);
                    }
                    else {
                        if (plist[i].shield == 100) {
                            $('#shield_per_second').empty();
                            $('#shield_per_second').append('FULL');
                        }
                        if (plist[i].missiles < 1) { // Player doesnt have missiles to attack
                            // Writes message, disable attack
                            $('#attackError').empty();
                            $('#attackError').append("You dont have missiles to attack!!!");
                            $('.attack-planet').prop("disabled",true);
                        }
                        else { // Player has missiles, enable button again, delete msg on div
                            $('#attackError').empty();
                            $('.attack-planet').prop("disabled",false);
                        }
                        if (plist[i].pop <= 100) {
                            $('#attackError').empty();
                            $('#attackError').append("You need more than 100 pop to send!!!");
                            $('.send-pop-planet').prop("disabled",true);
                        }
                        else {
                            $('.send-pop-planet').prop("disabled",false);
                        }
                    }
                    $('#planet-' + plist[i].id + ' .tb_planet_pop').empty();
                    $('#planet-' + plist[i].id + ' .tb_planet_pop').append(plist[i].pop);
                    $('#planet-' + plist[i].id + ' .tb_planet_shield').empty();
                    $('#planet-' + plist[i].id + ' .tb_planet_shield').append(plist[i].shield);
                }
                else {
                    $('#planet-' + plist[i].id + ' .tb_planet_pop').empty();
                    $('#planet-' + plist[i].id + ' .tb_planet_pop').append(plist[i].pop);
                    $('#planet-' + plist[i].id + ' .tb_planet_shield').empty();
                    $('#planet-' + plist[i].id + ' .tb_planet_shield').append(plist[i].shield);
                    if (plist[i].is_alive == 0) {
                        var planet_id = plist[i].id
                        $('#planet-' + planet_id).find('.tb_attack_order').empty();
                        $('#planet-' + planet_id).find('.tb_attack_order').append('DEAD PLANET');
                    }
                }
            }
            if (rst && alert_show) {
                alert("Game Has Finished!!!");
                location.href = "stats/";
                alert_show = false;
            }
            setTimeout(listPlanets, 2000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        },
    });
}

function planetDistribution() {
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

function battleLog(linelog) {
    var consoleLine = "<p class=\"console-line\"></p>";
    console = {
        log: function (text) {
            $("#console-log").append($(consoleLine).html(text));
        }
    };
    console.log(linelog);
}

function changeDistribution() {
    var csrftoken = getCookie('csrftoken');
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
        },
        dataType: 'json',
    });
    battleLog('[' + timest + ']' + ' ' + '|' + ' ' + 'NRD' + ' ' + 'P:' + population + ' ' + 'S:' + shield + ' ' + 'M:' + missiles);
}

function attackPlanet() {
    $('.attack-planet').on("click", function (event) {
        event.preventDefault();
        var planet_id = $(this).closest('tr').find('td:nth-child(1)').text();
        //battleLog(planet_id); //Uncomment to check attack is working OK
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: "send_attack/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                planet_id: planet_id,
            },
        });
    });
}


function sendPopPlanet() {
    $('.send-pop-planet').on("click", function (event) {
        event.preventDefault();
        var planet_id = $(this).closest('tr').find('td:nth-child(1)').text();
        //battleLog(planet_id); //Uncomment to check attack is working OK
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: "send_pop/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                planet_id: planet_id,
            }
        });
    });
}

function missilesStatus(){
    $('#missilesStatus').on("click", function (event) {
        event.preventDefault();
        $.ajax({
            type: "GET",
            url: "missiles_status/",
            success: function (data) {
                if("error" in data){
                    battleLog(data['error']);
                }else if(Object.keys(data).length > 0){
                    for (var key in data) {
                        var line = data[key] + " missiles going to " + key;
                        battleLog(line);
                    }
                } else {
                    battleLog("No missiles in travel.");
                }
            }
        })
    })
}

$(document).ready(function () {
    listPlanets();
    planetDistribution();
    attackPlanet();
    sendPopPlanet();
    missilesStatus();
});
