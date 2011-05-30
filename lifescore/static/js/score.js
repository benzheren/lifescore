$(function() {
	console.log('yes');
	
	$("a[href='friends']").click(function() {
	
		 $('#leaderboard2>li').tsort({attr:"value"});  
		alert('yes');

	 	return false;
	});

	
});


