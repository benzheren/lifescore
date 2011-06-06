$(function() {
	
	$('.sticky').ajaxStart(function() {$(this).show(); }).ajaxStop(function() { $(this).hide();});
	
	var lbheight = 500;
	var $leaderboard = $('#leaderboard');
	
	$('.more a').click(function(e) {
		
		if(($leaderboard.children().size()*50	) > lbheight) {
			lbheight += 500;
			$leaderboard.animate({height: lbheight}, 800 );
		} else {
			
		}
		e.preventDefault();
	});
	
if(size) {
	
	for (var i=0; i<=size; i++) {
		if ((i+1) * 20 > length) {
			fetch_friends(friends_id.slice(20 * i, length));
			
		} else {
			fetch_friends(friends_id.slice(20 * i, 20 * (i+1)));
			
		}	
	}
		
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

function fetch_friends_callback(data) {
	var topfriends = '';
	$.each(data, function(index, value){
			var friend = '<li id="'+value.id+'" class="row" value="'+value.score+'">'
						+  	'<ul class="lb-row">'
						+  	'<li class="lb-rank"><img class="smallpic" src="http://graph.facebook.com/'+value.id+'/picture?type=square" /></li>'
						+	'<li class="lb-name">'+value.id+'</li>'
						+	'<li class="lb-score">'+value.score+'</li>'
						+	'</ul></li>';	
			topfriends += friend;
	});
	
	$leaderboard.append(topfriends);
	
	//$('#leaderboard>li').tsort({order:"desc",attr:"value"})
	
	sort_friends();
	$leaderboard.animate({height: lbheight}, 800 );;
	
	$('.more').show();
}


function sort_friends(){

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
	
	
}
	

});