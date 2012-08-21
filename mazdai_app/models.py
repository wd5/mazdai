# coding=utf-8
from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=300, verbose_name='Имя')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')

    @property
    def quantities(self):
        result = []
        all_markets = list(Market.objects.all().order_by('name'))

        for market in all_markets:
            goods_quantity = None

            try:
                goods_quantity = GoodsQuantity.objects.get(position=self, market=market)
            except:
                pass

            if goods_quantity:
                result.append(goods_quantity.quantity)
            else:
                result.append(0)

        return result

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'


class Market(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class GoodsQuantity(models.Model):
    position = models.ForeignKey(Position, verbose_name='Позиция')
    market = models.ForeignKey(Market, verbose_name='Магазин')
    quantity = models.IntegerField(verbose_name='Количество')

    def __unicode__(self):
        return '%s(%s) - %d' % (self.position, self.market.name, self.quantity)

    class Meta:
        verbose_name = 'Количество товара'
        verbose_name_plural = 'Количества товара'


class SaleEntry(models.Model):
    position = models.ForeignKey(Position)
    date = models.DateTimeField(verbose_name='Дата')
    quantity = models.IntegerField(verbose_name='Количество', max_length=3)
    market = models.ForeignKey(Market, verbose_name='Магазин')