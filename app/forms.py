from django import forms
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import BadHeaderError, message, send_mail
from django.http import HttpResponse
from .models import Area, Attraction, Category


class PostForm(forms.Form):
    # here

    def __init__(self, *args, **kwargs):
        # __init__ メソッドは、必ず最初に実行される
        # (class ではなく instance の初期化時という意味で"最初")

        # - 例え話
        #     - class: 猫型ロボットの設計図
        #     - instance: ドラえもん、ドラミちゃん、ドラ○○、…
        #     - 設計図から実際のロボットを作り出す操作のことを「インスタンス化」という

        # ※インスタンス化
        # draemon = CatRobot(name='ドラえもん', color='yellow')

        # ↑メソッドの呼び出しに似てる
        # def func():
        #     ...

        # ★↓このように書き換えたが、「title = ...」部分の処理で self 変数を参照できないためこれでもダメ。
        # ModelChoiceField を使うべし。

        area_data = Area.objects.all()
        self.area_choice = {}
        for area in area_data:
            self.area_choice[area] = area
        
        attraction_data = Attraction.objects.all()
        self.attraction_choice = {}
        for attraction in attraction_data:
            self.attraction_choice[attraction] = attraction

        category_data = Category.objects.all()
        self.category_choice = {}
        for category in category_data:
            self.category_choice[category] = category

        title = forms.CharField(max_length=50, label='タイトル')
        # area = forms.ChoiceField(label='エリア', widget=forms.Select, choices=list(self.area_choice.items()), initial="----選択してください")
        area = forms.ModelChoiceField(queryset=Area.objects.all(), label='エリア', widget=forms.Select, initial="----選択してください")
        # attraction = forms.ChoiceField(label='アトラクション', widget=forms.Select, choices=list(self.attraction_choice.items()))
        attraction = forms.ModelChoiceField(queryset=Attraction.objects.all(), label='アトラクション', widget=forms.Select, initial="----エリアを選択してください")
        # category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(self.category_choice.items()), initial="----選択してください")
        category = forms.ModelChoiceField(queryset=Category.objects.all(), label='カテゴリ', widget=forms.Select, initial="----選択してください")
        content = forms.CharField(label='内容', widget=forms.Textarea())
        image = forms.ImageField(label='イメージ画像', required=False)

    def clean_name(self):
        area = self.cleaned_data.get('area')
        if area in ('ワールドバザール'):
            self.add_error('area', 'お名前に禁止ワードが含まれています')
        return area

CATEGORIES = (
    ('0', '----選択してください'),
    ('1', 'このサイトについて'),
    ('2', '投稿記事について'),
    ('3', '不具合について'),
    ('4', 'ご意見・ご要望'),
)

class ContactForm(forms.Form):
    name = forms.CharField(
        label='お名前',
        max_length=30, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '入力してください',
        })
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '入力してください',
        })
    )
    cntct_category = forms.ChoiceField(
        label='カテゴリー',
        choices=CATEGORIES,
        widget=forms.Select(attrs={
        'class': 'form-control',
        })
    )
    message = forms.CharField(
        label='お問い合わせ内容',
        max_length=5000,
        widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': '入力してください(最大5,000文字)',
        }),
    )
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ('ばか', 'あほ', 'まぬけ', 'うんこ', '死ね'):
            self.add_error('name', 'お名前に禁止ワードが含まれています')
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message in ('ばか', 'あほ', 'まぬけ', 'うんこ', '死ね'):
            self.add_error('message', 'お問い合わせ内容に禁止ワードが含まれています')
        return message
