<%inherit file="base.mak"/>
<div id="rank"></div>
<div class="wrapper container">
	
	<div class="left span-6">
		<div class="pic-outer">
			<div class="pic-inner">
				<img class="pic" src="http://graph.facebook.com/${profile['id']}/picture?type=large" />
			</div>
		</div>
		<div class="sticky"><img src="../../static/images/loading-arrows.gif" class="loading" />loading...</div>
	</div>
	
	<div class="right span-17">
		
		<div class="paper">
			<h1 class="name">${profile['name']}</h1>
			<h3 class="subs">${profile['location']['name']}</h3>
			<h3 class="subs">school: ${profile['education'][1]['school']['name']}</h3>
			<h3 class="subs">work: ${profile['work'][0]['employer']['name']}</h3>
			
			<div class="your-score">your score</div>
			
			<div class="score"><h2>750</h2></div>
		</div>
		
		<div class="share">
			<a href="" title="facebook"></a>
			<a href="" title="twitter"></a>
			<a href="" title="google"></a>
			<a href="" title="technorati"></a>
			<a href="" title="reddit"></a>
			<a href="" title="yahoo"></a>
			<a href="" title="delicious"></a>
		</div>
		
		<div class="folders">
			<ul class="tabs">
				<li><a href="">Head 2 Head</a></li>
				<li class="active"><a href="">Your Friends</a></li>
				<li><a href="">World Wide Scores</a></li>

			</ul>
			<div class="contents friends active">
				<ul class="leaderboard" id="leaderboard">
				</ul>
				<div class="leaderboard">
					<div class="more"><a href="more">show more</a></div>
				</div>
								
				
                <div class="lines"></div><div class="lines"></div>
                <div class="clear"></div>
			</div>
			<div class="contents world">
				<ul class="leaderboard" id="leaderboard">
				</ul>
				<div class="leaderboard">
					<div class="more"><a href="more">show more</a></div>
				</div>
                <div class="lines"></div><div class="lines"></div>
                <div class="clear"></div>
			</div>
			<div class="contents world">
				<ul class="leaderboard" id="leaderboard">
				</ul>
				<div class="leaderboard">
					<div class="more"><a href="more">show more</a></div>
				</div>
                <div class="lines"></div><div class="lines"></div>
                <div class="clear"></div>
			</div>
		</div>
		
	</div>

</div>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
<script type="text/javascript" src="../../static/js/jquery.plugins.js"></script>
<script type="text/javascript" src="../../static/js/jquery.quicksand.js"></script>
% if friends_id:
	<script type="text/javascript">
		var friends_id = ${friends_id.__repr__()|n}.split(","),
		    length = friends_id.length,
		    size = friends_id.length/20;
		var profile_id = ${profile["id"]};
	</script>
% endif

<script type="text/javascript" src="../../static/js/score.js"></script>

