function listPlayers() {
    $.ajax({
        type: 'GET',
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
                        + '<td>' + plist[i].alliance + '</td>'
                        + '</tr>');
                }
            }
            setTimeout(listPlayers, 2000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        },
    });
}

function gameState() {
    $.ajax({
        type: 'GET',
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
                location.href = "game/";
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
