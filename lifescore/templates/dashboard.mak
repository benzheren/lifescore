<%inherit file="base.mak"/>
${fb_id}
<div id="rank"></div>



<div class="wrapper container">
	
	<div class="left span-3">
		<div class="pic-outer">
			<div class="pic-inner">
				<img class="pic" src="http://profile.ak.fbcdn.net/hprofile-ak-snc4/174503_10037093_2768946_n.jpg" />
			</div>
		</div>
	</div>
	
	<div class="right span-17 prepend-1">
		<div class="paper">
			<h1 class="name">Alexander Timothy</h1>
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
					<li id="id1" class="row" value="500">
						<ul class="lb-row">
							<li class="lb-rank">#1</li>
							<li class="lb-name">Ben Hu</li>
							<li class="lb-score">500</li>
						</ul>
					</li>
                    
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

		function fetch_friends(ids) {
			$.ajax({
			url: '/fetch_friends',
			data: {friends_id: ids.toString(), fb_id: '${fb_id}'},
			dataType: 'json',
			success: fetch_friends_callback
			});	
		}
		
		var friends = '';
		
		function fetch_friends_callback(data) {
			$.each(data, function(index, value){
				
						friends += 	'<li id="'+value.id+'" class="row" value="'+index+'">'
								+  	'<ul class="lb-row">'
								+  	'<li class="lb-rank">'+index+'</li>'
								+	'<li class="lb-name">Ben Hu</li>'
								+	'<li class="lb-score">500</li>'
								+	'</ul></li>';
						
				
			});
			$('#leaderboard').append($friends)	
		}
	</script>
% endif
