$(function(){
	$('#dashboard-tabs a').click(function(e){
		e.preventDefault();
		if (!$(this).parent().hasClass('active')) {
			$('#dashboard-tabs li.active').removeClass('active');
			$('div.active').removeClass('active');
			$(this).parent().addClass('active');
			$('div.' + $(this).attr('rel')).addClass('active');
		}
	});		
});
