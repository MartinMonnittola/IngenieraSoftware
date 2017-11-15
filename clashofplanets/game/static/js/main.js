function fillOutGame(game_num) {
    $('#JoinError').empty();
    $('#game_num').val(game_num);
    $('#planet_name').focus();
}

var gaps = [1];
function transform(num) {
    var pos = gaps.indexOf(num);
    // skip value from gaps array
    if (pos !== -1) {
        return num - 1;
    }
    return num;
}

function max_Players_slider() {
    var $range = $(".max_playersC-slider");
    $range.ionRangeSlider({
        type: 'single',
        min: 2,
        max: 50,
        from: 2,
    });
    var slider = $(".max_playersC-slider").data("ionRangeSlider");
    $(".range-slider-players").mouseleave(function(){
      slider.dragging = false;
    });
}

function num_Alliances_slider() {
    var $range = $(".num_alliancesC-slider");
    $range.ionRangeSlider({
        type: 'single',
        min: 1,
        max: 10,
        from: 1,
        prettify: function(num) {
            return transform(num);
        },
    });
    var slider = $(".num_alliancesC-slider").data("ionRangeSlider");
    $(".range-slider-alliances").mouseleave(function(){
      slider.dragging = false;
    });
}

function num_Bots_slider() {
    var $range = $(".bot_playersC-slider");
    $range.ionRangeSlider({
        type: 'single',
        min: 1,
        max: 10,
        from: 1,
        prettify: function(num) {
            return transform(num);
        },
    });
    var slider = $(".bot_playersC-slider").data("ionRangeSlider");
    $(".range-slider-bots").mouseleave(function(){
      slider.dragging = false;
    });
}

//List available games
function listGames() {
    $.ajax({
        type: 'GET',
        url: "get_games/",
        success: function (json) {
            if (status != "notmodified") {
                //console.log(json);
                var glist = json.games;
                //alert(clist);
                $('#openGames').empty();
                $('#rooms_list').empty();
                if ((glist.length) > 0) {
                    for (var i = 0; i < glist.length; i++) {
                        var num = glist[i];
                        buildListElementItem = $(
                            '<tr>'
                            + '<td class=\"game-'+glist[i].id+'\">' + glist[i].id + '</td>'
                            + '<td>' + glist[i].name + '</td>'
                            + '<td>' + glist[i].owner + '</td>'
                            + '<td>' + glist[i].num_alliances + '</td>'
                            + '<td>' + glist[i].connected_players + '</td>'
                            + '<td>' + glist[i].max_players + '</td>'
                            + '</tr>');
                        $("#openGames").append(buildListElementItem)
                        $(".game-"+glist[i].id).bind('click', function (){
                            fillOutGame($(this).text());
                        });
                    }
                }
                else {
                    buildListElementItem = $('<p>No open rooms were found.</p>');
                    $("#rooms_list").append(buildListElementItem)
                }
            }
            setTimeout(listGames, 4000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

//For doing AJAX post
$(document).ready(function () {
    listGames();
    max_Players_slider();
    num_Alliances_slider();
    num_Bots_slider();

    //Create game is clicked
    $("#create").click(function (e) {
        console.log("creando");
        $("#join").prop('disabled', true);
        e.preventDefault();
        var csrftoken = getCookie('csrftoken');
        var pname = $('#planet_nameC').val();
        var rname = $('#game_nameC').val();
        var max_players = $('#max_playersC').val();
        var bot_players = $('#bot_playersC').val();
        var num_alliances = $('#num_alliancesC').val();
        var game_mode = $('#game_modesC').text();
        //Ajax post
        $.ajax({
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken,
                pname: pname,
                rname: rname,
                max_players: max_players,
                bot_players: bot_players,
                num_alliances: num_alliances,
                game_mode: game_mode,
            },
            url: 'make_game/',
            success: function (json) {
                //console.log(json);
                window.location.href = json.gameNumber;
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
    //When join is clicked
    $("#join").click(function (e) {
        //$("#create").attr('disabled', true);
        //Prevent default submit. Must for Ajax post.Beginner's pit.
        e.preventDefault();
        //Prepare csrf token
        var csrftoken = getCookie('csrftoken');
        //Collect data from fields
        var pname = $('#planet_name').val();
        var num = $('#game_num').val();
        //Send data
        $.ajax({
            type: 'POST', // http method
            data: {csrfmiddlewaretoken: csrftoken, pname: pname, num: num},
            url: 'make_player/',// data sent with the post request
            // handle a successful response
            /**
            * @param json - JSON response.
            * @param json.gameNumber - Displays the game number to join, or
             * error status code.
            */
            success: function (json) {
                //On success show the data posted to server as a message
                // alert(json.gameNumber);
                if (json.gameNumber === 0) {
                    window.location.href = 'GameClosed';
                }
                else if (parseInt(json.gameNumber) === -1) {
                    $('#JoinError').text("Sorry, that game doesn't exist.");
                }
                else if (parseInt(json.gameNumber) === -2) {
                    $('#JoinError').text("Sorry, that game is full of players.");
                }
                else if (parseInt(json.gameNumber) === -3){
                    $('#JoinError').text("Sorry, you are already playing" +
                        " another game.");
                }
                else {
                    $("#join").prop('disabled', true);
                    window.location.href = json.gameNumber;
                }
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
});
