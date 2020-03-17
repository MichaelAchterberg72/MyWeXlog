from django.urls import path

from .import views

app_name = 'Profile'

urlpatterns = [
        path('', views.ProfileHome, name="ProfileHome"),
        path('view/<slug:tlt>/', views.ProfileView, name="ProfileView"),
        path('edit/<slug:tlt>/', views.ProfileEditView, name="ProfileEdit"),
        path('email/<slug:tlt>/', views.EmailEditView, name='EmailEdit'),
        path('email/<slug:tlt>/<slug:eml>/', views.EmailStatusView, name='EmailStatus'),
        path('email/delete/<int:pk>/<slug:tlt>/', views.EmailDelete, name='EmailDelete'),

        path('address/physical/', views.PhysicalAddressView, name='PhysicalAddress'),

        path('address/postal/', views.PostalAddressView, name='PostalAddress'),

        path('phone/add/', views.PhoneNumberAdd, name='PhoneNumberAdd'),

        path('online/add/<slug:tlt>/', views.OnlineProfileAdd, name='OnlineProfileAdd'),
        path('online/delete/<int:pk>/<slug:tlt>/', views.OnlineDelete, name='OnlineDelete'),
        path('popup/add/', views.ProfileTypePopup, name="ProfileTypeAddPop"),
        path('popup/ajax/get_site_id/', views.get_SiteType_id, name="AJAX_GetSiteTypeID"),
        path('file/pftp/', views.FileUploadView, name='FileUploadView'),
        path('id/update/', views.IdentificationView, name='IdView'),
        path('popup/add/idtype/', views.IdTypePopup, name="IdTypeAddPop"),
        path('popup/ajax/get_IdType_id/', views.get_IdType_id, name="AJAX_GetIdTypeID"),
        path('passport/', views.PassportAddView, name='PassportAddView'),
        path('passport/<slug:psp>/<slug:tlt>/edit/', views.PassportEditView, name='PassportEditView'),
        path('language/<slug:tlt>/', views.LanguageAddView, name='LanguageAdd'),
        path('language/<slug:tlt>/<slug:lang>/', views.LanguageEditView, name='LanguageEdit'),
        path('language-del/<int:lang_id>/<slug:tlt>/', views.LanguageDeleteView, name='LanguageDelete'),
        path('popup/add/language/', views.LanguagePopup, name="LanguagePop"),
        path('popup/ajax/get_language_id/', views.get_language_id, name="AJAX_GetLanguageID"),
        path('passport/delete/<int:pk>/<slug:tlt>/', views.PassportDeleteView, name='PassportDelete'),
        path('phonenumber/delete/<int:pk>/', views.PhoneNumberDelete, name='PhoneDelete'),
        path('file/delete/<int:pk>/', views.FileDelete, name='FileDelete'),
        path('experience-review/', views.ConfirmView, name='Confirm'),
        path('lecturer-confirm/<int:pk>/', views.LecturerConfirmView, name='LecturerConfirm'),
        path('lecturer-reject/<int:pk>/', views.LecturerRejectView, name='LecturerReject'),
        path('lecturer-comment/<slug:lct>/', views.LecturerCommentView, name='LecturerComment'),
        path('lecturer-wrongperson/<int:pk>/', views.LecturerWrongPersonView, name='LecturerWrongPerson'),
        path('classmates-confirm/<int:pk>/', views.ClassMatesConfirmView, name='ClassMatesConfirm'),
        path('classmates-reject/<int:pk>/', views.ClassMatesRejectView, name='ClassMatesReject'),
        path('classmates-comment/<slug:cmt>/', views.ClassMatesCommentView, name='ClassMatesComment'),
        path('classmates-wrongperson/<slug:cmt>/', views.ClassMatesWrongPersonView, name='ClassMatesWrongPerson'),
        #Colleague Confirm
        path('colleague-confirm/<int:pk>/', views.ColleagueConfirmView, name='ColleagueConfirm'),
        path('colleague-reject/<int:pk>/', views.ColleagueRejectView, name='ColleagueReject'),
        path('colleague-wrongperson/<int:pk>/', views.ColleagueWrongPersonView, name='ColleagueWrongPerson'),
        path('colleague-comment/<slug:clg>/', views.ColleagueCommentView, name='ColleagueComment'),
        #Superior Confirm
        path('superior-confirm/<int:pk>/', views.SuperiorConfirmView, name='SuperiorConfirm'),
        path('superior-reject/<int:pk>/', views.SuperiorRejectView, name='SuperiorReject'),
        path('superior-wrongperson/<int:pk>/', views.SuperiorWrongPersonView, name='SuperiorWrongPerson'),
        path('superior-comment/<slug:spr>/', views.SuperiorCommentView, name='SuperiorComment'),
        #Collaborator confirm
        path('collaborator-confirm/<int:pk>/', views.CollaboratorConfirmView, name='CollaboratorConfirm'),
        path('collaborator-reject/<int:pk>/', views.CollaboratorRejectView, name='CollaboratorReject'),
        path('collaborator-wrongperson/<int:pk>/', views.CollaboratorWrongPersonView, name='CollaboratorWrongPerson'),
        path('collaborator-comment/<slug:clb>/', views.CollaboratorCommentView, name='CollaboratorComment'),
        #Client Confirm
        path('client-confirm/<int:pk>/', views.ClientConfirmView, name='ClientConfirm'),
        path('client-reject/<int:pk>/', views.ClientRejectView, name='ClientReject'),
        path('client-wrongperson/<int:pk>/', views.ClientWrongPersonView, name='ClientWrongPerson'),
        path('client-comment/<slug:wkc>/', views.ClientCommentView, name='ClientComment'),
        #PreColleague Confirm
        path('precolleague-confirm/<int:pk>/', views.PreColleagueConfirmView, name='PreColleagueConfirm'),
        path('precolleague-reject/<int:pk>/', views.PreColleagueRejectView, name='PreColleagueReject'),
        path('precolleague-wrongperson/<int:pk>/', views.PreColleagueWrongPersonView, name='PreColleagueWrongPerson'),
        path('precolleague-comment/<slug:clg>/', views.PreColleagueCommentView, name='PreColleagueComment'),
        path('careerhistory/', views.BriefCareerHistoryView, name='History'),
        path('career-resign/<slug:bch>/<slug:tlt>/', views.ResignedView, name='Resigned'),
        path('int-remove/<int:int_id>/', views.InterviewTltRemove, name='IntRemove'),
        path('int-accept/<int:int_id>/', views.InterviewAcceptView, name='IntAccept'),
        path('int-decline/<int:int_id>/', views.InterviewDeclineView, name='IntDecline'),
        path('int-complete/<int:int_id>/', views.InterviewTltComplete, name='IntComplete'),
        path('assignment-accept/<slug:slug>/', views.AssignmentAcceptView, name='AssignmentAccept'),
        path('assignment-decline/<slug:slug>/', views.AssignmentDeclineView, name='AssignmentDecline'),
        path('assignment-rfi/<slug:wit>/', views.AssignmentClarifyView, name='AssignmentClarify'),
        path('assignment-reassign/<slug:slug>/', views.AssignmentReAssign, name='AssignmentReassign'),
        #Talent Workshop
        path('workshop-tlt/', views.TltWorkshopView, name='WorkshopTlt'),
        path('tlt-mark-complete/<slug:wit>/', views.TltVacancyComplete, name="TltMarkComp"),
        path('rate-tlt/<slug:wit>/', views.TltUpdateStatusRate, name='TltRatePerformance'),
        path('rate-tlt-view/<slug:wit>/', views.TltRatingView, name='TltRateView'),
        #Employer Office
        path('workshop-emp/', views.EmpWorkshopView, name='WorkshopEmp'),
        path('rate-emp/<slug:wit>/', views.EmpUpdateStatusRate, name='EmpRatePerformance'),
        path('rate-emp-view/<slug:wit>/', views.EmpRatingView, name='EmpRateView'),
        path('emp-mark-complete/<slug:wit>/', views.EmpVacancyComplete, name="EmpMarkComp"),
        # Help pages
        path('help/desktop/assignment-tracking/', views.HelpDesktopWorkshopView, name='HelpDesktopWorkshop'),
        path('help/desktop/information/', views.HelpDesktopInformationView, name='HelpDesktopInformation'),
        path('help/desktop/network/', views.HelpDesktopNetworkView, name='HelpDesktopNetwork'),
        path('help/desktop/workflow/', views.HelpDesktopWorkflowView, name='HelpDesktopWorkflow'),
        path('help/desktop/pending-interviews/', views.HelpDesktopPendingInterviewsView, name='HelpDesktopPendingInterviews'),
        path('help/desktop/assignments/', views.HelpDesktopAssignmentsView, name='HelpDesktopAssignments'),

]
