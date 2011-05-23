<%inherit file="base.mak"/>
${fb_id}
% if friends_id:
	<script type="text/javascript">
		var friends_id = ${friends_id.__repr__()|n}.split(","),
		    length = friends_id.length,
		    size = friends_id.length/20,
		    i = 0;

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

		function fetch_friends_callback(data) {
			
		}
	</script>
% endif
