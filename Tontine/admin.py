from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import (Fond, Notification, Tontine, Reunion,
                     MesTontine, MesReunion, Election, Candidat, Vote, Cotisation)
from .models import MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'surname', 'address', 'email',
                  'telephone', 'date_of_birth', 'profession', 'profile')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        if (password1 == password2) and (len(password1) < 8):
            L = ['Password Must Be Atleast 6 characters',
                 'Password Must contain an alphanumeric characters', 'COP']
            raise ValidationError(L)
            # "Password Must Be aleast 8 characters", code='HELLO world')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'surname', 'address', 'email', 'telephone',
                  'date_of_birth', 'profession', 'password', 'profile', 'is_active', 'is_admin')

        ordering = ['username']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'surname', 'address',
                    'email', 'telephone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'surname', 'email',)}),
        ('Personal info', {'fields': ('address', 'telephone',
         'date_of_birth', 'profession', 'profile', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'surname', 'address', 'email', 'telephone', 'date_of_birth', 'profession', 'image', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email')
    filter_horizontal = ()


# admin.site.register(Tontine)


@admin.register(Tontine)
class TontineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation', 'slogan',
                    'reglement_interieur', 'creator')
    ordering = ('nom', 'date_creation',)
    search_fields = ('nom', 'slogan')


# admin.site.register(Membre)
admin.site.register(Reunion)
admin.site.register(MesTontine)
admin.site.register(MesReunion)
admin.site.register(Election)
admin.site.register(Candidat)
admin.site.register(Notification)
# admin.site.register(Vote)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('election', 'member', 'candidat')
    ordering = ('election',)
    search_fields = ('election',)


admin.site.register(Fond)

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    list_display = ('id_tontine', 'nom_cotisation', 'montant', 'date', 'cycle')
    ordering = ('id_tontine',)
    search_fields = ('nom_cotisation', 'id_tontine')
