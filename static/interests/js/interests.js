var interestlist = [];

function getInterestList() {
    var str_ids = "";
    interestlist.forEach(function(interest) {
	    str_ids += interest.id + ", ";
	});
    return str_ids.substr(0, str_ids.length-2);;
}
    
UpdateInterestList = function() {
    $('#interest-name-list').empty()
    $.each(interestlist, function(i, val) {
	    $('#interest-name-list').append($('<li/>').text(val.name))
	});
};
    
AddToInterestList = function(interest) {
    interest["priority"] = 1
    interestlist = interestlist.concat(interest)
    UpdateInterestList()
};
    
var sort_by = function(field, reverse, wrapperfunc){
    // wrapperfunc 
    var key = wrapperfunc ? 
    function(x) {return wrapperfunc(x[field])} : 
    function(x) {return x[field]};
    
    reverse = [-1, 1][+!!reverse];
    
    return function (a, b) {
	return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
    }
};
    
user_interests = getCurrentUserInterests();

user_interests.forEach(function(interest) {
	AddToInterestList(interest)		
	    });

$(".selectbtn").click(function(element) {
	jsn = JSON.parse(element.toElement.firstElementChild.textContent)
	    ids = $.map(interestlist, function(val, index) {return val.id})
	    if ((x = $.inArray(jsn.id, ids)) != -1) {
		interestlist[x]["priority"] += 1
		if (interestlist[x]["priority"] == 3) {
		    interestlist.splice(x, 1)
		} else {
		    interestlist.sort(sort_by('priority', false))
		}
	    } else {
		jsn["priority"] = 1
		    interestlist.push(jsn)
		    }
	
	UpdateInterestList()
	    });
    
    
// Section management functions
updateTitle = function(newtitle) {
    $(".topbar").text(newtitle)
};
    
updateNext = function(nextid) {
    $(".nextbutton").attr('href', '#' + nextid).removeAttr('disabled');
};
	
updatePrevious = function(nextid) {
    $(".previousbutton").attr('href', '#' + nextid).removeAttr('disabled');
};
	    
mainCategories = getMainCategories();
titles = [];
mainCategories.forEach(function(interest) {
	$('#' + interest.id + '_jump').waypoint({
		handler: function(direction) {
		    if (direction=="down") {
			nxt = this.next()
			    prv = this
			    titles.push(this.element)
			    } else {
			nxt = this
			    prv = this.previous()
			    titles.pop()
			    }
		    
		    if(nxt) {
			updateNext(nxt.element.id)
			    } else {
			$(".nextbutton").attr('disabled','disabled')
			    }
		    
		    if(prv) {
			updatePrevious(prv.element.id)
			    $("#" + prv.element.id.replace("jump", "btn"))
			    } else {
			$(".previousbutton").attr('disabled','disabled')
			    }
		    
		    if (titles.length > 0) { 
			newtitle = titles[titles.length - 1].getAttribute("name")
			    } else { newtitle = "" }
		    
		    updateTitle(newtitle)
			
			}
	    })
	    });
    
// Jumper functions
jumpFunction = function(e, element) {
    e.preventDefault();
    $("body, html").animate({ 
	    scrollTop: $( $(element).attr('href') ).offset().top 
		}, 600);
};
    
$(".jumper").on("click", function( e ) {
	jumpFunction(e, this);
    });

$(".nextbutton").on("click", function( e ) {
  	jumpFunction(e, this);
    });

$(".previousbutton").on("click", function( e ) {
  	jumpFunction(e, this);
    });

// TODO: Shamelessly copied and pasted from Diana's chat.js file...
// Should probably put it in its own common js file

// This function gets cookie with a given name
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
var csrftoken = getCookie('csrftoken');

/*
  The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	// or any other URL that isn't scheme relative or absolute i.e relative.
	!(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
	    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		// Send the token to same-origin, relative URLs only.
		// Send the token only if the method warrants CSRF protection
		// Using the CSRFToken value acquired earlier
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }}
    });

$("#sendinterests").click(function(event) {
	// TODO: Return id and priority only in the interest of speed?
	// var interests = $.map(interestlist, function(val, index) {return val.id val.priority})
	/*
	deferred = $.post("/interest/update/", {list: getInterestList()});
	console.log(interests);
	deferred.success(function (response) {
		debugger
		    });
	deferred.error(function (response) {
		debugger
		});*/
	$("#to_send_interest_list").val(getInterestList());
	
    });
    