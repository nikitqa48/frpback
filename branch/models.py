from django.db import models
from PIL import Image
import os
from io import BytesIO
from django.utils.text import slugify
from django.utils import timezone
from django.core.files.base import ContentFile
from django.urls import reverse

class Branch(models.Model):
    name = models.CharField('Название Отрасли', max_length=100)
    image = models.ImageField(upload_to = 'branch')
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    class Meta:
        verbose_name = 'Отрасль'
        verbose_name_plural = 'Отрасли'

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField('Краткое название компании', max_length=100)
    logo = models.ImageField('Логотип', upload_to='company' , null=True)
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False)
    full_name = models.CharField('Полное название компании', max_length=100)
    description = models.TextField('Описание')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Отрасль' , null=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название продукта', max_length=500)
    price = models.CharField('Цена', max_length=500, default=0) 
    description = models.TextField('Описание продукта')
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=False)
    organisation = models.ForeignKey(Company, verbose_name='Производитель', on_delete=models.CASCADE, related_name='products')
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукция'
    
    def __str__(self):
        return self.name


def get_path_upload_image(instance, filename):
    """
    Переопределение имени и путя фотографии, сокращение названия
    В следующий формат: (media)/product/2019-08-20/photo-name_23-59-59.extension
    """
    if '/' in filename:
        filename = filename.split('/')[-1]
    img_header, img_extension = os.path.splitext(filename)
    if len(img_header) > 30:
        if img_header[-6:] == '_thumb':
            img_header = img_header[:30] + '_thumb'
        else:
            img_header = img_header[:30]
    time = timezone.now().strftime('%Y-%m-%d')
    img_name = img_header + '_' + time + img_extension
    path = os.path.join('product/', '{}').format(img_name)
    return path

class ProductPhoto(models.Model):
    image = models.ImageField('Фото продукции', upload_to=get_path_upload_image)
    product = models.ForeignKey(Product, verbose_name='Продукция', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотографии к продукции'
        verbose_name_plural = 'Фотографии к продукции'

    def save(self, *args, **kwargs):
        self.make_thumbnail()
        super(ProductPhoto, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

    def make_thumbnail(self):
        image = Image.open(self.image)
        if image.width > 1920 or image.height > 1080:
            output_size = (1920, 1080)
            image.thumbnail(output_size, Image.ANTIALIAS)
            path = self.image
            temp_thumb = BytesIO()
            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_filename = thumb_name + '_thumb' + thumb_extension
            image.save(temp_thumb, 'JPEG')
            temp_thumb.seek(0)
            self.image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()
            # image.save(quality=80, fp='media/product/{}'.format(path))
            