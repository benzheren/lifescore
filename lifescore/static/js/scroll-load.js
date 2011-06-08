pageNum = 0;

var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop() > $(document).height() - ($(window).height()*3)) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).unbind('scroll');
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
    // If the next page doesn't exist, just quit now 
    //if (hasNextPage === false) {
    //    return false
    //}
    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    var url = "/friends_rank_fetch?start=" + (20 * pageNum) + '&fb_id=508406568';
    $.ajax({
        url: url, 
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            //hasNextPage = data.hasNext;
            // Loop through all items
	    console.log('success');
            var html = [];
            $.each(data, function(index, item){
                /* Format the item in our HTML style */
		html.push('<li class="row"><ul class="lb-row"><li class="lb-rank"><img class="smallpic" src="http://graph.facebook.com/', item.fb_id, '/picture?type=square"/></li><li class="lb-name">', item.name, '</li><li class="lb-score">', item.score, "</li></ul></li>");
            });
            // Pop all our items out into the page
            $("#leaderboard").append(html.join(""));
	    console.log('hello');
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        }
    });
};

$(document).ready(function(){     
   $(window).bind('scroll', loadOnScroll);
});

