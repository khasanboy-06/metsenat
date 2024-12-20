from django.contrib import admin

from apps.common.models import (StudentSponsor, Student,
                            Sponsor, University)

admin.site.register([StudentSponsor, Student, Sponsor, University])