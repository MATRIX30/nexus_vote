from django.contrib import admin
from polling_app.models import User, Vote, VoteOption, Registration, Poll
# Register your models here.

admin.site.register(User)
admin.site.register(Vote)
admin.site.register(VoteOption)
admin.site.register(Registration)
admin.site.register(Poll)