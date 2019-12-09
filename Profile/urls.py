from django.urls import path

from .import views

app_name = 'Profile'

urlpatterns = [
        path('', views.ProfileHome, name="ProfileHome"),
        path('view/<int:profile_id>/', views.ProfileView, name="ProfileView"),
        path('edit/<int:profile_id>/', views.ProfileEditView, name="ProfileEdit"),
        path('email/<int:profile_id>/', views.EmailEditView, name='EmailEdit'),
        path('email/<int:profile_id>/<int:email_id>/', views.EmailStatusView, name='EmailStatus'),
        path('address/physical/<int:profile_id>/', views.PhysicalAddressView, name='PhysicalAddress'),
        path('address/postal/<int:profile_id>/', views.PostalAddressView, name='PostalAddress'),
        path('phone/add/<int:profile_id>/', views.PhoneNumberAdd, name='PhoneNumberAdd'),
        path('online/add/<int:profile_id>/', views.OnlineProfileAdd, name='OnlineProfileAdd'),
        path('popup/add/', views.ProfileTypePopup, name="ProfileTypeAddPop"),
        path('popup/ajax/get_site_id/', views.get_SiteType_id, name="AJAX_GetSiteTypeID"),
        path('file/<int:profile_id>/', views.FileUploadView, name='FileUploadView'),
        path('id/<int:profile_id>/', views.IdentificationView, name='IdView'),
        path('popup/add/idtype/', views.IdTypePopup, name="IdTypeAddPop"),
        path('popup/ajax/get_IdType_id/', views.get_IdType_id, name="AJAX_GetIdTypeID"),
        path('passport/<int:profile_id>/', views.PassportAddView, name='PassportAddView'),
        path('passport/<int:p_id>/<int:profile_id>/edit/', views.PassportEditView, name='PassportEditView'),
        path('language/<int:profile_id>/', views.LanguageAddView, name='LanguageAdd'),
        path('popup/add/language/', views.LanguagePopup, name="LanguagePop"),
        path('popup/ajax/get_language_id/', views.get_language_id, name="AJAX_GetLanguageID"),
        path('language/<int:profile_id>/<int:lang_id>/', views.LanguageEditView, name='LanguageEdit'),
        path('online/delete/<int:pk>/', views.OnlineDelete, name='OnlineDelete'),
        path('passport/delete/<int:pk>/', views.PassportDeleteView, name='PassportDelete'),
        path('phonenumber/delete/<int:pk>/', views.PhoneNumberDelete, name='PhoneDelete'),
        path('file/delete/<int:pk>/', views.FileDelete, name='FileDelete'),
        path('email/delete/<int:pk>/', views.EmailDelete, name='EmailDelete'),
        path('experience-review/', views.ConfirmView, name='Confirm'),
        path('lecturer-confirm/<int:pk>/', views.LecturerConfirmView, name='LecturerConfirm'),
        path('lecturer-reject/<int:pk>/', views.LecturerRejectView, name='LecturerReject'),
        path('lecturer-comment/<int:pk>/', views.LecturerCommentView, name='LecturerComment'),
        path('lecturer-wrongperson/<int:pk>/', views.LecturerWrongPersonView, name='LecturerWrongPerson'),
        path('classmates-confirm/<int:pk>/', views.ClassMatesConfirmView, name='ClassMatesConfirm'),
        path('classmates-reject/<int:pk>/', views.ClassMatesRejectView, name='ClassMatesReject'),
        path('classmates-comment/<int:pk>/', views.ClassMatesCommentView, name='ClassMatesComment'),
        path('classmates-wrongperson/<int:pk>/', views.ClassMatesWrongPersonView, name='ClassMatesWrongPerson'),
        #Colleague Confirm
        path('colleague-confirm/<int:pk>/', views.ColleagueConfirmView, name='ColleagueConfirm'),
        path('colleague-reject/<int:pk>/', views.ColleagueRejectView, name='ColleagueReject'),
        path('colleague-wrongperson/<int:pk>/', views.ColleagueWrongPersonView, name='ColleagueWrongPerson'),
        path('colleague-comment/<int:pk>/', views.ColleagueCommentView, name='ColleagueComment'),
        #Superior Confirm
        path('superior-confirm/<int:pk>/', views.SuperiorConfirmView, name='SuperiorConfirm'),
        path('superior-reject/<int:pk>/', views.SuperiorRejectView, name='SuperiorReject'),
        path('superior-wrongperson/<int:pk>/', views.SuperiorWrongPersonView, name='SuperiorWrongPerson'),
        path('superior-comment/<int:pk>/', views.SuperiorCommentView, name='SuperiorComment'),
        #Collaborator confirm
        path('collaborator-confirm/<int:pk>/', views.CollaboratorConfirmView, name='CollaboratorConfirm'),
        path('collaborator-reject/<int:pk>/', views.CollaboratorRejectView, name='CollaboratorReject'),
        path('collaborator-wrongperson/<int:pk>/', views.CollaboratorWrongPersonView, name='CollaboratorWrongPerson'),
        path('collaborator-comment/<int:pk>/', views.CollaboratorCommentView, name='CollaboratorComment'),
        #Client Confirm
        path('client-confirm/<int:pk>/', views.ClientConfirmView, name='ClientConfirm'),
        path('client-reject/<int:pk>/', views.ClientRejectView, name='ClientReject'),
        path('client-wrongperson/<int:pk>/', views.ClientWrongPersonView, name='ClientWrongPerson'),
        path('client-comment/<int:pk>/', views.ClientCommentView, name='ClientComment'),
        #PreColleague Confirm
        path('precolleague-confirm/<int:pk>/', views.PreColleagueConfirmView, name='PreColleagueConfirm'),
        path('precolleague-reject/<int:pk>/', views.PreColleagueRejectView, name='PreColleagueReject'),
        path('precolleague-wrongperson/<int:pk>/', views.PreColleagueWrongPersonView, name='PreColleagueWrongPerson'),
        path('precolleague-comment/<int:pk>/', views.PreColleagueCommentView, name='PreColleagueComment'),
        path('careerhistory/', views.BriefCareerHistoryView, name='History'),

]
