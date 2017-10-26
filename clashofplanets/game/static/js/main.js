//LOBBY JS
//For getting CSRF token
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

var scrollFunction = function (idstring) {
    $('html, body').animate({
        scrollTop: $(idstring).offset().top
    }, 400);
};

function fillOutGame(game_num) {
    $('#JoinError').empty();
    $('#room_num').val(game_num);
    scrollFunction('.cardb');
    $('#planet_name').focus();
}

//List available games
function listGames() {
    var csrftoken2 = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken2},
        ifModified: true,
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
                            + '<td>' + glist[i].id + '</td>'
                            + '<td>' + glist[i].name + '</td>'
                            + '<td>' + glist[i].owner + '</td>'
                            + '<td>' + glist[i].connected_players + '</td>'
                            + '<td>' + glist[i].max_players + '</td>'
                            + '</tr>');
                        $("#openGames").append(buildListElementItem)
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
    //Create game is clicked
    $("#create").click(function (e) {
        console.log("creando");
        $("#join").prop('disabled', true);
        e.preventDefault();
        var csrftoken = getCookie('csrftoken');
        var pname = $('#planet_nameC').val();
        var rname = $('#game_nameC').val();
        var max_players = $('#max_playersC').val();
        //Ajax post
        $.ajax({
            type: 'POST',
            data: {csrfmiddlewaretoken: csrftoken, pname: pname, rname: rname, max_players: max_players},
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
        $("#create").attr('disabled', true);
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
            success: function (json) {
                //On success show the data posted to server as a message
                // alert(json.gameNumber);
                if (json.gameNumber == 0) {
                    window.location.href = 'GameClosed';
                }
                else if (json.gameNumber == -1) {
                    $('#JoinError').text("Sorry, that game doesn't exist.");
                }
                else if (json.gameNumber == -2) {
                    $('#JoinError').text("Sorry, that game is full of players.");
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
