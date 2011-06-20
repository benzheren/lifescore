$(function() {
	var pageNum = 1;
	
	$('.sticky').ajaxStart(function() {
		$(this).show();
		$(window).unbind('scroll');
	}).ajaxStop(function() { 
		$(this).hide();
		$(window).bind('scroll', loadOnScroll);
	});
	
if(size) {
	for (var i=0; i<=size; i++) {
		if ((i+1) * 20 > friends_id.length) {
			fetch_friends(friends_id.slice(20 * i, friends_id.length));
			
		} else {
			fetch_friends(friends_id.slice(20 * i, 20 * (i+1)));
		}	
	}
} else {
	pageNum = 0;
	fetch_more_friends();
}



function fetch_more_friends() {
	pageNum = pageNum + 1;
    // Configure the url we're about to hit
    $.ajaxq("addqueue", {
        url: "/friends_rank_fetch", 
    	data: {start: (10 * pageNum), num: 10, fb_id: profile_id},
		dataType: 'json',
        success: add_more_friends,
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        }
    });
}


var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop()+100 >= ($(document).height() - ($(window).height()))) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).unbind('scroll');
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        fetch_more_friends();
    }
};

function add_more_friends(data) {
		var $topfriends = '';
	$.each(data, function(index, value){
			$topfriends += '<li id="'+value.fb_id+'" class="row" value="'+value.score+'">'
						+  	'<ul class="lb-row">'
						+  	'<li class="lb-rank">'+(index+(pageNum*10)+1)+'.</li>'
						+  	'<li class="lb-pic"><a href="http://facebook.com/profile.php?id='+value.fb_id+'"><img class="smallpic" src="http://graph.facebook.com/'+value.fb_id+'/picture?type=square" /></a></li>'
						+	'<li class="lb-name">'+value.name+'</li>'
						+	'<li class="lb-score">'+value.score+'</li>'
						+	'</ul></li>';	
	});
	$leaderboard.append($topfriends);
	var lbheight = ($leaderboard.children().length * 50)
	$leaderboard.animate({height: lbheight}, 800);

}

function fetch_friends(ids) {
	$.ajaxq("friendsqueue",{
		url: '/fetch_friends',
		data: {friends_id: ids.toString(), fb_id: profile_id},
		dataType: 'json',
		async: true,
		success: fetch_friends_callback
	});
}
var $leaderboard = $('#leaderboard');
function fetch_friends_callback(data) {
	var $topfriends = '';
	
	$.each(data, function(index, value){
			$topfriends += '<li id="'+value.id+'" class="row" value="'+value.score+'">'
						+  	'<ul class="lb-row">'
						+  	'<li class="lb-rank">'+(index+1)+'.</li>'
						+  	'<li class="lb-pic"><a href="http://facebook.com/profile.php?id='+value.id+'"><img class="smallpic" src="http://graph.facebook.com/'+value.id+'/picture?type=square" /></a></li>'
						+	'<li class="lb-name">'+value.name+'</li>'
						+	'<li class="lb-score">'+value.score+'</li>'
						+	'</ul></li>';	
	});
	
	$leaderboard.quicksand($topfriends, {
		duration: 800,
		easing: 'easeInOutQuad',
		attribute: 'id'
	});
	
	/*deprecated
	$leaderboard.append(topfriends);
	
	//$('#leaderboard>li').tsort({order:"desc",attr:"value"})
	
	sort_friends($topfriends);
	//$leaderboard.animate({height: lbheight}, 800 );
	
	$('.more').show();
	*/
}

/* Deprecated based on old ways
function sort_friends(destination){

	// get the first collection
	var $applications = $('#leaderboard>li');

	// clone applications to get a second collection
	var $data = $applications.clone();

	var $sortedData = $data.sorted({
	by: function(v) {
	  return parseFloat($(v).attr('value'));
		}
	});	
	
	
	$leaderboard.quicksand($sortedData, {
		duration: 800,
		easing: 'easeInOutQuad',
		attribute: 'id'
	});
	
} */

});
