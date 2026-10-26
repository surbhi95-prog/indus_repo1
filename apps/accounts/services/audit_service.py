# from apps.accounts.models.audit_log import AuditLog

# class AuditService:
#  @staticmethod
#  def log(
#         user,
#         module,
#         action,
#         description,
#         request=None
#     ):
#         """
#        Generic Audit Logs
#         """
#         ip = None
#         if request:
#             ip = request.META.get("REMOTE_ADDR")
#             AuditLog.objects.create(
#                 user=user,
#                 module=module,
#                 action=action,
#                 description=description,
#                 ip_address=ip,
#             )
#  @staticmethod
#  def login(user,request):
#     AuditService.log(
#                     user=user,
#                     module="accounts",
#                     action="LOGIN",
#                     description=f"User {user.email} logged in Successfully",
#                     request=request,
#                 )


#  @staticmethod
#  def logout(user,request):
#                     AuditService.log(
#                         user=user,
#                         module="accounts",
#                         action="LOGOUT",
#                         description=f"User {user.email} logged out Successfully",
#                         request=request,
#                     )

# @staticmethod
# def failed_login(email,request):
#             AuditLog.objects.create(
#                 user=None,
#                 module="accounts",
#                 action="FAILED_LOGIN",
#                 description=f"Failed login attempt for {email}",
#                 ip_address=request.META.get(
#                     "REMOTE_ADDR"
#                 )
#             )
# @staticmethod
# def password_changed(user,request):
#             AuditService.log(
#                 user=user,
#                 module="accounts",
#                 action="PASSWORD_CHANGED",
#                 description="password changed",
#                 request=request
#             )

# @staticmethod
# def password_reset(user,request):
#             AuditService.log(
#                 user=user,
#                 module="accounts",
#                 action="PASSWORD_RESET",
#                 description="Password Reset Successfully.",
#                 request=request
#             )
                 


from apps.accounts.models.audit_log import AuditLog


class AuditService:

    @staticmethod
    def log(user, module, action, description, request=None):
        """
        Generic Audit Logs
        """
        ip = None
        if request:
            ip = request.META.get("REMOTE_ADDR")

        AuditLog.objects.create(
            user=user,
            module=module,
            action=action,
            description=description,
            ip_address=ip,
        )

    @staticmethod
    def login(user, request):
        AuditService.log(
            user=user,
            module="accounts",
            action="LOGIN",
            description=f"User {user.email} logged in successfully",
            request=request,
        )

    @staticmethod
    def logout(user, request):
        AuditService.log(
            user=user,
            module="accounts",
            action="LOGOUT",
            description=f"User {user.email} logged out successfully",
            request=request,
        )

    @staticmethod
    def failed_login(email, request):
        AuditLog.objects.create(
            user=None,
            module="accounts",
            action="FAILED_LOGIN",
            description=f"Failed login attempt for {email}",
            ip_address=request.META.get("REMOTE_ADDR"),
        )

    @staticmethod
    def password_changed(user, request):
        AuditService.log(
            user=user,
            module="accounts",
            action="PASSWORD_CHANGED",
            description="Password changed.",
            request=request,
        )

    @staticmethod
    def password_reset(user, request):
        AuditService.log(
            user=user,
            module="accounts",
            action="PASSWORD_RESET",
            description="Password reset successfully.",
            request=request,
        )