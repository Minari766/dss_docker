from django.conf import settings
from django.db import models
from django.utils import timezone

class Area(models.Model):
    name = models.CharField("エリア", max_length=100)
    slug = models.SlugField("スラッグ")

    def __str__(self):
        return str(self.name)

class Attraction(models.Model):
    name = models.CharField("アトラクション", max_length=100)
    slug = models.SlugField("スラッグ")

    def __str__(self):
        return str(self.name)

class Category(models.Model):
    name = models.CharField("カテゴリ", max_length=100)
    slug = models.SlugField("スラッグ")

    def __str__(self):
        return str(self.name)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name='エリア', on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, verbose_name='アトラクション', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    # blank=Trueであれば、QueryにデータがなくてもNot matchingエラーが出ない
    image = models.ImageField(upload_to='images', verbose_name='Image画像', null=True, blank=True)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)
    public = models.BooleanField("公開フラグ", default=False)
    # for post in Post.objects.annotate(Count('post')):

    def __str__(self):
        return str(self.title)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # AUTH_USER_MODEL：ログイン中のUser情報
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    # 管理画面で表示される文字列
    def __str__(self):
        return str(self.post)
