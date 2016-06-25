from django import forms
from .models import Post

class PostNormalForm(forms.Form):
    # 변수 명이 관련된 html 태그를 만들때 name 속성으로 들어간다.
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

class PostForm(forms.ModelForm):

    def clean(self):
        if '하하' in self.cleaned_data['title']:
            self.add_error('title', '하하는 추가하지마. ')


    class Meta:
        model = Post
        fields = ('title', 'content', 'category', )  # 전체를 지정하고 싶으면 fields = __all__
