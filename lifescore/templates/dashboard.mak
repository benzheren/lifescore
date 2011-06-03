<%inherit file="base.mak"/>
<div id="rank"></div>
<div class="wrapper container">
	
	<div class="left span-3">
		<div class="pic-outer">
			<div class="pic-inner">
				<img class="pic" src="http://graph.facebook.com/${profile['id']}/picture?type=large" />
			</div>
		</div>
		<div class="sticky">loading...</div>
	</div>
	
	<div class="right span-17 prepend-1">
		<div class="paper">
			<h1 class="name">${profile['name']}</h1>
			<h3 class="subs">${profile['location']['name']}</h3>
			<h3 class="subs">school: ${profile['education'][1]['school']['name']}</h3>
			<h3 class="subs">work: ${profile['work'][0]['employer']['name']}</h3>
			
			<div class="score"><h2>750</h2></div>
		</div>
		
	</div>
	
	<div class="main span-17 prepend-3">
		<div class="folders">
			<ul class="tabs">
				<li><a href="">Head 2 Head</a></li>
				<li class="active"><a href="">Your Friends</a></li>
				<li><a href="">World Wide Scores</a></li>

			</ul>
			<div class="contents">
				
				<ul class="leaderboard" id="leaderboard">
				</ul>
				<ul class="leaderboard" id="otherboard">
				</ul>
				
                <div class="lines"></div><div class="lines"></div>
                <div class="clear"></div>
			</div>	
		</div>
	
	</div>


</div>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
<script type="text/javascript" src="../../static/js/jquery.plugins.js"></script>
<script type="text/javascript" src="../../static/js/jquery.quicksand.js"></script>
<script type="text/javascript" src="../../static/js/score.js"></script>

% if friends_id:
	<script type="text/javascript">
		var friends_id = ${friends_id.__repr__()|n}.split(","),
		    length = friends_id.length,
		    size = friends_id.length/20;
		
		for (var i=0; i<=size; i++) {
			if ((i+1) * 20 > length) {
				fetch_friends(friends_id.slice(20 * i, length));
			} else {
				fetch_friends(friends_id.slice(20 * i, 20 * (i+1)));
			}	
		}
		
		$.ajaxStart(function() { $('.sticky').show(); })
		$.ajaxStop(function() { $('.sticky').hide(); });

		function fetch_friends(ids) {
			$.ajaxq("testqueue",{
				url: '/fetch_friends',
				data: {friends_id: ids.toString(), fb_id: '${profile['id']}'},
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
			
			$('#leaderboard').append(topfriends);
			
			//$('#leaderboard>li').tsort({order:"desc",attr:"value"})
			
			sort_friends();
			$('#leaderboard .row:eq(5)').nextAll().remove();
			$('#leaderboard').animate({height: "500px"}, 800 );;
			
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
			
			$('#leaderboard').quicksand($sortedData, {
				duration: 800,
				easing: 'easeInOutQuad',
				attribute: 'id'
			});
		}
	</script>
% endif
