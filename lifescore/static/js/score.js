$(function() {
	console.log('yes');
	
	$("a[href='friends']").click(function() {
	alert('yes');
		 $('#leaderboard > li').tsort({attr:"value"});  
	 	return false;
	});

	
});