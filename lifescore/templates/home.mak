<%inherit file="base.mak"/>
% if dashboard_url:
	<div>
		<a href="${dashboard_url}">go to your score</a>
	</div>
% else:
	<div>
		<fb:login-button perms="${facebook_perms}">Connect Your Facebook Account</fb:login-button>
	</div>
% endif

<div id="fb-root"></div>
<script>
	window.fbAsyncInit = function() {
		FB.init({appId: '${facebook_app_id}', status: true, cookie: true,
			xfbml: true});
		FB.Event.subscribe('auth.login', function(response) {
			FB.api('/me', function(response){
				window.location.replace('/' + response.id);
			});
		});
	};

   	(function() {
        	var e = document.createElement('script');
        	e.type = 'text/javascript';
        	e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
        	e.async = true;
        	document.getElementById('fb-root').appendChild(e);
    	}());	
</script>
