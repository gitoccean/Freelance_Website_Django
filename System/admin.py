from django.contrib import admin
from .models import Jobs, extended, Book, Contact_form, Document, customer, Location , Author, Skill


# make to customize and fields which you want to show in Super User which is provided by default to make a good interface
class Superuser(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('title', 'status', 'date')
    # fields = (('title','amount'),'status','date','description')
    # exclude = ('slug',)
    fieldsets = (
        ('Basic Information', {
            # 'classes': ('wide',),  # CSS property to create spaces between fields
            'fields': (('title', 'amount',), 'status', 'date', 'location')
        }),
        ('More Information', {
            'classes': ('collapse',),
            'fields': ('description', 'slug')
        })
    )


# Register your models here.

# inwhich model you want customize must have a link
# admin.site.register(Jobs, Superuser)
admin.site.register(Jobs)
admin.site.register(extended)
admin.site.register(Book)
admin.site.register(Contact_form)
admin.site.register(Document)
admin.site.register(customer)
admin.site.register(Location)
admin.site.register(Author)
admin.site.register(Skill)

# no need to register relations model like OneToOne, ManyToOne, ManyToMany model, only register here those, which you want to show these models on Django Admin panel