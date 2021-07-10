from flask_navigation import Navigation

nav = Navigation()

nav.Bar('default_navbar',[
nav.Item('Home', 'homepage.index'),
nav.Item('Contact', 'homepage.contact'),
nav.Item('Quiz', 'quiz.quiz_homepage', items=[
	nav.Item('Create Quiz', 'quiz.quiz_plans_page'),
	nav.Item('Browse Quiz', 'quiz.quiz_browse_page'),
]),
])

nav.Bar('user_navbar', [
	nav.Item('Dashboard', 'user_dashboard.user_dashboard_page', html_attrs={'icon-name': 'fas fa-tachometer-alt'}),
	nav.Item('Edit Profile', 'user.edit_user_profile'),
	nav.Item('Quiz', 'quiz.quiz_homepage', items=[
			nav.Item('Create Quiz', 'quiz.quiz_plans_page', html_attrs={'icon-name': 'fas fa-tachometer-alt'}),
			nav.Item('Browse Quiz', 'quiz.quiz_browse_page')
		]),
	nav.Item('Manage', '', items=[
		nav.Item('Owned Quiz', 'user_dashboard.user_quiz_owned'),
		nav.Item('Subscribed Quiz', 'user_dashboard.user_quiz_subscribed'),
		nav.Item('Hosting Quiz', 'user_dashboard.user_quiz_master')
		])
])

nav.Bar('user_settings_navbar', [
	nav.Item('Profile', 'user.edit_user_profile'),
	nav.Item('Change username', 'user.change_username'),
	nav.Item('Change password', 'user.change_password'),
	nav.Item('Manage emails', 'user.manage_emails')
])

nav.Bar('user_topnavbar', [
	nav.Item('Settings', 'user_dashboard.user_settings_page'),
	nav.Item('Sign-out', 'user.logout')
])