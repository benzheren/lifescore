<%inherit file="base.mak"/>
<div>
	<fb:login-button perms="${facebook_perms}">Connect Your Facebook Account</fb:login-button>
</div>
<div id="fb-root"></div>
<script>
	window.fbAsyncInit = function() {
		FB.init({appId: '${facebook_app_id}', status: true, cookie: true,
                	xfbml: true});
	};

   	(function() {
        	var e = document.createElement('script');
        	e.type = 'text/javascript';
        	e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
        	e.async = true;
        	document.getElementById('fb-root').appendChild(e);
    	}());	
</script>
