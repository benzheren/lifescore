$(function() {
	
	$("a").click(function(e) {
		e.preventDefault();
		e.stopPropagation();
		/*
		$('#leaderboard>li').fadeOut();  
		 $('#leaderboard>li').tsort({attr:"value",order:"desc"})
		 $('#leaderboard>li').each(function(index) {
    		$(this).delay(100*index).fadeIn(300);
		});  
		*/
		
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
      duration: 400,
      easing: 'easeInOutQuad',
	  attribute: 'id'
    });
		//Given two list, cycle through and insert items where appropriate
		
		//get max value of the list
		
		//if max is not in the 
		

	});

	
});

