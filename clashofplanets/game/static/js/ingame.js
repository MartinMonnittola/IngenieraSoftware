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
				}
			setTimeout(listPlanets, 3000);
		},
		error : function(xhr,errmsg,err) {
			console.log(xhr.status + ": " + xhr.responseText);
		},
	});
}

$(document).ready(function(){
	listPlanets();
});
