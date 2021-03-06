from flask_navigation import Navigation

nav = Navigation()

nav.Bar('default_navbar', [
    nav.Item('Home', 'homepage.index'),
    nav.Item('Contact', 'homepage.contact'),
    nav.Item('Quiz', 'quiz.quiz_homepage', items=[
        nav.Item('Create Quiz', 'quiz.quiz_plans_page'),
        nav.Item('Browse Quiz', 'quiz.quiz_browse_page'),
    ]),
])

nav.Bar('user_navbar', [
    nav.Item('Admin Dashboard', 'admin.admin_dashboard',
                html_attrs={'icon-name': 'fas fa-tachometer-alt'}),
        nav.Item('Dashboard', 'user_dashboard.user_dashboard_page',
                 html_attrs={'icon-name': 'fas fa-tachometer-alt'}),
        nav.Item('Edit Profile', 'user.edit_user_profile',
                 html_attrs={'icon-name': 'fas fa-user-edit'}),
        nav.Item('Quiz', 'quiz.quiz_homepage',  html_attrs={'icon-name': 'fas fa-house-user'}, items=[
            nav.Item('Create Quiz', 'quiz.quiz_plans_page',
                     html_attrs={'icon-name': 'far fa-plus-square'}),
            nav.Item('Browse Quiz', 'quiz.quiz_browse_page',
                     html_attrs={'icon-name': 'fas fa-folder-open'})
        ]),
        nav.Item('Manage', '', items=[
            nav.Item('Owned Quiz', 'user_dashboard.user_quiz_owned',
                     html_attrs={'icon-name': 'fas fa-folder-open'}),
            nav.Item('Subscribed Quiz', 'user_dashboard.user_quiz_subscribed', html_attrs={
                     'icon-name': 'fas fa-folder-open'}),
            nav.Item('Hosting Quiz', 'user_dashboard.user_quiz_master',
                     html_attrs={'icon-name': 'fas fa-folder-open'})
        ])
        ])

nav.Bar('user_settings_navbar', [
        nav.Item('Profile', 'user.edit_user_profile'),
        # nav.Item('Change username', 'user.change_username'),
        nav.Item('Change password', 'user.change_password')
        ])

nav.Bar('user_topnavbar', [
        nav.Item('Settings', 'user.edit_user_profile'),
        nav.Item('Sign-out', 'user.logout')
        ])

nav.Bar('admin_sidenav', [
    nav.Item('Back to User Dashboard', 'user_dashboard.user_dashboard_page'),
    nav.Item('Admin Dashboard', 'admin.admin_dashboard'),
    nav.Item('Manage Users', 'admin.admin_dashboard', items=[
        nav.Item('Owners', 'admin.admin_user_quiz_owners'),
        nav.Item('Subscribers', 'admin.admin_dashboard'),
        nav.Item('Masters', 'admin.admin_dashboard')]),
    nav.Item('Manage Quizzes', 'admin.admin_dashboard', items=[
        nav.Item('Active Quizzes', 'admin.admin_dashboard'),
        nav.Item('Inactive Quizzes', 'admin.admin_dashboard')]),
    nav.Item('Payments', 'admin.admin_dashboard', items=[
        nav.Item('Orders', 'admin.admin_dashboard'),
        nav.Item('Refunds', 'admin.admin_dashboard')])
    ])
