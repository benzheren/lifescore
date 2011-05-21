<%inherit file="base.mak"/>
${fb_id}
% if friends_id:
	<script type="text/javascript">
		var friends_id = "${friends_id.__repr__()|n}".split(",");
		var length = friends_id.length;
		var size = friends_id.length/20;
		for (var i=0; i<=size; i++) {
			if ((i+1) * 20 > length) {
				//console.log(friends_id.slice(20 * i, length));
			} else {
				//console.log(friends_id.slice(20 * i, 20 * (i+1)));
			}
		}	
	</script>
% endif
