from django import template
from django.utils.safestring import mark_safe


register = template.Library()


TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """


TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'Производитель': 'brand',
        'Модель': 'model',
        'Цвет': 'color',
        'Диагональ': 'diagonal',
        'Разрешение экрана': 'screen_resolution',
        'Тип дисплея': 'display_type',
        'Операционная система': 'os',
        'Процессор': 'cpu',
        'Видеокарта': 'gpu',
        'Оперативная память': 'ram',
        'Твердотельный накопитель': 'ssd',
        'НЖМД': 'hdd',
        'Аккумулятор': 'battery',
        'Габариты ШхВхГ': 'dimension',
        'Веб-камера': 'web_cam',
        'Wi-Fi': 'wifi',
        'Bluetooth': 'bluetooth',
        'Подсветка': 'rgb',
    },
    'desktop': {
        'Производитель': 'brand',
        'Модель': 'model',
        'Форм-фактор корпуса': 'form_factor',
        'Цвет': 'color',
        'Операционная система': 'os',
        'Процессор': 'cpu',
        'Видеокарта': 'gpu',
        'Материнская плата': 'motherboard',
        'Оперативная память': 'ram',
        'Твердотельный накопитель': 'ssd',
        'НЖМД': 'hdd',
        'Блок питания': 'psu',
        'Корпус': 'case',
        'Габариты ШхВхГ': 'dimension',
        'Wi-Fi': 'wifi',
        'Bluetooth': 'bluetooth',
        'Подсветка': 'rgb',
    },
}

def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)