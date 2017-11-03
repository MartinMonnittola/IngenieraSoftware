function listPlayers() {
    var csrftoken = getCookie('csrftoken');
    var num = $('#gamenum').text();
    $.ajax({
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken, num: num},
        ifModified: true,
        url: "get_planets/",
        success: function (json) {
            if (status != "notmodified") {
                var plist = json.planets;
                $('#playerList').empty();
                for (var i = 0; i < plist.length; i++) {
                    $('#playerList').append(
                        '<tr>'
                        + '<td>' + plist[i].id + '</td>'
                        + '<td>' + plist[i].name + '</td>'
                        + '<td>' + plist[i].owner + '</td>'
                        + '</tr>');
                }
            }
            setTimeout(listPlayers, 4000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        },
    });
}

function gameState() {
    var csrftoken = getCookie('csrftoken');
    var num = $('#gamenum').text();
    $.ajax({
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken, num: num},
        url: "get_game_state/",
        success: function (json) {
            if (json.players_in_room < 2) {
                $(".start-game-btn").prop('disabled', true);
                $('#StartGameError').text("You can't start the game with less than 2 players.");
            }
            else {
                $(".start-game-btn").prop('disabled', false);
                $('#StartGameError').text("");
            }

            var rst = json.game_state;
            if (rst == 1) {
                alert("Game has been started!!!");
                location.href = "/game_rooms/game/" + num;
            }
            setTimeout(gameState, 4000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        },
    });
}

$(document).ready(function () {
    listPlayers();
    gameState();
});
