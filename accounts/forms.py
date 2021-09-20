from django import forms
from allauth.account.forms import SignupForm


class ProfileForm(forms.Form):
    user_name = forms.CharField(max_length=30, label='ニックネーム')
    icon = forms.ImageField(label='アイコン画像', required=False)
    
class SignupUserForm(SignupForm):
    user_name = forms.CharField(max_length=30, label='ニックネーム')

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8 :
            raise forms.ValidationError("パスワードはアルファベットと数字の組み合わせで8文字以上としてください。")
        return password1

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.user_name = self.cleaned_data['user_name']
        user.save()
        return user