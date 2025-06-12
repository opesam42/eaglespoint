from django.contrib import admin
from django.urls import path
from . import views

app_name = 'adminv2'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('listing/', views.listing, name="listing"),
    path('listing/add/', views.add_listing, name="add_listing"),
    path('listing/edit/<int:property_id>', views.edit_listing, name="edit-listing"),
    path('listing-search/<str:search_query>', views.search_listing, name="search_listing"),
    path('listing-search/', views.search_listing, name='search_listing_all'),
    path('listing/delete/<int:listing_id>', views.delete_listing, name="delete-listing"),

    path('user/', views.user_control_page, name="user-control-page"),
    path('get-users/', views.get_users, name='get-users'),
    path('user/toggle-admin/<int:user_id>', views.toggle_admin, name="toggle-admin"),
    path('user/info/<int:user_id>', views.user_info, name="user-info"),

    path('message/', views.message_page, name="message-page"),
    path('get-messages/', views.get_messages, name="get-messages"),
    path('get-messages/<int:message_id>/', views.get_messages, name="get-messages"),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete-message'),

    path('cms/', views.cms_admin_page, name='cms-page'),
    path('cms/testimonials/', views.testimonial_partial, name='testimonial-partial'),
    path('cms/testimonial-form/', views.render_testimonial_form, name='testimonial-form'),
    path('cms/update-testimonial-form/<int:id>',views.render_update_testimonial_form, name='update-testimonial-form'),

    path('cms/team/',views.team_partial, name='team-partial'),
    path('cms/team/create-form', views.render_add_member_form, name='add-member-form'),
    path('cms/team/edit-form/<int:id>', views.render_edit_member_form, name='edit-member-form'),

    path('cms/faqs/', views.faqs_partial, name='faqs-partial'),
    path('cms/faq/create-form', views.render_add_faq_form, name='add-faq-form'),
    path('cms/faq/update-form/<int:id>', views.render_update_faq_form, name='update-faq-form'),

    path('cms/partners/', views.partners_partial, name='partners-partial'),
    path('cms/partner/create-form', views.render_add_partner_form, name='add-partner-form'),
    path('cms/partner/update-form/<int:id>', views.render_update_partner_form, name='update-partner-form'),
    
    path('blog/', views.blog_index_page, name='blog-page'),
    path('blog/create-form', views.display_blog_form, name='display-blog-form'),
    path('blog/add', views.create_blog, name='create-blog'),
    path('blog/update-form/<int:id>', views.display_update_blog_form, name='display-update-blog-form'),
    path('blog/update/<int:id>', views.blog_update, name='update-blog'),
    path('blog/delete/<int:id>', views.delete_article, name='delete-article'),
    path('blog/publish/<int:id>', views.change_publish_status, name='change-publish-status'),

    
]
